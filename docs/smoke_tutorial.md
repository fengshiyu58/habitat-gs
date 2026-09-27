# Habitat-GS 冒烟测试 + 数据观察 + 代码精读教程

> 目标：自己跑通采集流程 → 亲眼看到采集的数据 → 吃透采集代码。
> 前提：环境已搭好（见 [autodl_setup.md](autodl_setup.md)），`data/scene_datasets/gs_scenes` 下有 scene01 等 4 个场景。
> 所有命令先激活环境：`conda activate /root/autodl-tmp/envs/habitat-gs`

---

## 第 1 步：亲手跑冒烟测试（约 20 分钟）

在 `/root/ws/habitat-gs` 下依次执行。**故意从小参数开始**，观察每个脚本的 stdout：

```bash
# ① PointNav：纯 navmesh 采样，不渲染，秒级完成
python scripts_gs/generate_pointnav_episodes.py --scene scene01 --train-episodes 20 --val-episodes 5

# ② ImageNav：会真实调用 GS 渲染做目标图质检（看 "rejects" 计数）
python scripts_gs/generate_imagenav_episodes.py --scene scene01 --train-episodes 10

# ③ ObjectNav：完整 SAM+CLIP 检测链路（GPU 上约 2-5 分钟），加 --visualize 看检测框
python scripts_gs/generate_objectnav_episodes.py --scene scene01 --train-episodes 5 --visualize
```

**你应该看到：**
- ① `navmesh area=...m² -> 20 episodes (dist: a-bm, mean=cm)`——距离分布是 episode 质量的直观指标
- ② `Done. Total image-quality rejects: N`——N>0 说明质检在真实看图并剔除对着天空/墙角的坏目标
- ③ 末行 `Categories found across all scenes: [...]`——这就是它在 scene01 里"认出"的物体（car/bench/barrier…），`--visualize` 的标注图在 `output_root/objectnav_visualization/scene01/`

**产物落盘位置：**
```
data/scene_datasets/gs_scenes/episodes/
├── pointnav/train/content/scene01.json.gz   ← 每场景一个内容文件
├── pointnav/train/train.json.gz             ← master index（content 文件列表）
├── imagenav/...
└── objectnav/...
```

---

## 第 2 步：亲眼看看采集的数据长什么样

### 2a. 看 JSON 结构（episode 的本体）

```bash
python - <<'EOF'
import gzip, json
d = json.load(gzip.open('data/scene_datasets/gs_scenes/episodes/pointnav/train/content/scene01.json.gz'))
print(json.dumps(d['episodes'][0], indent=1, ensure_ascii=False)[:600])
EOF
```

一条 PointNav episode 就 6 个字段（生成代码见 `generate_pointnav_episodes.py:147-159`）：

| 字段 | 含义 |
|---|---|
| `scene_id` | `gs_scenes/train/scene01/scene01.gs.ply`——**按后缀 `.gs.ply` 触发 GS 渲染管线**（`src/esp/assets/Asset.cpp:18-23`） |
| `start_position` / `start_rotation` | 起点米坐标 + 朝向四元数（只随机偏航） |
| `goals[].position/radius` | 目标点 + 判定成功半径 0.2m |
| `info.geodesic_distance` | 沿 navmesh 的最短路径长度（非直线距离！） |

ObjectNav 不同：**episode 的 `goals` 是空的**，目标存在文件顶层的 `goals_by_category`（Habitat `ObjectNavDatasetV1` 约定，`generate_objectnav_episodes.py:814-821`），每条 goal 还带 `view_points`（从哪些位姿能看到该物体 + IoU）。

### 2b. 把 episode "渲染"出来看 —— `tools_gs/render_episode.py`

AutoDL 没桌面，官方 viewer 跑不了。仓库里已备好一个 headless 工具（本教程配套，已验证），它读取任意一条已生成的 episode，在起点、最短路径中间 4 点、终点各渲一帧：

```bash
python tools_gs/render_episode.py --task pointnav --scene scene01 --ep 1
python tools_gs/render_episode.py --task objectnav --scene scene01 --ep 0 --cat barrier

ls /root/autodl-tmp/ep_vis/pointnav_scene01_train_ep1/
# rgb_00_start.png  rgb_11..14_path.png  rgb_99_at_goal.png   ← RGB
# depth_*.png                                                  ← 深度（0~20m 灰度归一）
```

**验收要点（亲眼确认三件事）：**
1. `rgb_00_start` 应该是照片级真实的场景图（GS 渲染，不是网格贴图；天空发黑正常——重建没拍到天顶）
2. `11→14` 四帧应当像"一路走向目标"的连续视角，且末帧里目标物越来越近
3. stdout 会打印 `geodesic path length = X (episode 记录: Y)`——**X 与 Y 一致**说明 episode 标注的路径距离与 navmesh 自洽（这就是训练时 reward 的依据）
4. 看 PNG 最方便的方式：VS Code 文件树里直接点开，或 AutoDL JupyterLab 里预览

### 2c. ObjectNav 的检测可视化

`--visualize` 产出的图（SAM 分割掩码 + CLIP 类别标在 RGB 上）在：
```
data/scene_datasets/gs_scenes/episodes/objectnav_visualization/scene01/*.jpg
```
抽两张看看 SAM 把哪些像素团成了"car/bench"，比读 100 行代码直观。

---

## 第 3 步：吃透采集代码（按"一条 episode 的一生"读）

### 3.1 PointNav：最短闭环（先读这个，30 分钟）

`scripts_gs/generate_pointnav_episodes.py`：

