# This script is the first script.
# It uses srcomapi (https://github.com/blha303/srcomapi) to scrape speedrun.com and identify all of the runs that still need fm2 files.
# To install srcomapi follow the directions at the above link.

import srcomapi
import srcomapi.datatypes as dt
from pathlib import Path

TIME_CUTOFF_MS = 300000
FM2_DIRECTORY = "../fm2/"

api = srcomapi.SpeedrunCom()
smb = api.search(srcomapi.datatypes.Game, {"name": "super mario bros."})[0]
anyp = smb.categories[0]

lb = dt.Leaderboard(api, 
        data=api.get("leaderboards/{}/category/{}?embed=variables".format(smb.id, anyp.id)))

already_done = set()
fm2_dir = Path(FM2_DIRECTORY)
for f in fm2_dir.glob("*.fm2"):
    assert(len(f.stem) == 8)
    already_done.add(f.stem)

under_time_cutoff = 0
todo = 0
done = 0

for r in lb.runs:
    srcrun = r["run"]
    srcid = srcrun.id
    elapsed_ms = srcrun.times["primary_t"] * 1000

    if elapsed_ms <= TIME_CUTOFF_MS:
        under_time_cutoff += 1

        if srcid not in already_done:
            todo += 1
        else:
            done += 1

print("under_time_cutoff: ", under_time_cutoff)
print("todo: ", todo)
print("done: ", done)


