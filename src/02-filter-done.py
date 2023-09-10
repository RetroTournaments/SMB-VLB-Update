# This script is the second script.
# Because some of the runs are already done (their fm2 files are already in the repo) the timestamps and video information do not need to be defined.
# This filters 01-runs.csv and creates 02-to-crop.csv, which goes to the google sheet and discord for manual verification and time stamp definition.

INPUT = "01-runs.csv"
OUTPUT = "02-to-crop.csv"
FM2_DIRECTORY = "../fm2/"

from pathlib import Path

seen = set()

fm2_dir = Path(FM2_DIRECTORY)
for f in fm2_dir.glob("*.fm2"):
    assert(len(f.stem) == 8)
    seen.add(f.stem)

with open(OUTPUT, "w") as fout:
    with open(INPUT, "r") as fin:
        fout.write(fin.readline())

        for line in fin.readlines():
            srcid = line.split(",")[0]
            if srcid not in seen:
                fout.write(line)

