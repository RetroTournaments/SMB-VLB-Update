# this small file provides helpers for do-crop, do-perspective, and do-uncrt

from pathlib import Path

TS = "05-timestamps.csv"
RAW_DIRECTORY = "../raw/"
VID_DIRECTORY = "../vid/"
CROP = "04-crop.csv"

def get_seen():
    seen = set()

    raw_dir = Path(RAW_DIRECTORY)

    vid_dir = Path(VID_DIRECTORY)
    vid_dir.mkdir(parents=True, exist_ok=True)
    for f in vid_dir.glob("*"):
        src_run_id = f.stem
        assert(len(f.stem) == 8)
        seen.add(f.stem)

    return seen

def get_timestamps():
    timestamps = {}
    with open(TS, "r") as f:
        f.readline()
        for line in f.readlines():
            src_run_id, start, end = line.strip().split(",")
            timestamps[src_run_id] = (start, end)

    return timestamps

def process_crop(prefix, func):
    seen = get_seen()
    timestamps = get_timestamps()

    raw_dir = Path(RAW_DIRECTORY)

    with open(CROP, "r") as f:
        f.readline()

        for line in f.readlines():
            src_run_id, crop = line.strip().split(",")
            if src_run_id in seen:
                continue
            if not crop.startswith(prefix):
                continue

            in_path = str(list(raw_dir.glob(f"{src_run_id}*"))[0])
            out_path = f"{VID_DIRECTORY}{src_run_id}.mp4"

            timestamp_start, timestamp_end = timestamps[src_run_id]

            func(in_path, out_path, crop, timestamp_start, timestamp_end)
