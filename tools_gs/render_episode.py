#!/usr/bin/env python3
"""
Headless 渲染已生成 episodes 的起始/路径/目标视角，用于肉眼检查采集到的数据。

AutoDL 无桌面，examples/gaussian_viewer.py 跑不了；本脚本用与
scripts_gs/generate_imagenav_episodes.py 相同的 Simulator 构建方式做单帧渲染。

用法示例：
  # 看 pointnav 第 0 条 episode：起始视角 + 沿最短路径的中间帧 + 终点回望
  python tools_gs/render_episode.py --task pointnav --scene scene01 --split train --ep 0

  # objectnav：额外打印目标物体类别（goals 里的元信息）
  python tools_gs/render_episode.py --task objectnav --scene scene01 --ep 0

输出：/root/autodl-tmp/ep_vis/{task}_{scene}_ep{n}/ 下的 rgb_*.png / depth_*.png
"""
import argparse
import gzip
import json
import math
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SCENES_ROOT = ROOT / "data" / "scene_datasets" / "gs_scenes"


def load_episode(content_path: Path, ep_index: int | None, ep_id: str | None):
    with gzip.open(content_path, "rt") as f:
        data = json.load(f)
    eps = data["episodes"] if isinstance(data, dict) else data
    ep = (next(e for e in eps if str(e["episode_id"]) == str(ep_id))
          if ep_id is not None else eps[ep_index])
    return ep, data


def resolve_goal(ep, data, cat=None):
    """pointnav/imagenav: goals[0]；objectnav: goals 为空，取 goals_by_category。"""
    if ep.get("goals"):
        return ep["goals"][0]["position"], None
    gbc = data.get("goals_by_category") or {}
    if not gbc:
        raise SystemExit("episode 与 goals_by_category 都没有目标")
    category = cat or sorted(gbc)[0]
    g = gbc[category][0]
    return g["position"], category


def render_views(scene, split, ep, goal, out_dir: Path, num_path_frames=4, wh=(480, 640)):
    import habitat_sim
    from habitat_sim.utils.settings import make_cfg, default_sim_settings

    out_dir.mkdir(parents=True, exist_ok=True)
    settings = dict(default_sim_settings)
    settings["scene"] = str(SCENES_ROOT / split / scene / f"{scene}.gs.ply")
    settings["scene_dataset_config_file"] = str(
        SCENES_ROOT / f"{split}.scene_dataset_config.json"
    )
    settings["default_agent_navmesh"] = False
    settings["enable_physics"] = False
    settings["height"], settings["width"] = wh
    settings["hfov"] = 79
    settings["depth_sensor"] = True

    sim = habitat_sim.Simulator(make_cfg(settings))
    rgb_uuid = depth_uuid = None
    for u in sim._sensors:
        if "color" in u or "rgb" in u:
            rgb_uuid = u
        if "depth" in u:
            depth_uuid = u
    agent = sim.get_agent(0)

    def shoot(pos, look_at=None, yaw=None, tag="view"):
        st = agent.get_state()
        st.position = np.array(pos, dtype=np.float32)
        if look_at is not None:
            dx, dz = look_at[0] - pos[0], look_at[2] - pos[2]
            yaw = math.atan2(-dx, -dz)
        if yaw is not None:
            q = habitat_sim.utils.common.quat_from_angle_axis(
                float(yaw), np.array([0.0, 1.0, 0.0], dtype=np.float64))
            st.rotation = [q.w, q.x, q.y, q.z] if hasattr(q, "w") else q
        else:
            st.rotation = ep["start_rotation"]
        agent.set_state(st, reset_sensors=True)
        obs = sim.get_sensor_observations()
        rgb = obs[rgb_uuid][:, :, :3].astype(np.uint8)
        dep = obs[depth_uuid]
        dep = dep[:, :, 0] if dep.ndim == 3 else dep
        Image.fromarray(rgb).save(out_dir / f"rgb_{tag}.png")
        d = np.clip(dep, 0, 20) / 20.0
        Image.fromarray((d * 255).astype(np.uint8)).save(out_dir / f"depth_{tag}.png")
        return rgb

    start = ep["start_position"]
    shoot(start, tag="00_start")

    # 最短路径中间帧（顺便验证 navmesh 与 episode 的自洽性）
    path = habitat_sim.ShortestPath()
    path.requested_start = np.array(start, dtype=np.float64)
    path.requested_end = np.array(goal, dtype=np.float64)
    if sim.pathfinder.find_path(path):
        pts = path.points
        print(f"geodesic path length = {path.geodesic_distance:.2f} m "
              f"(episode 记录: {ep.get('info', {}).get('geodesic_distance', float('nan')):.2f})")
        n = len(pts)
        for i in range(1, num_path_frames + 1):
            p = pts[int(i * (n - 1) / (num_path_frames + 1))]
            shoot(p, look_at=goal, tag=f"1{i}_path")
        shoot(goal, yaw=0.0, tag="99_at_goal")   # 到达终点后的视角
    sim.close()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--task", required=True, help="pointnav | imagenav | objectnav | vln")
    ap.add_argument("--scene", required=True)
    ap.add_argument("--split", default="train")
    ap.add_argument("--ep", type=int, default=0, help="episode 序号（content 文件内）")
    ap.add_argument("--cat", default=None, help="objectnav 类别名（默认取第一个类别）")
    ap.add_argument("--out", default="/root/autodl-tmp/ep_vis")
    args = ap.parse_args()

    content = SCENES_ROOT / "episodes" / args.task / args.split / "content" / f"{args.scene}.json.gz"
    if not content.exists():
        # 有的任务不分 content 子目录
        alt = SCENES_ROOT / "episodes" / args.task / args.split / f"{args.scene}.json.gz"
        content = alt
    ep, data = load_episode(content, args.ep, None)
    print(f"scene_id: {ep['scene_id']}")
    print(f"start_position: {np.round(ep['start_position'], 2).tolist()}")
    goal, category = resolve_goal(ep, data, getattr(args, "cat", None))
    if category:
        print(f"objectnav category: {category} @ goal position (goals_by_category)")
    for g in ep.get("goals", []):
        extra = {k: v for k, v in g.items() if k not in ("position", "radius")}
        print(f"goal @ {np.round(g['position'], 2).tolist()} radius={g.get('radius')} {extra if extra else ''}")
    out = Path(args.out) / f"{args.task}_{args.scene}_{args.split}_ep{args.ep}"
    render_views(args.scene, args.split, ep, goal, out)
    print(f"images -> {out}")


if __name__ == "__main__":
    main()
