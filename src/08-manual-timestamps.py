# 
from pathlib import Path
import re


RUNS = "01-runs.csv"
RAW_PATH = Path("../raw/")
TS = "05-timestamps.csv"

known = set()

def valid_timestamp(ts):
    return re.search("^\d\d:\d\d:\d\d$", ts) is not None


with open(TS, "r") as f:
    f.readline()
    for line in f.readlines():
        src_run_id, start, end = line.strip().split(",")
        known.add(src_run_id)

to_add_timestamps = set()

for f in RAW_PATH.glob("*"):
    src_run_id = f.stem
    assert(len(f.stem) == 8)

    if src_run_id not in known:
        to_add_timestamps.add(src_run_id)


with open(RUNS, "r") as f:
    f.readline()
    for line in f.readlines():
        toks = line.strip().split(",")
        src_run_id = toks[0]
        if src_run_id not in to_add_timestamps:
            continue
        url = toks[-1]
        print(src_run_id, ": ", url)
        start = ""
        while not valid_timestamp(start):
            start = input("start 'hh:mm:ss': ")
        end = ""
        while not valid_timestamp(end):
            end = input("end   'hh:mm:ss': ")


        with open(TS, "a") as o:
            o.write(f"{src_run_id},{start},{end}\n")








