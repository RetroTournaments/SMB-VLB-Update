# This script is the fifth script.
# This handles all of the straightforward 'crop' videos.
# Uses ffmpeg.

import subprocess
from pathlib import Path

CROP = "04-crop.csv"
TS = "05-timestamps.csv"
RAW_DIRECTORY = "../raw/"
VID_DIRECTORY = "../vid/"

seen = set()

raw_dir = Path(RAW_DIRECTORY)

vid_dir = Path(VID_DIRECTORY)
vid_dir.mkdir(parents=True, exist_ok=True)
for f in vid_dir.glob("*"):
    src_run_id = f.stem
    assert(len(f.stem) == 8)
    seen.add(f.stem)

timestamps = {}
with open(TS, "r") as f:
    f.readline()
    for line in f.readlines():
        src_run_id, start, end = line.strip().split(",")
        timestamps[src_run_id] = (start, end)


with open(CROP, "r") as f:
    f.readline()

    for line in f.readlines():
        src_run_id, crop = line.strip().split(",")
        if src_run_id in seen:
            continue
        if not crop.startswith("crop"):
            continue

        vs = crop.split("_")
        cx, cy, cw, ch = [int(round(float(v))) for v in vs[3:7]]

        px = 0
        py = 0
        pw = 'iw'
        ph = 'ij'

        if cx < 0:
            pw = f'max(iw + {-cx}\\, {cw})'
            px = -cx
            cx = 0
        else:
            pw = f'max(iw\\, {cx + cw})'

        if cy < 0:
            ph = f'max(ih + {-cy}\\, {ch})'
            py = -cy
            cy = 0
        else:
            ph = f'max(ih\\, {cy + ch})'

        pad = f'pad={pw}:{ph}:{px}:{py}'
        crop = f'crop={cw}:{ch}:{cx}:{cy}'

        vf = f"{pad},{crop},scale=256:240:flags=area,setsar=1:1"

        timestamp_start, timestamp_end = timestamps[src_run_id]

        vp = list(raw_dir.glob(f"{src_run_id}*"))[0]
        subprocess.call(['ffmpeg', '-i', vp, '-ss', timestamp_start, '-to', timestamp_end, "-vf", vf, "-vcodec", "libx264", "-crf", "12", f"{VID_DIRECTORY}{src_run_id}.mp4"])
