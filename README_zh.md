<div align="center">

<h1 align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/gs_assets/logo_black.png">
    <source media="(prefers-color-scheme: light)" srcset="docs/gs_assets/logo_white.png">
    <img alt="Habitat-GS" src="docs/gs_assets/logo_black.png" width="50%">
  </picture><br>
  基于动态高斯泼溅的高保真导航模拟器
  <br>
  <sub>ECCV 2026</sub>
</h1>

<div align="center">
  <a href="https://arxiv.org/abs/2604.12626"><img src='https://img.shields.io/badge/arXiv-Habitat--GS-red' alt='Paper PDF'></a>
  <a href='https://zju3dv.github.io/habitat-gs/'><img src='https://img.shields.io/badge/Project_Page-Habitat--GS-orange' alt='Project Page'></a>
  <a href="https://huggingface.co/datasets/RukawaY/gs_scenes"><img src='https://img.shields.io/badge/%F0%9F%A4%97%20Hugging_Face-GS_Dataset-blue' alt='Hugging Face'></a>
  <a href="docs/gs_assets/wechat.png">
    <img src="https://img.shields.io/badge/WeChat-Group-green?logo=wechat&logoColor=green">
  </a>
</div>
  
<p align="center">
  <a href="https://ziyuan-xia.com">Ziyuan Xia</a> •
  <a href="https://github.com/echo636">Jingyi Xu</a> •
  <a href="https://github.com/Kinchite17">Chong Cui</a> •
  <a href="https://yuanhongyu.xyz">Yuanhong Yu</a> •
  <a href="https://jzhzhang.github.io">Jiazhao Zhang</a> •
  <a href="https://yanqswhu.top">Qingsong Yan</a> •
  <a href="https://orcid.org/0000-0002-8676-6546">Tao Ni</a> <br>
  <a href="https://scholar.google.com/citations?user=4YOIYGwAAAAJ&hl=en">Junbo Chen</a> •
  <a href="https://xzhou.me">Xiaowei Zhou</a> •
  <a href="http://www.cad.zju.edu.cn/home/bao/">Hujun Bao</a> •
  <a href="https://csse.szu.edu.cn/staff/ruizhenhu/">Ruizhen Hu</a> •
  <a href="https://pengsida.net/">Sida Peng</a>
</p>

</div>

<div align="center">
  <video src="https://github.com/user-attachments/assets/1d971739-3507-4667-b9c1-f9debd64ea76" controls width="600"></video>
</div>


## 📢 动态

> **[2026-06]** 🎉 Habitat-GS 被 ECCV 2026 接收！Malmö 见！

