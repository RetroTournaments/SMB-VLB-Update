# This script is the third script.
# Unfortunately I need to download all the raw video files, it is ~17GB! 
# Don't worry they are not tracked.

import subprocess
from pathlib import Path

INPUT = "01-runs.csv"
FM2_DIRECTORY = "../fm2/"
RAW_DIRECTORY = "../raw/"

seen = set()

fm2_dir = Path(FM2_DIRECTORY)
for f in fm2_dir.glob("*.fm2"):
    assert(len(f.stem) == 8)
    seen.add(f.stem)

raw_dir = Path(RAW_DIRECTORY)
raw_dir.mkdir(parents=True, exist_ok=True)

for f in raw_dir.glob("*"):
    src_run_id = f.stem
    assert(len(f.stem) == 8)
    seen.add(f.stem)

with open(INPUT, "r") as fin:
    fin.readline()

    for line in fin.readlines():
        vs = line.strip().split(",")
        src_run_id = vs[0]
        url = vs[-1]

        if src_run_id not in seen:
            print(src_run_id)
            subprocess.call(["yt-dlp", url, "-o", f"{RAW_DIRECTORY}/{src_run_id}.%(ext)s"])
            
