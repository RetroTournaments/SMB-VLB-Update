#! /bin/bash
# on error: rclone config reconnect flib: -vv
rclone sync -v "flib:SMB-VLB-UPDATE/Submit a completed fm2 (File responses)/the fm2 (make sure the name is the srcid.fm2) (File responses)" fm2-submissions/
