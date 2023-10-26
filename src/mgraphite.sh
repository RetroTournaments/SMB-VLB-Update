#!/bin/bash

if [ "$#" -lt 1 ]; then
    >&2 echo "give srcid as mgraphite xxxxxxxx"
    exit
fi

/home/matthew/repos/graphite/build/graphite/graphite /home/matthew/repos/rgms/data/roms/SMB.nes /home/matthew/repos/SMB-VLB-Update/vid/$1.mp4 /home/matthew/repos/SMB-VLB-Update/fm2/$1.fm2
rm -f graphite.json
rm -f graphite.log
