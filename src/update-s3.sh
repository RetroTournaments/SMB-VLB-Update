
aws s3 sync vid/ s3://smb-vlb-update/vid --acl public-read --content-disposition attachment --profile mvd
aws s3 sync fm2/ s3://smb-vlb-update/fm2 --acl public-read --content-disposition attachment --profile mvd
