# This script is the sixth script.
# This handles the perspective transform videos.
# Uses ffmpeg.

import subprocess
from size_runs import *

def warp_vid(in_path, out_path, crop, timestamp_start, timestamp_end):
    vs = crop.split("_")
    cx, cy, cw, ch = [int(round(float(v))) for v in vs[3:7]]
    nquad = []
    for i in range(7, 15, 2):
        nquad.append([float(vs[i]), float(vs[i+1])])
    pts = ""
    for x, y in nquad:
        pts += str(x) + ":" + str(y) + ":"

    persp = f'perspective={pts}'

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

    vf = f"{persp},{pad},{crop},scale=256:240:flags=area,setsar=1:1"

    args = ['ffmpeg', '-i', in_path, '-ss', timestamp_start, '-to', timestamp_end, "-vf", vf, "-vcodec", "libx264", "-crf", "12", out_path]

    print(" ".join(args))
    subprocess.call(args)

process_crop("perspective", warp_vid)