| 环节 | 位置 | 要点 |
|---|---|---|
| 场景发现 | `discover_scenes :172` | 要求场景目录同时有 `{name}.gs.ply` + `{name}.navmesh`（`:183-185`）——**这就是你自建场景要交付的两个文件** |
| 无渲染 Simulator | `:280-292` | `scene_id="NONE"` + 不建 sensor，只加载 navmesh 做寻路。**寻路和渲染是两套独立子系统**，PointNav 生成根本不需要 GPU |
| 采样起点 | `generate_episodes_for_scene :100` | `pathfinder.get_random_navigable_point()` 随机撒点 |
| 过滤 | `is_compatible_episode :65` | 四条规则：高差≤0.5m（`:75`）、距离 1–30m（`:82`）、测地/欧氏比≤阈值（`:90-92`，排除绕远路的伪样本）、`island_radius≥1.5`（`:94`，排除孤立地块）——**读懂这五个常量，你就懂了什么才算"好数据"** |
| 测地距离 | `_geodesic_distance :55` | `habitat_sim.ShortestPath + pathfinder.find_path`，和你在 viewer 里看到的黄线同一套 |
| 写盘 | `save_episodes :197` | gzip JSON，content/index 两级（Habitat 标准分片格式，允许按场景并行生成） |

### 3.2 ImageNav：多一个"渲染回查"环

`generate_imagenav_episodes.py`：流程与 PointNav 相同，差异是 simulator **带真实 GS 渲染**（`:292-303`，即 2b 工具同款构建法），每个候选目标渲一张 256² 图，`image_quality_ok :70` 用亮度/方差/边缘密度剔掉对墙对地的坏目标。目标图**不落盘**——训练时 `ImageGoalSensor` 按 goal 位姿现场重渲（这是 GS 仿真器特有的设计：数据里只存"位姿"这种极小的信息）。

### 3.3 ObjectNav：感知驱动的采集（核心在 `scan_scene_for_objects :351`）

```
撒 200 点 × 多朝向 (sample_observation_points :326)
  → 每点 GS 渲染 RGB+D (agent.set_state + get_sensor_observations :380-386)
  → SAM 自动分割 (mask_gen.generate :389)
  → 每个 mask 裁图喂 CLIP，与 12 类室外(或 --indoor 10 类室内)文本比相似度，阈值 0.15 (:399-419)
  → 命中则用 depth 把 mask 反投影到 3D (backproject_mask_to_3d :270)   ← RGBD→米制坐标的关键
  → 同一物体的多次检测做 DBSCAN 聚类 (eps=2m :514-526) → 去重/限数/剔除"到处都有的类" (:572/:609/:629)
  → 每个物体记录"从哪些位姿看得见 + 视角 IoU" (build_goals_by_category :689)
  → 再按 PointNav 流程生成"起点→某物体附近"的 episodes
```

### 3.4 渲染核心（看懂 GS 怎么出图即可，不用抠 kernel）

请求链：`sim.get_sensor_observations()` → `Renderer.cpp:96`（dynamic_cast 分流到 GS 路径）→ `GaussianSplattingRenderer`（`src/esp/gfx/GaussianSplattingRenderer.h:93`）→ CUDA 光栅化器：

- **forward.cu**：`preprocessCUDA :153` 把几百万高斯投影到屏幕并按视锥剔除 → **rasterizer_impl.cu** `:76-107` 给每个高斯生成 tile 排序 key → `cub::DeviceRadixSort :189` 基数排序（深度序）→ `renderCUDA :277` 每 16×16 tile 按序 alpha-blend 泼溅
- **depth 是顺带产物**：alpha 混合时累积期望深度（`forward.cu:383-417`），所以 GS 场景有精确米制深度（对比网格光栅化的深度精度差异是论文卖点之一）
- `.gs.ply` 识别从 `Asset.cpp:18-23`（后缀）→ `GaussianSplattingImporter.cpp:288` 解析进显存

### 3.5 自建场景闭环（你的终点，重点读）

`web_tools/navmesh_editor/`：浏览器里看 GS 俯视图、涂可行走区域；服务端 `_nav_worker.py:93-97` 把涂出来的多边形烘焙成代理网格 → `sim.recompute_navmesh()`（Recast 引擎）→ `pathfinder.save_nav_mesh()` 落 `.navmesh`。**3DGS → navmesh → episodes 全链路就此闭合。**

---

## 第 4 步：自测理解（每个都只要一条命令）

1. **距离分布**：`--seed 7` 换种子再生成一次，比较两次 mean 距离；再试着解释为何 mean 在 15–25m 而不是 30m（提示：`:82` 上限 + `:90` 比率过滤会淘汰贴边样本）
2. **navmesh 边界**：用 render_episode 跑 `--ep 99`，看哪条 episode 路径最长/最短，用图验证"绕路"
3. **感知偏差**：objectnav `--visualize` 的图里找一个 CLIP 误检（README 也提醒"可能 mislocalize"——这就是提供手工标注 web 工具的原因）
4. **终极预演**（等你有一个自己的 .gs.ply 时）：navmesh_editor 画区 → 按 README 三段式 JSON 组织 → `--scenes 你的场景` 生成 episodes → render_episode 检查。做完这个，教程目标全部达成。

## 常见故障速查

| 症状 | 去看 |
|---|---|
| Unable to create windowless context | autodl_setup.md 坑 3（10_nvidia.json） |
| sklearn / segment_anything 缺失 | 坑 7 |
| ObjectNav 全是 0 个类别 | SAM/CLIP 权重路径（`~/.cache/sam_checkpoints`, `~/.cache/clip_models`） |
| episode 生成一直 skip | navmesh 未加载：stdout 有 `navmesh NOT loaded`，检查 `.navmesh` 文件名与场景目录名是否严格一致 |
