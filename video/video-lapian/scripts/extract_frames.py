#!/usr/bin/env python3
"""
Extract evenly-spaced frames from a video and build labeled montage grids.

Why this exists: doing a 拉片 (shot-by-shot teardown) means actually LOOKING at
every beat of the video. Reading 60+ individual frames is slow and burns tool
calls. Instead we sample frames at a fixed interval, burn a timestamp label onto
each, and tile them into a few montage grids. You then Read the montages (one
image covers ~12 frames) to review the whole film fast, and Read individual
full-res frames only where you need to read fine UI/spec text.

Uses OpenCV (cv2) so it works WITHOUT ffmpeg installed. Audio is not extracted
(cv2 can't) — the caller must treat audio as an inference, not a transcript.

Usage:
    python3 extract_frames.py --video path/to/vid.mp4 --out path/to/workdir --step 0.5

Outputs, under --out:
    frames/f_<TTTTT.T>.png   one full-res frame per sample (e.g. f_007.5.png)
    montage_<N>.png          4x3 grids of labeled frames

Pick --step by duration (see SKILL.md): ~0.5s for <=60s films, ~1.0-1.5s for
2-3 min films, so you end up with a manageable number of montages.
"""
import argparse
import os
import sys

try:
    import cv2
    import numpy as np
except ImportError:
    sys.exit("Missing deps. Run: pip3 install opencv-python-headless numpy")


def label(img, txt):
    """Burn a yellow timestamp chip in the top-left so montage cells are identifiable."""
    img = img.copy()
    cv2.rectangle(img, (0, 0), (170, 40), (0, 0, 0), -1)
    cv2.putText(img, txt, (6, 29), cv2.FONT_HERSHEY_SIMPLEX, 0.95,
                (0, 255, 255), 2, cv2.LINE_AA)
    return img


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", required=True, help="path to the video file")
    ap.add_argument("--out", required=True, help="output working directory")
    ap.add_argument("--step", type=float, default=0.5,
                    help="seconds between sampled frames (default 0.5)")
    ap.add_argument("--cols", type=int, default=4, help="montage columns")
    ap.add_argument("--rows", type=int, default=3, help="montage rows")
    args = ap.parse_args()

    cap = cv2.VideoCapture(args.video)
    if not cap.isOpened():
        sys.exit(f"Could not open video: {args.video}")

    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    nframes = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    dur = nframes / fps if fps else 0
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(f"video: fps={fps:.2f} dur={dur:.1f}s res={w}x{h}")

    frames_dir = os.path.join(args.out, "frames")
    os.makedirs(frames_dir, exist_ok=True)

    frames = []
    t = 0.0
    while t < dur:
        cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000)
        ok, fr = cap.read()
        if not ok:
            break
        cv2.imwrite(os.path.join(frames_dir, f"f_{t:05.1f}.png"), fr)
        frames.append((t, fr.copy()))
        t = round(t + args.step, 2)
    print(f"extracted {len(frames)} frames at {args.step}s step -> {frames_dir}")

    per = args.cols * args.rows
    mi = 0
    for i in range(0, len(frames), per):
        chunk = frames[i:i + per]
        canvas = np.full((h * args.rows, w * args.cols, 3), 255, dtype=np.uint8)
        for j, (tt, fr) in enumerate(chunk):
            r, c = divmod(j, args.cols)
            canvas[r * h:(r + 1) * h, c * w:(c + 1) * w] = label(fr, f"{tt:.1f}s")
        out = os.path.join(args.out, f"montage_{mi}.png")
        cv2.imwrite(out, canvas)
        print(f"  {out}: {chunk[0][0]:.1f}-{chunk[-1][0]:.1f}s")
        mi += 1
    print(f"{mi} montages written to {args.out}")


if __name__ == "__main__":
    main()
