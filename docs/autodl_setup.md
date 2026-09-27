# Habitat-GS 在 AutoDL 上的环境搭建避坑指南

> 实测环境：AutoDL 容器，RTX 4090 24G / Xeon Gold 6430 16C / 1TB RAM
> 系统盘 `/` 仅 30G，数据盘 `/root/autodl-tmp` 200G
> 日期：2026-09-27，验证范围：安装 → episodes 生成 → GS headless 渲染 → DDPPO 冒烟训练

## 核心原则：大文件全部放数据盘

系统盘只有 30G，conda 环境（~5.3G）+ pip 缓存 + HF 下载缓存会迅速撑爆。

```bash
# conda 环境默认建到数据盘
conda config --add envs_dirs /root/autodl-tmp/envs
# 数据下载目录也放数据盘，再软链进仓库
mkdir -p /root/autodl-tmp/gs_scenes /root/ws/habitat-gs/data/scene_datasets
ln -sfn /root/autodl-tmp/gs_scenes /root/ws/habitat-gs/data/scene_datasets/gs_scenes
```

## 坑 1：torch 国际线下载慢 → 直接克隆 AutoDL base 镜像

README 让你 `pip install torch --index-url download.pytorch.org/whl/cu121`，但 2GB 轮子走国际线约 0.86 MB/s（40 分钟+），国内镜像（aliyun/sjtu pytorch-wheels）实测超时或极慢。

**AutoDL base 环境自带 `torch 2.3.0+cu121`（与 README 要求一致），克隆它零下载：**

```bash
conda create -y -p /root/autodl-tmp/envs/habitat-gs --clone /root/miniconda3
# 补上构建工具（pip 走阿里云源，秒装）
/root/autodl-tmp/envs/habitat-gs/bin/pip install "cmake==3.27.*" ninja
```

## 坑 2：编译缺系统库（X11 / EGL / glm）

直接 `pip install .` 会在 CMake 配置或编译中期报缺失，按报错对号入座：

| 报错 | 缺的东西 |
|---|---|
| `Could NOT find X11` | glfw 需要 X11 头文件 |
| `Could NOT find EGL` | magnum headless 上下文需要 EGL 头文件 |
| `fatal error: glm/glm.hpp: No such file` | CUDA 光栅化器依赖系统 glm（仓库未 vendored） |

**一次装齐：**

```bash
apt-get update && apt-get install -y \
  xorg-dev libgl1-mesa-dev libglu1-mesa-dev mesa-common-dev \
  libegl1-mesa-dev libegl-dev libgles2-mesa-dev libglm-dev
```

然后编译（约 5–20 分钟，CUDA ON / Bullet OFF）：

```bash
source /etc/network_turbo   # 子模块走加速（见坑 4）
cd /root/ws/habitat-gs
git submodule update --init --recursive --jobs 8
CUDA_HOME=/usr/local/cuda HABITAT_WITH_CUDA=ON HABITAT_WITH_BULLET=OFF \
  CMAKE_BUILD_PARALLEL_LEVEL=16 \
  pip install . --no-build-isolation
```

> `--no-build-isolation` 是为了用环境里已装的 cmake 3.27 / ninja。

## 坑 3：headless 渲染报 "Unable to create windowless context"

**AutoDL 容器最阴的坑。** 编译、import 一切正常，一渲染就报：

```
Platform::WindowlessEglApplication::tryCreateContext(): unable to find CUDA device 0
  among 1 EGL devices in total
WindowlessContext: Unable to create windowless context
```

原因：驱动提供了 `libEGL_nvidia.so.0`，但 glvnd 的 vendor 注册目录里只有
`50_mesa.json`，EGL 根本不知道 NVIDIA 的存在。

**修复（容器内 root 直接写）：**

```bash
cat > /usr/share/glvnd/egl_vendor.d/10_nvidia.json <<'EOF'
{
    "file_format_version" : "1.0.0",
    "ICD" : {
        "library_path" : "libEGL_nvidia.so.0"
    }
}
EOF
```

> 注意：**换实例/重建容器后要重做**，这个文件不在你的持久数据盘里（`/root` 下除
> `autodl-tmp` 外的内容随镜像而定，建议把上面这条写进启动脚本自查）。

## 坑 4：网络

- **GitHub / HuggingFace**：`source /etc/network_turbo`（学术加速代理）。子模块 17 个、约 600MB，不开加速基本拉不动。
- **pip**：AutoDL 已默认阿里云源，**别在开着 network_turbo 的 shell 里 pip install**（代理会让国内源变慢）。用完可 `unset http_proxy https_proxy`。
- **conda**：已配 TUNA 源。

## 坑 5：OpenCV 5.0 破坏 habitat-lab 导入

`import habitat` 直接崩：

```
habitat/utils/visualizations/maps.py, line 44: ValueError:
  cannot select an axis to squeeze out which has size not equal to one
```