> **[2026-05]** 🎉 试试我们的 [NavMesh 编辑工具](https://github.com/zju3dv/habitat-gs/blob/main/web_tools/README.md#navmesh_editor)！它打通了从原始 3DGS 场景到可导航仿真的完整闭环（**3DGS → NavMesh → 仿真**）：在浏览器中于 3DGS 场景上绘制/编辑可行走区域，烘焙出 Habitat NavMesh，并在 Habitat-GS 中用于导航。

> **[2026-05]** 🎉 [GS 数据集](https://huggingface.co/datasets/RukawaY/gs_scenes)新增 64 个 [InteriorGS](https://huggingface.co/datasets/spatialverse/InteriorGS) 场景！目前共 129 个场景！

> **[2026-04]** 🎉 [GS 数据集](https://huggingface.co/datasets/RukawaY/gs_scenes)更新！我们提供 65 个高质量 GS 场景，以及用于训练和评估的 episodes 与轨迹！

> **[2026-04]** 🎉 Habitat-GS 的论文、项目主页、代码和数据集全部发布！快来看看！

## 🧭 Habitat-GS 是什么？能做什么？

`Habitat-GS` 是 [Habitat-Sim](https://github.com/facebookresearch/habitat-sim) 的一个非侵入式扩展，面向 Gaussian Splatting（高斯泼溅）场景中的具身导航任务。它保留了 [Habitat](https://aihabitat.org) 标准的场景数据集抽象、NavMesh/路径规划、智能体控制以及 [Habitat-Lab](https://github.com/facebookresearch/habitat-lab) 集成，同时将渲染后端扩展为支持 [3D Gaussian Splatting](https://github.com/graphdeco-inria/gaussian-splatting)，并引入了动态高斯化身（gaussian avatar）模块来驱动人形高斯化身。

在实践中，Habitat-GS 可以：

- 使用 Habitat 的 RGB 和深度传感器渲染照片级真实的 GS 场景；
- 支持在仿真环境中驱动来自 [GaussianAvatar](https://github.com/aipixel/GaussianAvatar) 和 [AnimatableGaussians](https://github.com/lizhe00/AnimatableGaussians) 的动态高斯化身；
- 接入 Habitat-Lab，以相同的场景数据集格式进行训练与评估。

与传统基于网格（mesh）的模拟器相比，Habitat-GS 能够实现照片级真实感渲染，并高效渲染高保真的高斯化身。通过将 Gaussian Splatting 引入具身模拟器，我们希望本工作能够推动未来的具身 AI 研究。

## 📖 目录

- 🛠️ [安装 Habitat-GS](#%EF%B8%8F-安装-habitat-gs)
  - 🧪 [创建环境](#-创建环境)
  - 📦 [安装 Habitat-GS](#-安装-habitat-gs)
  - 🤖 [安装 Habitat-Lab](#-安装-habitat-lab可选但推荐)
- 📦 [下载 GS 资产](#-下载-gs-资产)
- 🚀 [运行 Habitat-GS](#-运行-habitat-gs)
  - 🧱 [准备 GS 资产](#-准备-gs-资产)
  - 🗂️ [组织场景数据集](#%EF%B8%8F-组织场景数据集)
  - 🖥️ [运行交互式查看器](#%EF%B8%8F-运行交互式查看器)
- 🦞 [HabitatAgent](#-habitatagent)
- 🏋️ [在 Habitat-GS 上训练/评估导航智能体](#%EF%B8%8F-在-habitat-gs-上训练评估导航智能体)
  - 🗺️ [基于 Habitat-Lab 的 Point/Image/Object Goal 导航](#%EF%B8%8F-基于-habitat-lab-的-pointimageobject-goal-导航)
  - 🗣️ [基于 StreamVLN 的视觉语言导航](#%EF%B8%8F-基于-streamvln-的视觉语言导航)
  - ✈️ [基于 Uni-NaVid 的视觉语言导航](#%EF%B8%8F-基于-uni-navid-的视觉语言导航)
  - 🚶 [基于高斯化身的动态导航](#-基于高斯化身的动态导航)
- 🧩 [Agent Skills](#-agent-skills)
- 📚 [引用](#-引用)

## 🛠️ 安装 Habitat-GS

> 🇨🇳 **国内服务器（AutoDL 等）部署**：环境搭建、编译、headless 渲染、数据集下载等环节在国内云环境下有若干特有的坑（torch 下载慢、X11/EGL/glm 缺库、glvnd 未注册 NVIDIA EGL vendor、OpenCV 5.x 不兼容、HF 下载卡死等），实测避坑指南见 [docs/autodl_setup.md](docs/autodl_setup.md)。

### 🧪 创建环境

```bash
conda create -n habitat-gs python=3.12 cmake=3.27
conda activate habitat-gs

# 重要：先安装与 CUDA 匹配的 torch
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

### 📦 安装 Habitat-GS

```bash
git clone https://github.com/zju3dv/habitat-gs.git
cd habitat-gs
git submodule update --init --recursive

# 推荐：开启 CUDA，关闭 Bullet
HABITAT_WITH_CUDA=ON HABITAT_WITH_BULLET=OFF pip install .
```

如果你还需要 Bullet 物理引擎（例如在 3DGS 场景中操纵 mesh 物体），请使用：

```bash
HABITAT_WITH_CUDA=ON HABITAT_WITH_BULLET=ON pip install .
```

### 🤖 安装 Habitat-Lab（可选但推荐）

Habitat-GS 可以独立用于渲染和场景查看，但导航任务的定义、训练和评估通常需要将 Habitat-Lab 与 Habitat-GS 配合使用。

```bash
git clone https://github.com/facebookresearch/habitat-lab.git
```

**重要**：在安装 Habitat-Lab 到同一环境之前，先修改其对 NumPy 的版本锁定，以避免与 Habitat-GS 冲突：

- 编辑 `habitat-lab/habitat-lab/requirements.txt`
- 将 `numpy==1.26.4` 改为 `numpy>=2.0.0,<2.4`

然后安装：

```bash
cd habitat-lab
pip install -e habitat-lab
pip install -e habitat-baselines
```

> **注意**：[动态导航任务](#-基于高斯化身的动态导航)（化身避障/跟踪）需要我们的**专用 [habitat-lab fork](https://github.com/RukawaY/habitat-lab-dynamic)**。此时请用 `git clone https://github.com/RukawaY/habitat-lab-dynamic.git` 克隆，然后进行相同的修改和安装步骤。

## 📦 下载 GS 资产

更多细节请参考我们的 🤗 [HuggingFace 数据集](https://huggingface.co/datasets/RukawaY/gs_scenes)。我们提供六类资产：

|   | 类别 | 大小 | 用途 |
|---|----------|------|-------------|
| 1 | **GS 场景** | ~27 GB | 一切的基础 —— 核心场景资产 |
| 2 | **高斯化身** | ~3.1 GB | 动态化身仿真 |
| 3 | **Habitat-Lab 导航数据** | ~30 MB | PointNav / ImageNav / ObjectNav 训练与评估 |
| 4 | **StreamVLN 数据** | ~40 GB | VLN 训练与评估（[StreamVLN](https://github.com/InternRobotics/StreamVLN)） |
| 5 | **Uni-NaVid 数据** | ~25 GB | VLN 训练与评估（[Uni-NaVid](https://github.com/jzhzhang/Uni-NaVid)） |
| 6 | **动态导航数据** | ~25 MB | 动态导航（化身避障与跟踪）训练与评估 |

## 🚀 运行 Habitat-GS

### 🧱 准备 GS 资产

Habitat-GS 需要两类资产：GS 场景和 GS 化身。

<details>
<summary>点击展开：GS 场景资产</summary>

对于不含化身的静态 GS 场景，你只需要：

- 一个 3DGS 渲染资产；
- 一个 Habitat 格式的 `.navmesh` 文件用于导航，它定义了智能体的可行走区域。

**重要**：Habitat-GS 通过后缀识别 GS stage 资产，因此你的场景文件必须以 `.gs.ply` 或 `.3dgs.ply` 结尾。

关于 NavMesh 生成，请使用我们的[交互式 Web 工具](https://github.com/zju3dv/habitat-gs/blob/main/web_tools/README.md#navmesh_editor)：它能在浏览器中渲染 GS 场景，让你绘制/修改可行走区域，然后烘焙出供仿真使用的 Habitat `.navmesh`。

```bash
conda activate habitat-gs

python web_tools/navmesh_editor/server.py --port 8080   # 默认场景目录：data/scene_datasets/gs_scenes（含 train/ 和 val/ 子目录）。
# 然后打开 http://localhost:8080 

python web_tools/navmesh_editor/server.py --port 8080 --scene interior_0007_840137        # 打开指定场景
python web_tools/navmesh_editor/server.py --port 8080 --gs-dir /path/to/gs_scenes/train   # 打开目录中的场景
```

</details>

<details>
<summary>点击展开：GS 化身资产</summary>

每个高斯化身需要两个资产：

- `canonical_gs.npz`：从 [GaussianAvatar](https://github.com/aipixel/GaussianAvatar) 或 [AnimatableGaussians](https://github.com/lizhe00/AnimatableGaussians) 导出的标准姿态高斯（canonical gaussians）；
- `driver.pkl`：使用 [GAMMA](https://github.com/yz-cnsdqz/GAMMA-release) 方法在 NavMesh 上生成的场景专属运动驱动器（motion driver）。

1.1. 从 GaussianAvatar 导出标准姿态高斯

在安装好上游仓库后，在 `GaussianAvatar` conda 环境中运行：

```bash
python tools_gs/export_gaussian_avatar_to_canonical.py \
  --posmap /path/to/query_posemap_.npz \
  --lbs-map /path/to/lbs_map_.npy \
  --joint-mat /path/to/smpl_cano_joint_mat.pth \
  --net-ckpt /path/to/net.pth \
  --out /path/to/canonical_gs.npz \
  --ga-root /path/to/GaussianAvatar
```

1.2. 从 AnimatableGaussians 导出标准姿态高斯

类似地，在安装好上游仓库后，在 `AnimatableGaussians` conda 环境中运行：

```bash
python tools_gs/export_animatable_to_canonical.py \
  --config /path/to/config.yaml \
  --ckpt /path/to/checkpoints \
  --out /path/to/canonical_gs.npz \
  --anim-root /path/to/AnimatableGaussians \
  --smpl-model-path /path/to/AnimatableGaussians/smpl_files/smplx
```

2. 在场景 NavMesh 上生成运动驱动器

`driver.pkl` 依赖于目标场景，因为它是在场景 NavMesh 上生成的。请在安装好 GAMMA 后的 `GAMMA` 环境中运行以下命令，并确保该环境中可以导入 `habitat_sim`。

> **GAMMA 环境**：conda 环境的搭建请参考 [`environment.yml`](https://github.com/user-attachments/files/28255628/environment.yml)（`conda env create -f environment.yml`），并按照其中的说明应用必要的补丁。

我们提供两种模式生成驱动器轨迹：

按目标长度自动采样路径：

```bash
python tools_gs/generate_trajectory.py \
  --navmesh /path/to/scene.navmesh \
  --output /path/to/driver.pkl \
  --path-length 6.0 \
  --smpl-model-path /path/to/smpl_files/smplx \
  --gamma-root /path/to/GAMMA-release
```

显式指定起点/终点/若干途经点：

```bash
python tools_gs/generate_trajectory.py \
  --navmesh /path/to/scene.navmesh \
  --output /path/to/driver.pkl \
  --start 0.0 0.0 0.0 \
  --via 1.0 0.0 -1.0 \
  --end 2.0 0.0 -2.0 \
  --smpl-model-path /path/to/smpl_files/smplx \
  --gamma-root /path/to/GAMMA-release
```

生成的 `driver.pkl` 包含用于渲染的预计算 `joint_mats`。化身渲染采用显式高斯 + CUDA LBS，运行时不需要神经网络前向传播。该 `.pkl` 还包含预计算的 `proxy_capsules`，用于 NavMesh 级别的动态障碍物处理，保证智能体无法穿过高斯化身。

</details>

### 🗂️ 组织场景数据集

Habitat-GS 遵循 Habitat 标准的数据集层级：

`scene_dataset_config.json` → `scene_instance.json` → `stage_config.json`

<details>
<summary>点击展开：推荐的数据集目录结构</summary>

```unicode
playroom/
├── playroom.scene_dataset_config.json
├── configs/
│   ├── scenes/
│   │   └── playroom.scene_instance.json
│   └── stages/
│       └── playroom_stage.stage_config.json
├── stages/
│   └── playroom.gs.ply
├── navmeshes/
│   └── playroom.navmesh
└── avatars/
    └── actor01/
        ├── canonical_gs.npz
        ├── driver.pkl
        └── smplx/
```

`playroom.scene_dataset_config.json`

```json
{
  "stages": {
    "paths": {
      ".json": ["configs/stages"]
    }
  },
  "scene_instances": {
    "paths": {
      ".json": ["configs/scenes"]
    }
  },
  "navmesh_instances": {
    "playroom_navmesh": "navmeshes/playroom.navmesh"
  }
}
```

`configs/stages/playroom_stage.stage_config.json`

```json
{
  "render_asset": "../../stages/playroom.gs.ply"
}
```

`configs/scenes/playroom.scene_instance.json`

```json
{
  "stage_instance": {
    "template_name": "playroom_stage"
  },
  "navmesh_instance": "playroom_navmesh",
  "time_max": 20.0,
  "time_loop": true,
  "gaussian_avatars": [
    {
      "name": "actor01",
      "canonical_gaussians": "../../avatars/actor01/canonical_gs.npz",
      "driver": "../../avatars/actor01/driver.pkl",
      "smpl_model_path": "../../avatars/actor01/smplx",
      "smpl_type": "smplx",
      "scale": 1.0,
      "offset_y": 1.0,
      "time_begin": 0.0,
      "time_end": 20.0
    }
  ]
}
```

说明：

- 如果只需要静态 GS 场景，直接省略 `gaussian_avatars` 即可。
- 如果你的 GS 导出器保存的已经是归一化四元数，且观察到渲染结果出现尖刺或模糊，请在 stage config 中添加 `"norm_quaternion": false`。
- 时间相关字段说明：
  - `time_max`：最大仿真时间（秒）。默认为所有化身中最大的 time_end；场景中无化身时为 0。
  - `time_loop`：是否循环仿真时间。默认为 true。

  对每个化身，你还可以指定：
  - `time_begin`：化身出现的仿真时间。默认为 0。
  - `time_end`：化身消失的仿真时间。默认为 0.025 * 帧数。若 time_end > time_begin + 0.025 * 帧数，化身在剩余时间内会静止在终点处。

</details>

### 🖥️ 运行交互式查看器

`examples/gaussian_viewer.py` 是 Habitat-GS 场景的交互式 RGB/深度查看器。运行查看器需要显示环境（例如本地桌面会话、X11 会话或 VNC 会话）。我们提供两种运行模式：

快速预览 GS 场景：

```bash
python examples/gaussian_viewer.py --input /path/to/playroom.gs.ply
```

运行包含 GS stage + NavMesh + 高斯化身的完整 Habitat 场景数据集：

```bash
python examples/gaussian_viewer.py \
  --dataset /path/to/playroom.scene_dataset_config.json \
  --scene playroom
```

<details>
<summary>点击展开：常用参数</summary>

- `--width` / `--height` 修改窗口大小。
- `--time` 从指定的 Gaussian 时间开始；
- `--time-rate` 修改播放速度；
- `--enable-physics` 开启物理仿真，用于与 GS 场景中的 mesh 物体进行物理交互。需要编译时启用 Bullet。

</details>

<details>
<summary>点击展开：常用查看器快捷键</summary>

- `W/S`：前进/后退
- `A/D`：左移/右移
- `Z/X`：上升/下降
- `方向键`：旋转视角
- `TAB`：在 RGB 和深度之间切换
- `SPACE`：播放/暂停 Gaussian 时间
- `H`：打印帮助
- `[` / `]`：时间轴后退/前进
- `N`：切换 NavMesh 可视化
- `ESC`：退出查看器

</details>

## 🦞 HabitatAgent

`HabitatAgent` 是构建在 Habitat-GS 之上的 LLM 驱动智能体系统，支持
自然语言导航、MCP 工具集成，以及通过终端聊天界面进行交互式场景探索。

核心特性：TUI 聊天、16 个 MCP 桥接工具、自主导航循环、场景图
查询、SPL 评估、rerun 实时可视化、第三人称相机及可选的
可视化机器人模型、多客户端支持（Claude Code、Codex、OpenClaw）。

👉 **[视频演示 → 项目主页](https://zju3dv.github.io/habitat-gs/#agent)**

👉 **[完整文档 → docs/habitatagent.md](docs/habitatagent.md)**

```bash
# 快速开始（TUI + bridge）
pip install -r requirements-agent.txt
python tools/habitat_agent.py

# 带 MCP 服务器（用于 Claude Code / Codex 集成）
python tools/habitat_agent.py --mcp
```

## 🏋️ 在 Habitat-GS 上训练/评估导航智能体

### 🗺️ 基于 Habitat-Lab 的 Point/Image/Object Goal 导航

我们使用 [Habitat-Lab](https://github.com/facebookresearch/habitat-lab) + DDPPO，为 GS 场景上的三类导航任务提供**一键式**训练与评估流程：

| 任务 | 目标 | 传感器 | 动作 |
|------|------|---------|---------|
| **PointNav** | GPS 坐标 | RGB, Depth, GPS, Compass | move_forward, turn_left, turn_right, stop |
| **ImageNav** | 目标图像 | RGB, Depth, ImageGoal | move_forward, turn_left, turn_right, stop |
| **ObjectNav** | 物体类别（如 "bench"） | RGB, Depth, GPS, Compass, ObjectGoal | move_forward, turn_left, turn_right, look_up, look_down, stop |

#### 前置条件

- 在 `habitat-gs` conda 环境中安装好 Habitat-GS 和 Habitat-Lab（见[安装](#%EF%B8%8F-安装-habitat-gs)）
- 下载 GS 数据并放置到 `data/scene_datasets/gs_scenes/`（见[数据布局](#数据布局)）

#### 数据布局

<details>
<summary>点击展开：我们提供的场景数据与生成的 episodes 的结构</summary>

```
data/scene_datasets/gs_scenes/
├── train.scene_dataset_config.json
├── val.scene_dataset_config.json
├── train/                           # 110 个训练场景
│   ├── scene01/                     #   自建场景（55 个）：完整资产
│   │   ├── scene01.gs.ply           #     GS 渲染资产
│   │   ├── scene01.mesh.ply         #     碰撞 mesh（除非启用物理，否则不会被使用）
│   │   └── scene01.navmesh          #     导航网格
│   ├── scene02/ ... scene55/
│   ├── interior_0007_840137/        #   InteriorGS（55 个）：仅 3DGS 和 navmesh
│   │   ├── interior_0007_840137.gs.ply
│   │   └── interior_0007_840137.navmesh
│   └── interior_0022_840117/ ... ×55
├── val/                             # 19 个评估场景
│   ├── scene56/ ... scene65/
│   └── interior_0516_840045/ ... ×9
├── configs/                         # Hydra YAML 配置（已提供）
│   ├── ddppo_pointnav_gs_train.yaml
│   ├── ddppo_pointnav_gs_eval.yaml
│   ├── ddppo_imagenav_gs_train.yaml
│   ├── ddppo_imagenav_gs_eval.yaml
│   ├── ddppo_objectnav_gs_train.yaml
│   └── ddppo_objectnav_gs_eval.yaml
└── episodes/                        # 由下方脚本生成
    ├── pointnav/{train,val}/
    ├── imagenav/{train,val}/
    └── objectnav/{train,val}/
```

</details>

#### 第 1 步：生成 Episodes

训练和评估前必须先生成 episode 数据。我们在发布的数据集中已为每个训练场景提供 1000 个 episodes、每个评估场景提供 100 个 episodes，但你也可以用以下命令自行生成：

```bash
conda activate habitat-gs

# PointNav episodes
python scripts_gs/generate_pointnav_episodes.py

# ImageNav episodes
python scripts_gs/generate_imagenav_episodes.py

# ObjectNav episodes - 户外场景中的户外类别（使用 SAM + CLIP）
python scripts_gs/generate_objectnav_episodes.py

# ObjectNav episodes - InteriorGS 场景中的室内类别（--indoor 开关）
python scripts_gs/generate_objectnav_episodes.py --indoor
```

> 💡 上面的 ObjectNav episode 生成器使用 SAM + CLIP 自动检测物体，可能存在定位误差。若要在任意场景上获得人工核验的精确标注，请使用我们的[交互式 Web 工具](https://github.com/zju3dv/habitat-gs/blob/main/web_tools/README.md#objectnav_helper)，在浏览器中于渲染的 GS 场景上放置并标注物体。

<details>
<summary>点击展开：ObjectNav episode 生成细节</summary>

ObjectNav 使用 **SAM（Segment Anything）** + **CLIP（零样本分类）**自动检测并分类 GS 场景中的物体，然后生成通往这些物体的导航 episodes。

**所需模型权重：**

| 模型 | 路径 | 下载 |
|-------|------|----------|
| SAM ViT-B | `~/.cache/sam_checkpoints/sam_vit_b_01ec64.pth` | [GitHub](https://github.com/facebookresearch/segment-anything#model-checkpoints) |
| CLIP ViT-B-32 | `~/.cache/clip_models/vit_b_32_laion400m.pt` | [GitHub](https://github.com/mlfoundations/open_clip/releases) |

**物体类别：**

| 编号 | 模式 | 类别 |
|---|---|---|
| ID 0–11 | outdoor（默认） | car, bench, tree, street lamp, traffic sign, fire hydrant, trash can, bicycle, **potted plant**, barrier, statue, **chair** |
| ID 12–21 | indoor（`--indoor`） | sofa, bed, dining table, toilet, sink, tv, refrigerator, bookshelf, cabinet, lamp |

</details>

#### 第 2 步：训练

```bash
# PointNav（默认 5e8 步）
bash scripts_gs/train_pointnav.sh --output output/pointnav

# ImageNav（默认 2.5e9 步）
bash scripts_gs/train_imagenav.sh --output output/imagenav

# ObjectNav（默认 2.5e9 步）
bash scripts_gs/train_objectnav.sh --output output/objectnav
```

<details>
<summary>点击展开：训练选项</summary>

所有训练脚本接受相同的选项：

```
--output DIR             保存 checkpoint 和 tensorboard 的输出目录（必填）
--num-envs N             每块 GPU 的并行环境数（默认：4）
--num-gpus N             用于 DDPPO 的 GPU 数量（默认：1）
--total-steps N          总训练步数
--num-ckpts N            保存的 checkpoint 数量（默认：100）
--pretrained-ckpt PATH   从已有 .pth checkpoint 进行微调
                         （会设置 ddppo.pretrained=True；critic 会重新初始化）
```

额外的参数会作为 Hydra override 转发。多 GPU 示例：

```bash
bash scripts_gs/train_objectnav.sh \
    --output output/objectnav \
    --num-envs 8 \
    --num-gpus 4
```

从已训练的 checkpoint 微调：

```bash
bash scripts_gs/train_pointnav.sh \
    --output output/pointnav_ft \
    --pretrained-ckpt output/pointnav/checkpoints/ckpt.99.pth
```

默认会加载**整个** policy（encoder + RNN + actor head）并重新初始化 critic head —— 适合同任务继续训练或迁移到高度相关的任务。若要自定义加载行为，可追加 Hydra override，例如：

```bash
# 保留已训练的 critic
bash scripts_gs/train_pointnav.sh \
    --output output/pointnav_ft \
    --pretrained-ckpt output/pointnav/checkpoints/ckpt.99.pth \
    habitat_baselines.rl.ddppo.reset_critic=False

# 只加载视觉 encoder 主干（如从 PointNav 迁移到 ImageNav）
bash scripts_gs/train_imagenav.sh \
    --output output/imagenav_ft \
    --pretrained-ckpt output/pointnav/checkpoints/ckpt.99.pth \
    habitat_baselines.rl.ddppo.pretrained=False \
    habitat_baselines.rl.ddppo.pretrained_encoder=True \
    habitat_baselines.rl.ddppo.train_encoder=False    # 冻结 encoder
```

> 注意：优化器状态、步数计数器和随机种子会被**重置** —— 这是微调（fine-tuning），不是断点续训（resume）。若要续跑被中断的训练，只需用相同的 `--output` 目录重新启动即可；habitat-baselines 会自动检测 `.resume_state.pth` 并无损继续。

输出结构：

```
output/objectnav/
├── checkpoints/    # .pth checkpoint 文件
├── tb/             # TensorBoard 日志
└── train.log       # 训练日志
```

</details>

#### 第 3 步：评估

```bash
# PointNav
bash scripts_gs/eval_pointnav.sh --ckpt output/pointnav/checkpoints/ckpt.0.pth

# ImageNav
bash scripts_gs/eval_imagenav.sh --ckpt output/imagenav/checkpoints/ckpt.0.pth

# ObjectNav
bash scripts_gs/eval_objectnav.sh --ckpt output/objectnav/checkpoints/ckpt.0.pth
```

<details>
<summary>点击展开：评估选项</summary>

```
--ckpt PATH         .pth checkpoint 文件路径或 checkpoint 目录（必填）
--num-envs N        并行环境数（默认：1）
--video-dir DIR     保存评估 rollout 视频的目录（可选）
```

将 `--ckpt` 指向目录时，会依次评估其中的所有 checkpoint。

</details>

### 🗣️ 基于 StreamVLN 的视觉语言导航

我们还为 [StreamVLN](https://github.com/InternRobotics/StreamVLN)（基于 LLaVA-Video-7B-Qwen2 + SigLIP 构建的 SOTA VLM 导航智能体）在 GS 场景上提供**一键式**训练与评估流程。与使用 Habitat-Lab + DDPPO 的 PointNav/ImageNav/ObjectNav 不同，StreamVLN 是通过在示范轨迹上对视觉语言模型进行监督微调（SFT）训练的。

| 任务 | 目标 | 传感器 | 动作 | 主干网络 |
|------|------|---------|---------|----------|
| **VLN-R2R** | 自然语言指令（如"走过桌子，停在窗户附近"） | RGB, GPS, Compass | move_forward, turn_left, turn_right, stop | LLaVA-Video-7B-Qwen2 + SigLIP |

#### 前置条件

- 一个**独立的** `habitat-gs-streamvln` conda 环境（见下方 `第 1 步`）。StreamVLN 锁定了特定包版本（`transformers==4.45.1`、`accelerate==0.28.0` 等），与主 `habitat-gs` 环境存在冲突。

- 将 StreamVLN 克隆为 `habitat-gs/` 的同级目录：

  ```bash
  cd /path/to/parent
  git clone https://github.com/InternRobotics/StreamVLN.git
  ```

- 下载 GS 数据并放置到 `data/scene_datasets/gs_scenes/`（与上一节相同的布局）

#### 数据布局

<details>
<summary>点击展开：在基础数据集布局之上增加的 VLN 专属文件</summary>

```
data/scene_datasets/gs_scenes/
├── configs/
│   └── vln_gs_eval.yaml             # VLN 评估的 habitat 配置（已提供）
├── episodes/
│   └── vln/                         # 由 generate_vln_episodes.py 生成
│       ├── train/train.json.gz      # 110 场景 × 200 episodes = 22,000 条训练
│       └── val/val.json.gz          # 19 场景 × 50 episodes = 950 条验证
└── trajectory_data/
    └── vln/                         # 由 generate_vln_trajectories.py 生成
        ├── annotations.json         # StreamVLN 格式的动作序列
        └── images/{scene}_gs_{ep_id}/rgb/*.jpg   # 渲染的 RGB 帧
```

</details>

#### 第 1 步：一次性设置

`setup_vln.sh` 会从 `habitat-gs` 克隆出 `habitat-gs-streamvln` conda 环境、为兼容性给 StreamVLN 仓库打补丁、安装 StreamVLN 的 Python 依赖，并将 LLaVA-Video-7B-Qwen2（约 15GB）和 SigLIP（约 3.3GB）权重下载到 `StreamVLN/checkpoints/`。

```bash
bash scripts_gs/setup_vln.sh
```

<details>
<summary>点击展开：setup_vln.sh 实际执行的内容</summary>

该脚本对 StreamVLN 克隆应用 `scripts_gs/streamvln_compat.patch`（4 个文件，+42/−13 行），使得：

- `streamvln/habitat_extensions/measures.py` 兼容 habitat-lab 0.3.3（该版本移除了 `try_cv2_import`）
- `streamvln/streamvln_train.py` 支持通过 `--vision_tower` CLI 覆盖本地模型路径、修复量化加载时的 `low_cpu_mem_usage`、移除重复的量化参数，并为合并 LoRA 后的 checkpoint 添加 tokenizer 加载兜底
- `streamvln/streamvln_eval.py` 显式加载 SigLIP 视觉塔（修复 `delay_load` 问题），并在 `flash_attention_2` 不可用时自动回退到 `eager`
- `llava/model/multimodal_encoder/siglip_encoder.py` 在基于 `device_map` 加载时传递 `low_cpu_mem_usage=True`

该脚本是幂等的 —— 重复运行 `setup_vln.sh` 是安全的。可用参数：

```
--skip-env          跳过创建 conda 环境
--skip-patch        跳过应用兼容性补丁
--skip-download     跳过下载模型权重
--skip-deps         跳过安装 Python 依赖
--hf-token TOKEN    用于受限模型的 HuggingFace token
```

</details>

#### 第 2 步：生成 Episodes 与轨迹

VLN 同时需要 **episodes**（起点/终点 + 自然语言指令）和**轨迹数据**（渲染的 RGB 帧 + 用于 SFT 的真值动作序列）。发布的数据集中两者都已包含，但你也可以重新生成：

```bash
conda activate habitat-gs-streamvln

# 1. 生成 VLN episodes（在 navmesh 上采样路径，用 GS 渲染途经点，
#    并调用 VLM 生成指令文本）。输出 R2RVLN-v1 格式。
python scripts_gs/generate_vln_episodes.py

# 2. 用一个贪心路径跟随器重放每个 episode 并记录
#    （RGB 帧, 动作）对，生成 StreamVLN 轨迹数据。
python scripts_gs/generate_vln_trajectories.py
```

<details>
<summary>点击展开：episode/轨迹生成细节</summary>

`generate_vln_episodes.py` 默认每个训练场景生成 200 个 episodes、每个评估场景生成 50 个，采用 habitat-lab `vln_r2r` 任务消费的标准 R2RVLN-v1 格式。指令通过向 OpenAI 兼容的 VLM 端点发送沿路径的多视角渲染图像来生成。通过 `OPENAI_BASE_URL` + `OPENAI_API_KEY` 环境变量配置端点，或传入 `--api-config /path/to/config.json`。

`generate_vln_trajectories.py` 在每个 episode 上运行基于朝向的贪心路径跟随器（`forward_step=0.25m`、`turn_angle=15°`，终点航点 `success_distance=0.25m`），并记录：

- **annotations.json** —— 每个 episode 一条记录，包含指令、动作序列（`-1`=初始、`0`=stop、`1`=前进、`2`=左转、`3`=右转）以及每步的位姿
- **images/{scene}\_gs\_{ep_id}/rgb/*.jpg** —— 每一步的 RGB 帧，经由 GS 管线渲染

脚本支持 `--resume` 跳过已完成的场景，在生成中断时非常有用。

</details>

#### 第 3 步：训练

训练脚本默认执行**标准全量微调**（视觉塔 + projector + LLM，与 StreamVLN 官方配置一致）。在默认 DeepSpeed ZeRO-2 配置下需要**每块 GPU ≥80 GB 显存**（推荐 A100 80GB）。消费级 GPU（RTX 3090/4090）请添加 `--lora` 参数启用显存友好的 LoRA 训练。

```bash
# ── 标准全量微调 ──

# Stage-1：在示范轨迹上进行 SFT
bash scripts_gs/train_vln.sh --output output/vln_stage1 --stage stage-one

# DAgger：使用 DAgger 采集的数据重新训练
bash scripts_gs/train_vln.sh --output output/vln_dagger --stage dagger \
    --ckpt output/vln_stage1/checkpoint-XXX

# Stage-2：与辅助 QA 数据联合训练
bash scripts_gs/train_vln.sh --output output/vln_stage2 --stage stage-two \
    --ckpt output/vln_dagger/checkpoint-XXX


# ── LoRA 模式 ──
bash scripts_gs/train_vln.sh --output output/vln_stage1 --stage stage-one --lora
bash scripts_gs/train_vln.sh --output output/vln_dagger --stage dagger \
    --ckpt output/vln_stage1 --lora
```

<details>
<summary>点击展开：训练选项</summary>

```
--output DIR        保存 checkpoint 的输出目录（必填）
--stage STAGE       训练阶段：stage-one | dagger | stage-two（默认：stage-one）
--num-gpus N        GPU 数量（默认：1）
--ckpt PATH         基础 checkpoint（stage-one 默认使用本地 LLaVA-Video-7B-Qwen2）
--epochs N          epoch 数（默认：1）
--batch-size N      单设备 batch size（默认：2）
--grad-accum N      梯度累积步数（默认：2）
--lr RATE           学习率（默认：2e-5）
--num-frames N      每个样本的帧数（默认：32）
--lora              启用 LoRA 模式（见下文）
```

**标准模式（默认）：** 全量微调整个模型（约 8 GB 可训练参数），使用 `anyres_max_9` 图像分块、32 帧、32K 上下文和 `torch.compile`。多 GPU 训练使用 DeepSpeed ZeRO-2。需要**每块 GPU ≥80 GB 显存**（推荐 A100 80GB）。

**LoRA 模式（`--lora`）：** 冻结 LLM 主干，只训练 MM projector + LoRA adapter（`r=64, alpha=128`，约 17 MB 可训练参数），帧数降为 4、上下文降为 2K。可在**单块 24GB RTX 4090** 上运行。使用 `--lora` 串联阶段时（如 stage-one → dagger），脚本会自动先合并上一个 LoRA checkpoint 再应用新的 adapter。

</details>

#### 第 4 步：评估

```bash
bash scripts_gs/eval_vln.sh --ckpt output/vln_stage1/checkpoint-XXX
```

<details>
<summary>点击展开：评估选项</summary>

```
--ckpt PATH         训练好的 StreamVLN checkpoint 路径（必填）
--output DIR        结果输出目录（默认：results/vln/<ckpt>_<split>）
--num-gpus N        用于并行 rollout 的 GPU 数（默认：1）
--split SPLIT       评估划分：train | val（默认：val）
--num-frames N      每个样本的帧数（默认：32）
--save-video        保存可视化视频
```

评估器使用 `data/scene_datasets/gs_scenes/configs/vln_gs_eval.yaml`（640x480 的 RGB+Depth、hfov=79°、`forward_step=0.25m`、`turn_angle=15°`、`success_distance=3.0m`、`max_episode_steps=500`），并报告标准 VLN 指标：Success、SPL、Oracle Success、Distance-to-Goal 和 Oracle Navigation Error。

</details>

### ✈️ 基于 Uni-NaVid 的视觉语言导航

我们还支持 [Uni-NaVid](https://github.com/jzhzhang/Uni-NaVid)（RSS 2025）的**一键式**训练与评估流程。它是一个统一的基于视频的视觉-语言-动作模型，用单个模型处理多种具身导航任务（VLN、ObjectNav、EQA 等）。Uni-NaVid 构建于 Vicuna-7B + EVA-ViT-G 之上，采用在线 token 合并实现高效流式推理。

| 任务 | 目标 | 传感器 | 动作 | 主干网络 |
|------|------|---------|---------|----------|
| **VLN-R2R** | 自然语言指令 | RGB（120° HFOV） | move_forward (0.25m)、turn_left/right (30°)、stop | Vicuna-7B + EVA-ViT-G |

#### 前置条件

- 一个**独立的** `habitat-gs-uni-navid` conda 环境（见下方 `第 1 步`）。

- 将 Uni-NaVid 仓库克隆为 `habitat-gs/` 的同级目录：

  ```bash
  cd /path/to/parent
  git clone https://github.com/jzhzhang/Uni-NaVid.git
  ```

- 下载 GS 数据并放置到 `data/scene_datasets/gs_scenes/`（与其他任务相同的布局）

#### 数据布局

<details>
<summary>点击展开：在基础数据集布局之上增加的 Uni-NaVid 专属文件</summary>

```
data/scene_datasets/gs_scenes/
├── configs/
│   └── vln_uninavid_gs_eval.yaml    # Uni-NaVid 评估的 habitat 配置（已提供）
├── episodes/
│   └── vln/                         # 与 StreamVLN 共用
│       ├── train/train.json.gz      # 110 场景 × 200 episodes = 22,000 条训练
│       └── val/val.json.gz          # 19 场景 × 50 episodes = 950 条验证
└── trajectory_data/
    └── uninavid/                    # 由 generate_uninavid_trajectories.py 生成
        ├── nav_gs_train.json        # Uni-NaVid 对话格式标注
        ├── nav_gs_val.json
        └── nav_videos/              # .mp4 轨迹视频
            ├── scene01_gs_000000.mp4
            ├── interior_0007_840137_gs_000000.mp4
            └── ...
```

</details>

#### 第 1 步：一次性设置

`setup_uninavid.sh` 会从 `habitat-gs` 克隆出 `habitat-gs-uni-navid` conda 环境、安装 Uni-NaVid 的 Python 依赖、应用 `scripts_gs/uninavid_compat.patch` 保证兼容性，并下载模型权重（EVA-ViT-G 约 3.5GB、Vicuna-7B 约 13GB、Uni-NaVid 预训练权重约 14GB）。

```bash
bash scripts_gs/setup_uninavid.sh
```

<details>
<summary>点击展开：设置选项</summary>

```
--skip-env          跳过创建 conda 环境
--skip-deps         跳过安装 Python 依赖
--skip-patch        跳过应用 uninavid_compat.patch
--skip-download     跳过下载模型权重
--proxy URL         下载使用的 HTTP 代理
```

</details>

#### 第 2 步：生成轨迹数据

Uni-NaVid 以对话格式的视频轨迹进行训练。该脚本用贪心路径跟随器重放每个 VLN episode，将 RGB 帧记录为 `.mp4` 视频，并生成 Uni-NaVid 对话 JSON 格式的动作标注 —— 两者都已包含在发布的数据集中。

```bash
conda activate habitat-gs-uni-navid
python scripts_gs/generate_uninavid_trajectories.py
```

<details>
<summary>点击展开：轨迹生成细节</summary>

贪心控制器使用 `forward_step=0.25m`、`turn_angle=30°`、`HFOV=120°`。每条轨迹视频以 10 fps 编码。输出的 JSON 使用 Uni-NaVid 的对话格式，带 `NAV_ID` 前缀和 `NAVIGATION_IDENTIFIER` 字符串，以在训练时触发导航专属的 token 处理。

</details>

#### 第 3 步：训练

按 Uni-NaVid 标准支持两阶段训练。需要**每块 GPU ≥80 GB 显存**（推荐 A100 80GB）。
- **stage-1**：从 Vicuna-7B 微调（从零训练，需要大数据集）
- **stage-2**：从预训练的 Uni-NaVid checkpoint 微调（推荐）

```bash
conda activate habitat-gs-uni-navid

# 推荐：从预训练 Uni-NaVid 微调
bash scripts_gs/train_uninavid.sh --output output/uninavid_gs --stage stage-2

# 或者从 Vicuna-7B 开始训练
bash scripts_gs/train_uninavid.sh --output output/uninavid_gs --stage stage-1
```

<details>
<summary>点击展开：训练选项</summary>

```
--output DIR         保存 checkpoint 的输出目录（必填）
--stage STAGE        训练阶段：stage-1|stage-2（默认：stage-2）
--num-gpus N         GPU 数量（默认：1）
--ckpt PATH          基础 checkpoint 路径（按阶段自动选择）
--epochs N           epoch 数（默认：1）
--batch-size N       单设备 batch size（默认：8）
--grad-accum N       梯度累积步数（默认：2）
--lr RATE            学习率（默认：1e-5）
```

</details>

#### 第 4 步：评估

评估在 `habitat.Env` 中在线运行 VLN-v0 任务，与 [NaVid-VLN-CE](https://github.com/jzhzhang/NaVid-VLN-CE) 的评估方式一致。

```bash
conda activate habitat-gs-uni-navid
bash scripts_gs/eval_uninavid.sh --ckpt output/uninavid_gs/<checkpoint>
```

<details>
<summary>点击展开：评估选项</summary>

```
--ckpt PATH         训练好的 Uni-NaVid checkpoint 路径（必填）
--output DIR        结果输出目录（默认：results/uninavid/<ckpt>_<split>）
--num-gpus N        用于并行评估的 GPU 数（默认：1）
--split SPLIT       评估划分：train|val（默认：val）
--save-video        保存评估 rollout 视频
```

评估器报告：Success Rate (SR)、SPL、Oracle Success (OSR) 和 Distance-to-Goal (DTG)。

</details>

### 🚶 基于高斯化身的动态导航

我们在 10 个示例场景上提供动态导航任务的**一键式**训练与评估流程，每个场景中都有一个沿 GAMMA 生成轨迹行走的高斯化身。在三个*避障*任务中，化身是导航过程中的移动障碍物；而在*跟踪*任务中，化身是跟踪目标。

| 任务 | `--task` | 目标 | 化身角色 |
|------|----------|------|-------------|
| **动态 PointNav** | `avoid` | GPS 坐标 | 移动障碍物 |
| **动态 ImageNav** | `avoid_imagenav` | 目标图像 | 移动障碍物 |
| **动态 ObjectNav** | `avoid_objectnav` | 物体类别 | 移动障碍物 |
| **人体跟踪** | `track` | 跟随行走的化身 | 跟踪目标 |

#### 前置条件

- 安装 **[我们的 habitat-lab fork](https://github.com/RukawaY/habitat-lab-dynamic)**（见[安装 Habitat-Lab](#-安装-habitat-lab可选但推荐)）
- 将 GS 场景、高斯化身、SMPL-X 人体模型以及**动态导航数据**放置到 `data/scene_datasets/gs_scenes/`
- 安装好 `GAMMA` conda 环境（见[准备 GS 资产](#-准备-gs-资产)）

#### 数据布局

<details>
<summary>点击展开：在基础数据集布局之上增加的动态导航专属文件</summary>

```
data/scene_datasets/gs_scenes/
├── configs/
│   ├── ddppo_dynamic_track_gs_{train,eval}.yaml            # 跟踪
│   ├── ddppo_dynamic_avoid_gs_{train,eval}.yaml            # 动态 PointNav
│   ├── ddppo_dynamic_avoid_imagenav_gs_{train,eval}.yaml   # 动态 ImageNav
│   └── ddppo_dynamic_avoid_objectnav_gs_{train,eval}.yaml  # 动态 ObjectNav
└── dynamic_nav/                         # 10 个场景（scene01–scene10），每个一个行走化身
    ├── dynamic_nav.scene_dataset_config.json
    ├── scenes/<scene>.scene_instance.json      # stage + navmesh + gaussian_avatars 关联配置
    ├── stages/<scene>.stage_config.json
    ├── trajectories/<scene>.driver.pkl         # GAMMA 行走轨迹（joint_mats + proxy_capsules）
    ├── episodes/{train,val}/                   # PointNav 格式：1,000 条训练 + 100 条验证
    │                                           #   （avoid / avoid_imagenav / track 共用）
    └── episodes_objectnav/{train,val}/         # ObjectNav 格式：1,000 条训练 + 100 条验证
```

</details>

#### 第 1 步：生成 Episodes

上述 10 个示例场景的动态导航数据已包含在发布数据集中。若要为新的场景或不同的化身/轨迹组合生成数据：

```bash
conda activate habitat-gs

# --scenes 接受任意场景名；--avatars 指定每个场景的化身 id
# （或为所有场景指定同一个 id）。例如复现发布的 10 场景数据：
python scripts_gs/generate_dynamic_nav.py \
    --scenes scene01 scene02 scene03 scene04 scene05 scene06 scene07 scene08 scene09 scene10 \
    --avatars 2 1 6 3 2 1 6 3 4 6

# ObjectNav episodes：将已标注的 ObjectNav episodes 重定向到动态场景
python scripts_gs/generate_dynamic_objectnav.py \
    --scenes scene01 scene02 scene03 scene04 scene05 scene06 scene07 scene08 scene09 scene10
```

#### 第 2 步：训练

```bash
bash scripts_gs/train_dynamic_nav.sh --task avoid           --output output/dyn_pointnav
bash scripts_gs/train_dynamic_nav.sh --task avoid_imagenav  --output output/dyn_imagenav
bash scripts_gs/train_dynamic_nav.sh --task avoid_objectnav --output output/dyn_objectnav
bash scripts_gs/train_dynamic_nav.sh --task track           --output output/dyn_track
```

这些脚本接受与静态流程相同的选项（`--num-envs`、`--num-gpus`、`--total-steps`、`--num-ckpts`、`--pretrained-ckpt`，以及 Hydra override）。

由于跟踪任务对从零开始的 RL 来说很难，我们还额外提供了一个 **DAgger** 训练器，将几何跟随器蒸馏为可部署的跟踪策略：

```bash
python scripts_gs/train_dynamic_nav_dagger.py output/dyn_track_dagger 90000
```

#### 第 3 步：评估

```bash
bash scripts_gs/eval_dynamic_nav.sh --task avoid --ckpt output/dyn_pointnav/checkpoints/latest.pth
# ... avoid_imagenav / avoid_objectnav / track 同理
```

除标准任务指标（避障类：Success、SPL、Distance-to-Goal；跟踪类：`track_rate`、`tracknav_success`）外，四个任务都会报告每个 episode 的化身交互指标：`avatar_proxy_collision_count` 和 `avatar_proxy_intrusion`。

## 🧩 Agent Skills

我们随仓库附带两个 [Agent Skills](skills)，让编程智能体（Claude Code、Codex、OpenClaw 等）无需通读整个仓库就能直接操作 Habitat-GS：

| Skill | 能帮智能体做什么 |
|---|---|
| [`skills/habitat-gs-control`](skills/habitat-gs-control) | 通过 MCP 工具在实时 GS 仿真中与机器人交互操控（加载场景、移动、观察 RGB/深度、运行自主导航循环、导出视频）。与 [HabitatAgent](#-habitatagent) MCP 服务器配套使用。 |
| [`skills/habitat-gs-train`](skills/habitat-gs-train) | 在 Habitat-GS 仿真环境中快速训练和评估导航策略，覆盖 PointNav/ImageNav/ObjectNav 以及 VLN（StreamVLN、Uni-NaVid）的完整「生成 → 训练 → 评估」流程。 |

使用 skill 管理器将它们安装到智能体的工作区：

```bash
tools/manage_habitat_gs_skill.sh install --workspace /path/to/agent/workspace
tools/manage_habitat_gs_skill.sh status  --workspace /path/to/agent/workspace
```

更多细节见 [docs/habitatagent.md](docs/habitatagent.md#agent-skill)。

## 📚 引用

如果 Habitat-GS 对你的研究有帮助，欢迎引用：

```bibtex
@inproceedings{xia2026habitat,
  title={Habitat-gs: A high-fidelity navigation simulator with dynamic gaussian splatting},
  author={Xia, Ziyuan and Xu, Jingyi and Cui, Chong and Yu, Yuanhong and Zhang, Jiazhao and Yan, Qingsong and Ni, Tao and Chen, Junbo and Zhou, Xiaowei and Bao, Hujun and others},
  booktitle={European Conference on Computer Vision},
  pages={306--323},
  year={2026},
  organization={Springer}
}
```
