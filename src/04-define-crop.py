# This script is the fourth script.
# After the raw videos are downloaded it is necessary to define where the game footage is for each video.
# For this I used 'carbon' from the graphite repository in the following fashion.
# I did them all myself because I didn't want to get other people set up doing it. Yay.

import subprocess
from pathlib import Path

CARBON_PATH = "/home/matthew/repos/graphite/build/carbon/carbon"
RAW_DIRECTORY = "../raw/"
OUTPUT = "04-crop.csv"

lines = []
seen = set()

try:
    with open(OUTPUT, "r") as f:
        f.readline()
        for line in f.readlines():
            lines.append(line)
            src_run_id, _ = line.strip().split(",")
            seen.add(src_run_id)
except FileNotFoundError:
    with open(OUTPUT, "w") as f:
        f.write("src_run_id,filter\n")
    pass

with open(OUTPUT, "a") as fout:
    raw_dir = Path(RAW_DIRECTORY)
    for f in raw_dir.glob("*"):
        if len(f.stem) != 8:
            continue

        if f.stem not in seen:
            subprocess.call([CARBON_PATH, f, "filter.txt"])
            with open("filter.txt", "r") as flt:
                fltr = flt.read().strip()

            if fltr.startswith("none"):
                break

            fout.write(f"{f.stem},{fltr}\n")

for f in ["filter.txt", "imgui.ini", "carbon.log"]:
    p = Path(f)
    p.unlink(missing_ok=True)

