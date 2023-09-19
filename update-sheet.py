#! python3
# import overtop of VLB-2023/Data (https://docs.google.com/spreadsheets/d/1_GwGMzxJuHCW60huQASQmNDknZlJMZCWh4LCEjRxUy0/edit)

from itertools import zip_longest
from pathlib import Path

FM2_DIR = "fm2/"
VID_DIR = "vid/"
OUT = "data.csv"

done = []
vids = []

for f in Path(FM2_DIR).glob("*.fm2"):
    assert(len(f.stem) == 8)
    done.append(f.stem)

for f in Path(VID_DIR).glob("*.mp4"):
    assert(len(f.stem) == 8)
    vids.append(f.stem)

with open(OUT, "w") as f:
    f.write("DONE,VIDEO_READY\n")
    for fm2, vid in zip_longest(done, vids):
        f.write(f"{fm2},{vid}\n")



