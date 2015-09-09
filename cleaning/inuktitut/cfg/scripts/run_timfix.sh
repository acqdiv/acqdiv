# /bin/bash

# Causes shell to echo everything it is executing in stdout.
#set -v


# Where do we want timfix.py to put its outputs?
OUT_FOLDER='output'
if [ -n "$1" ]; then
	OUT_FOLDER=$1
fi

# Where is the output folder of the "acqdiv clean"?
OUT_ACQDIV='../../.output/'
if [ -n "$2" ]; then
	OUT_ACQDIV=$2
fi


# Deletes the output of the previous time this was executed
rm -rf $OUT_FOLDER

echo "Will fix %tim tier in the following files from folder: $OUT_ACQDIV"
FILES=$(ls ${OUT_ACQDIV})
echo $FILES
echo "... and output the results in: $OUT_FOLDER"

# Inserts a '\r' in the end of every file
# (Chatter complains when this is not there)
for i in $FILES
do
	echo "Fixing %tim tier in file: ${OUT_FOLDER}/$i"
	./timfix.py ${OUT_ACQDIV}/$i $OUT_FOLDER
done

echo "Finished fixing %tim tier in all files"
echo ""