原因：habitat-lab 声明依赖 `opencv-python>=3.3.0`，pip 会装上新发布的大版本
OpenCV 5.x，而 5.x 的 `cv2.applyColorMap` 输出形状从 `(N,1,3)` 变成 `(N,3)`。

**修复：**

```bash
pip install "opencv-python==4.10.0.84"
```

## 坑 6：HF 数据集下载不要用 `hf download --include` 多通配符

`huggingface_hub` 1.32 的 CLI 会把 `--include` 后的多个 pattern 当成显式文件名列表，
然后**递归展开整个仓库**去匹配——gs_scenes 仓库的 `trajectory_data/` 有几十万张图，
命令会静默卡死十几分钟不报错（进程高 CPU、无输出、零文件落下）。

**小规模下载用显式文件清单**（单场景约 130–350MB）：

```python
# python 脚本，逐文件 hf_hub_download；或先经 API 拿到文件名再喂给 CLI
from huggingface_hub import hf_hub_download
files = [
    "train.scene_dataset_config.json", "val.scene_dataset_config.json",
    "train/scene01/scene01.gs.ply", "train/scene01/scene01.navmesh",
    # ... configs/*.yaml（16 个小文件）等
]
for f in files:
    hf_hub_download("RukawaY/gs_scenes", f, repo_type="dataset",
                    local_dir="/root/autodl-tmp/gs_scenes")
```

缺场景不报错：顶层配置按 `train/*/*.gs.ply` 通配 stage，navmesh 路径按需解析，
生成脚本也支持 `--scene scene01` 只跑已下载的场景。

## 坑 7：ObjectNav 生成缺包 & SAM/CLIP 权重获取

`generate_objectnav_episodes.py` 会报 `ModuleNotFoundError: No module named 'sklearn'`：

```bash
pip install segment-anything open-clip-torch scikit-learn
```

权重放 `~/.cache/sam_checkpoints/sam_vit_b_01ec64.pth`（375MB）与
`~/.cache/clip_models/vit_b_32_laion400m.pt`（605MB，即 open_clip 官方
`vit_b_32-quickgelu-laion400m_e32-46683a32.pt` 改名）。AutoDL 上的实测获取路径：

- **CLIP**：`dl.fbaipublicfiles.com` 直连极慢且代理 403；但 **GitHub release 走
  `/etc/network_turbo` 代理正常**（约 10MB/s）：
  `curl -Lx $PROXY https://github.com/mlfoundations/open_clip/releases/download/v0.2-weights/vit_b_32-quickgelu-laion400m_e32-46683a32.pt`
- **SAM**：Meta CDN 走代理 403；`hf download ybelkada/segment-anything
  --repo-type model checkpoints/sam_vit_b_01ec64.pth --local-dir <dir>`
  设 `HF_ENDPOINT=https://hf-mirror.com` 下载，中途会反复停滞，
  **套一层重试循环让它断点续传**即可（实测几分钟~1小时不等）。
- ⚠️ `gh-proxy.com` 之类的 GitHub 加速站会返回 **HTTP 200 的错误页**（195 字节
  HTML），curl `-f` 不报错——**下完必须校验文件大小**，别只看退出码。

## 验证清单（全部通过的标志）

```bash
E=/root/autodl-tmp/envs/habitat-gs/bin/python
$E -c "import habitat, habitat_baselines, habitat_sim; print('ok')"
$E scripts_gs/generate_pointnav_episodes.py --scene scene01 --train-episodes 50
$E scripts_gs/generate_imagenav_episodes.py --scene scene01 --train-episodes 5
$E scripts_gs/generate_objectnav_episodes.py --scene scene01 --train-episodes 5
# ↑ 末尾打印 "Categories found: [...]" + Done = SAM/CLIP 检测聚类链路通
# ↑ "Total image-quality rejects: 0" = GS headless 渲染真实出图（目标图不落盘，训练时按位姿现渲）
cd /root/ws/habitat-lab && bash /root/ws/habitat-gs/scripts_gs/train_pointnav.sh \
  --output /tmp/ptnav_smoke --total-steps 128 --num-envs 2   # 冒烟训练出 ckpt
```

已知良性告警：`scene01.gs.scn ... failed to load`（无可选语义标注文件，PointNav/ImageNav 不依赖）。

## 硬件边界备忘

| 任务 | 单卡 4090 24G |
|---|---|
| GS 渲染 / 数据采集（episodes、轨迹） | ✅ 完全够用 |
| DDPPO PointNav/ImageNav/ObjectNav | ✅ 可训（论文规模 5e8–2.5e9 步需数周，建议调小 total-steps 或下载官方 ckpt） |
| StreamVLN | 仅 `--lora` 模式可训 |
| StreamVLN 全参 / Uni-NaVid stage-1 | ❌ 需 ≥80GB VRAM（A100/H100） |
| 交互式 gaussian_viewer | ❌ 需要桌面/X11；headless 场景请走脚本 |
