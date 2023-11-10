from pathlib import Path
import datetime
from collections import defaultdict
import sqlite3

RUN_CSV = "../src/01-runs.csv"
FM2_DIR = Path("../fm2/")
VID_DIR = Path("../vid/")
RECREATOR_CSV = "../src/recreator.csv"
DB_PATH = Path("./vlb2023.db")
SCHEMA_PATH = Path("./schema.sql")

if DB_PATH.is_file():
    print(DB_PATH, "already exists. remove it first.")
    DB_PATH.unlink()

if not SCHEMA_PATH.is_file():
    print("no schema?")
    exit()

fm2 = set()
for f in FM2_DIR.glob("*.fm2"):
    fm2.add(f.stem)

vids = set()
for v in VID_DIR.glob("*"):
    vids.add(v.stem)


recreators = {}
with open(RECREATOR_CSV, "r") as f:
    for line in f.readlines():
        src_run_id, recreator = line.strip().split(",")
        recreators[src_run_id] = recreator

runs = []
runners = defaultdict(list)

REJECTED_RUNS = set(["z0jvdw4y"])


with open(RUN_CSV, "r") as f:
    f.readline()

    for line in f.readlines():
        src_run_id, _, _, display_name, _, elapsed_ms, platform_fps, _ = line.strip().split(",")

        elapsed_time = datetime.datetime.fromtimestamp(float(elapsed_ms) / 1000).strftime("%M:%S.%f")[1:(len("04:55.222"))]

        run = [src_run_id, display_name, elapsed_time, platform_fps]
        if src_run_id not in REJECTED_RUNS:
            runs.append(run)
            runners[display_name].append(src_run_id)

runs = sorted(runs, key=lambda x: x[2])

for runner, these_runs in runners.items():
    one_recre = False
    for src_run_id in these_runs:
        if src_run_id in fm2:
            one_recre = True
    if not one_recre:
        for src_run_id in these_runs:
            if src_run_id in vids:
                print("STOP AND RECREATE ONE FOR THIS RUNNER: ", runner, these_runs)
                break
already = set()

runs2 = []
for src_run_id, display_name, elapsed_time, platform_fps in runs:
    if display_name in already:
        continue
    if src_run_id not in fm2:
        print("no recreation: ", src_run_id, display_name, elapsed_time)
        pass
    else:
        already.add(display_name)

        if src_run_id in recreators:
            recreator = recreators[src_run_id]
        else:
            recreator = "FlibidyDibidy"

        runs2.append([src_run_id, display_name, elapsed_time, platform_fps, recreator])


db = sqlite3.connect(DB_PATH)
cur = db.cursor()

v = open(SCHEMA_PATH, "r").read()
cur.executescript(v)

for run in runs2:
    cur.execute("INSERT INTO run (src_run_id, runner_alias, elapsed_time, platform_fps) VALUES (?, ?, ?, ?)", run[0:4])
    print(run)
    run_id = cur.lastrowid

    inputs = []
    with open(FM2_DIR / f"{run[0]}.fm2", "r") as f:
        for line in f.readlines():
            if line.startswith("|"):
                v = 0
                for b in range(8):
                    if line[10 - b] != '.':
                        v |= (1 << b)
                inputs.append(v)
    inputs = bytes(inputs[1:])
    print(len(inputs))

    cur.execute("INSERT INTO tas_recreation (run_id, recreator_alias, inputs) VALUES (?, ?, ?)", (run_id, run[-1], inputs))

db.commit()
db.close()

