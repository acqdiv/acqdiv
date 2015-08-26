# /bin/bash

# Causes shell to echo everything it is executing in stdout.
#set -v

# Runs the cleaner
acqdiv --corpora inuktitut clean

# Now, we want to run check in each one of the files.
# We suppose the output folder is in ".output". If path was passed as parameter,
# we use that path.
FOLDER='../../.output/'
if [ -n "$1" ]; then
	FOLDER=$1
fi

# Gets all the files from that output folder.
FILES=$(ls ${FOLDER})
echo $FILES

# Where should the output of "check" be?
CHECK_OUT='checks'
if [ -n "$2" ]; then
	CHECK_OUT=$2
fi

# Deletes the output of the previous time this was executed
rm -rf $CHECK_OUT
mkdir $CHECK_OUT

# For each output file, we run check and put its output in a file named as
# <output_file_name>_check.txt
for i in $FILES
do
	check ${FOLDER}/$i > ${CHECK_OUT}/$i\_check.txt
done

