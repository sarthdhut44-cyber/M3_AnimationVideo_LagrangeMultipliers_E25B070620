"""Parallel 1080p animation renderer that compiles all 19 beats and muxes audio into ../_Video.mp4."""

import concurrent.futures
import json
import os
os.environ.setdefault("MPLCONFIGDIR", "/tmp/mpl_cache")
import subprocess
import time
from typing import Callable, Dict, Tuple

import matplotlib.pyplot as plt

from scenes_part1 import (
    render_s1_constrained_hook,
    render_s1_title,
    render_s1_unconstrained,
    render_s2_definitions,
    render_s2_goal,
    render_s2_theorem,
    render_s3_contours_2d,
    render_s3_crossing,
    render_s3_slice3d,
    render_s3_tangency,
)
from scenes_part2 import (
    render_s4_candidates,
    render_s4_evaluate,
    render_s4_setup,
    render_s4_solve,
    render_s4_system,
    render_s5_geometry,
    render_s5_lambda_meaning,
    render_s6_credits,
    render_s6_summary,
)
from theme import HEIGHT, WIDTH, configure_matplotlib, figure_to_rgb_bytes


RENDERERS: Dict[str, Callable[[float, float], plt.Figure]] = {
    "s1_title": render_s1_title,
    "s1_unconstrained": render_s1_unconstrained,
    "s1_constrained_hook": render_s1_constrained_hook,
    "s2_goal": render_s2_goal,
    "s2_definitions": render_s2_definitions,
    "s2_theorem": render_s2_theorem,
    "s3_slice3d": render_s3_slice3d,
    "s3_contours_2d": render_s3_contours_2d,
    "s3_crossing": render_s3_crossing,
    "s3_tangency": render_s3_tangency,
    "s4_setup": render_s4_setup,
    "s4_system": render_s4_system,
    "s4_solve": render_s4_solve,
    "s4_candidates": render_s4_candidates,
    "s4_evaluate": render_s4_evaluate,
    "s5_geometry": render_s5_geometry,
    "s5_lambda_meaning": render_s5_lambda_meaning,
    "s6_summary": render_s6_summary,
    "s6_credits": render_s6_credits,
}


def render_beat_segment(args: Tuple[Dict, int, float, str, str, int]) -> str:
    beat_info, start_frame, total_frames, seg_dir, preview_dir, fps = args
    configure_matplotlib()

    idx = beat_info["index"]
    beat_id = beat_info["beat_id"]
    n_frames = beat_info["frames"]
    render_fn = RENDERERS[beat_id]

    seg_path = os.path.join(seg_dir, f"{idx:02d}_{beat_id}.mp4")
    cmd = [
        "ffmpeg",
        "-y",
        "-loglevel",
        "error",
        "-f",
        "rawvideo",
        "-vcodec",
        "rawvideo",
        "-pix_fmt",
        "rgb24",
        "-s",
        f"{WIDTH}x{HEIGHT}",
        "-r",
        str(fps),
        "-i",
        "-",
        "-an",
        "-c:v",
        "libx264",
        "-preset",
        "medium",
        "-crf",
        "18",
        "-pix_fmt",
        "yuv420p",
        seg_path,
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    assert proc.stdin is not None

    preview_frame = int(round(0.88 * max(1, n_frames - 1)))
    try:
        for f_i in range(n_frames):
            p = f_i / float(max(1, n_frames - 1))
            gp = (start_frame + f_i) / float(max(1, total_frames - 1))
            fig = render_fn(p, gp)
            if f_i == preview_frame:
                fig.savefig(os.path.join(preview_dir, f"{idx:02d}_{beat_id}.png"), dpi=100)
            raw = figure_to_rgb_bytes(fig)
            plt.close(fig)
            proc.stdin.write(raw)
        proc.stdin.close()
    finally:
        ret = proc.wait()
        if ret != 0:
            raise RuntimeError(f"ffmpeg failed for beat {beat_id} with exit code {ret}")

    return seg_path


def main() -> None:
    t0 = time.time()
    code_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(code_dir)
    audio_dir = os.path.join(code_dir, "build_audio")
    seg_dir = os.path.join(code_dir, "build_segments")
    preview_dir = os.path.join(code_dir, "build_previews")
    os.makedirs(seg_dir, exist_ok=True)
    os.makedirs(preview_dir, exist_ok=True)

    with open(os.path.join(audio_dir, "timings.json"), "r", encoding="utf-8") as f:
        manifest = json.load(f)

    fps = manifest["fps"]
    total_frames = manifest["total_frames"]
    beats = manifest["beats"]

    tasks = []
    frame_cursor = 0
    for b in beats:
        tasks.append((b, frame_cursor, float(total_frames), seg_dir, preview_dir, fps))
        frame_cursor += b["frames"]

    workers = min(len(tasks), max(2, (os.cpu_count() or 4) - 1))
    print(f"Rendering {len(tasks)} beat segments ({total_frames} frames @ {fps}fps) using {workers} workers...")

    seg_paths = []
    with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as ex:
        for idx, seg_path in enumerate(ex.map(render_beat_segment, tasks), start=1):
            print(f"  Completed [{idx}/{len(tasks)}] -> {os.path.basename(seg_path)}")
            seg_paths.append(seg_path)

    concat_txt = os.path.join(seg_dir, "concat.txt")
    with open(concat_txt, "w", encoding="utf-8") as f:
        for p in seg_paths:
            f.write(f"file '{p}'\n")

    video_only = os.path.join(seg_dir, "video_only.mp4")
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-loglevel",
            "error",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            concat_txt,
            "-c",
            "copy",
            video_only,
        ],
        check=True,
    )

    final_mp4 = os.path.join(repo_root, "_Video.mp4")
    final_wav = os.path.join(audio_dir, "final_audio.wav")
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-loglevel",
            "error",
            "-i",
            video_only,
            "-i",
            final_wav,
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-shortest",
            "-movflags",
            "+faststart",
            final_mp4,
        ],
        check=True,
    )

    elapsed = time.time() - t0
    print(f"Successfully built {final_mp4} in {elapsed:.1f}s!")


if __name__ == "__main__":
    main()
