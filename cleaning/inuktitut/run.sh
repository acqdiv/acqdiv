# Inuktitut clean up script
# =========================

# set up data
DIRECTORY="cha"
if [ -d "$DIRECTORY" ]; then
# echo "rm -R " $DIRECTORY
rm -R $DIRECTORY
fi

# echo "mkdir inuktitut/cha"
mkdir $DIRECTORY

# echo "copy all files into one directory"
SOURCE="../../corpora/Inuktitut/cha/"
find $SOURCE -type f -exec cp {} cha \;

# to double check that all the files are copied
# find ../../../Corpora/Inuktitut/cha -name '*.NAC' -or -name '*.XXS' -or -name '*.XXX' -or -name '*.MAY' | wc -l

# change filenames
python filenames.py cha/

# convert to utf-8 - this takes a bit of time
python ../scripts/utf8.py cha/

# call the cleaners
python3 clean.py cha *.txt

