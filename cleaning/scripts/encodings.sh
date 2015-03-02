# Get encoding -- make sure to pass the input directory/* when calling this script:
# sh encodings.sh ../inuktitut/test/*
file $1 > file.log
file -i $1 > file-i.log
chardetect $1 > chardetect.log