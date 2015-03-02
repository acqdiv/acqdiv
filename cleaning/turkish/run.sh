# Package to clean up Turkish data (.cha) and convert it to .xml
# Steven Moran <steven.moran@uzh.ch>
# November 2014

# Set up data folder
DIRECTORY="cha"
if [ -d "$DIRECTORY" ]; then
rm -R $DIRECTORY
fi
mkdir $DIRECTORY 

# Get all the data
SOURCE="../../corpora/Turkish_KULLD/"
find $SOURCE -type f -exec cp {} $DIRECTORY \;

# hack
rm cha/session-status-2014-09-14.xls
rm cha/.DS_Store

# Convert filenames to something sane
python3 filenames.py cha/

# Convert the files to UTF-8; this initial attempt with iconv didn't work: iconv -f original_charset -t utf-8 originalfile > newfile 
python ../scripts/utf8.py cha

# Clean up the files and make them CHAT conformant
python3 clean.py cha *.txt

echo
echo "Now you should run the chatter program and convert .cha to .xml & have a nice day!"
echo


