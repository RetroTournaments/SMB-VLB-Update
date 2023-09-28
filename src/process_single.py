#! python3
# process a single youtube video out of system as some people ask for.
import sys
import re
import subprocess
from pathlib import Path

CARBON_PATH = "/home/matthew/repos/graphite/build/carbon/carbon"

def valid_timestamp(ts):
    return re.search("^\d\d:\d\d:\d\d$", ts) is not None

if __name__ == '__main__':
    argv = sys.argv[1:]
    n = len(argv)
    if n < 2 or n > 4:
        print("usage: process_single.py src_run_id url [timestamp_start] [timestamp_end]")
        exit()

    src_run_id, url = argv[0:2]
    if len(src_run_id) != 8:
        print(f"error: len(src_run_id) != 8, '{src_run_id}'")
        exit()

    start = ""
    end = ""

    if n >= 3:
        start = argv[2]
    if n >= 4:
        end = argv[3]

    while not valid_timestamp(start):
        start = input("start 'hh:mm:ss': ")
    while not valid_timestamp(end):
        end = input("end   'hh:mm:ss': ")


    print(f"./process_single.py {src_run_id} '{url}' {start} {end}")

    subprocess.call(["yt-dlp", url, "-o", f"{src_run_id}_raw.%(ext)s"])
    f = list(Path(".").glob(f"{src_run_id}_raw*"))[0]
    subprocess.call([CARBON_PATH, f, "filter.txt"])
    with open("filter.txt", "r") as flt:
        crop = flt.read().strip()

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

    args = ['ffmpeg', '-i', str(f), '-ss', start, '-to', end, "-vf", vf, "-vcodec", "libx264", "-crf", "12", f"{src_run_id}.mp4"]

    print(" ".join(args))
    subprocess.call(args)
    




    


