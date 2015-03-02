# Yuacatec

# set up data
DIRECTORY="cha"
if [ -d "$DIRECTORY" ]; then
# echo "rm -R " $DIRECTORY
rm -R $DIRECTORY
fi

# echo "mkdir cha"
mkdir $DIRECTORY

# echo "copy all files into one directory"
SOURCE="../../corpora/Yucatec/cha/"
find $SOURCE -type f -exec cp {} cha \;

# get report of file encodings
# file cha/* > file.log-after
# file cha/* > file-i.log-after
# chardetect cha/* > chardetect.log-after

# change filenames - for Yucatec strip the ".txt"
python filenames.py cha/

# md5.py in scripts/ directory can be used to identify duplicate files

# convert to utf-8 - this takes a bit of time
python ../scripts/utf8.py cha/

# get the unigram models
# 1. concatenate all the files together
# 2. run create_profiles.py
# 3. run add_unicode_info.py
# ugh

# call the cleaners
python3 clean.py cha *.txt



