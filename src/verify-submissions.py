#! python3

from pathlib import Path
import shutil
import subprocess

SUBMIT_DIR = "fm2-submissions/"
FM2_DIR = "fm2/"
VID_DIR = "vid/"

seen = set()
for f in Path(FM2_DIR).glob("*.fm2"):
    assert(len(f.stem) == 8)
    seen.add(f.stem)

for f in Path(SUBMIT_DIR).glob("*.fm2"):
    src_id = f.stem[:8]
    if src_id in seen:
        continue

    print(src_id, f)

    shutil.copy(str(f), FM2_DIR + src_id + ".fm2")
    subprocess.call(["/home/matthew/repos/graphite/build/graphite/graphite", "/home/matthew/repos/rgms/data/roms/SMB.nes",
                    f"/home/matthew/repos/SMB-VLB-Update/vid/{src_id}.mp4", f"/home/matthew/repos/SMB-VLB-Update/fm2/{src_id}.fm2"])


for f in ["graphite.log", "graphite.json"]:
    p = Path(f)
    p.unlink(missing_ok=True)

