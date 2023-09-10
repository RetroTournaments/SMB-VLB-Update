# This script is the seventh script.
# This handles those nasty recordings that are of a curved CRT.
# Uses uncrt from the graphite directory, and ffmpeg

import subprocess
from size_runs import *

VCODEC = " -vcodec libx264 -crf 12 "
UNCRT_PATH = "/home/matthew/repos/graphite/build/rgmvideo/uncrt"

def uncrt_vid(in_path, out_path, crop, timestamp_start, timestamp_end):
    vs = crop.split("_")

    npatch = []
    for i in range(15, 15 + 16 * 2, 2):
        npatch.append([float(vs[i]), float(vs[i+1])])

    pts = ""
    for x, y in npatch:
        pts += str(x) + ":" + str(y) + ":"

    src_run_id = "xxxxxxxx"
    vp = in_path

    frames_dir = f"{src_run_id}_frames/"
    print(f'mkdir {frames_dir}')
    print(f'ffmpeg -i {vp} -ss {timestamp_start} -to {timestamp_end} {frames_dir}%06d.png')
    print(f'ffmpeg -i {vp} -ss {timestamp_start} -to {timestamp_end} -vn -acodec copy {src_run_id}_audio.mkv')
    print(f'{UNCRT_PATH} --mesh "{pts}" --inplace --directory {frames_dir}')
    print(f'FPS=$(ffprobe -v 0 -of csv=p=0 -select_streams v:0 -show_entries stream=r_frame_rate {vp})')
    print(f'echo "{src_run_id}: $FPS"')
    print(f'ffmpeg -r $FPS -f image2 -i {frames_dir}%06d.png -i {src_run_id}_audio.mkv {VCODEC} {out_path}')
    print(f'rm -rf {frames_dir}')
    print(f'rm -f {src_run_id}_audio.mkv')

process_crop("uncrt", uncrt_vid)
