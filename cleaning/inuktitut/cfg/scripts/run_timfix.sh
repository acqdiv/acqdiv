# /bin/bash

# Causes shell to echo everything it is executing in stdout.
#set -v

# Where is the output folder of the "acqdiv clean"?
FOLDER='../../.output/'
if [ -n "$1" ]; then
	FOLDER=$1
fi
echo "Folder: $FOLDER"

# We want to create a copy of that folder (we will change those files).
OUT_COPY='output'
if [ -n "$2" ]; then
	OUT_COPY=$2
fi
echo "Copy of the output folder: $OUT_COPY"


# Deletes the output of the previous time this was executed
rm -rf $OUT_COPY ${OUT_COPY}-xml
cp $FOLDER ./$OUT_COPY -R

FILES=$(ls ${OUT_COPY})
echo $FILES

# Inserts a '\r' in the end of every file
# (Chatter complains when this is not there)
for i in $FILES
do
	./timfix.py ${OUT_COPY}/$i
done

