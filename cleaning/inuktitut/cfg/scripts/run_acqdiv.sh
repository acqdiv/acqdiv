# /bin/bash

# Causes shell to echo everything it is executing in stdout.
#set -v

# Runs the cleaner
acqdiv --corpora inuktitut clean

# Now, we want to run check in each one of the files.
# We suppose the output folder is in "../../.output", unless it was passed as
# parameter
OUT_ACQDIV='../../.output/'
if [ -n "$1" ]; then
	OUT_ACQDIV=$1
fi

# Where should the output of "check" be?
OUT_CHECK='checks'
if [ -n "$2" ]; then
	OUT_CHECK=$2
fi

# Deletes the output of the previous time this was executed
rm -rf $OUT_CHECK

command -v check >/dev/null 2>&1 || {
	echo >&2 "WARNING: Couldn't find 'check'."
	exit 0
}

mkdir $OUT_CHECK

# Gets all the files from $OUT_ACQDIV
FILES=$(ls ${OUT_ACQDIV})
echo "Will run 'check' in the following files:"
echo $FILES

# For each output file, we run check and put its output in a file named as
# <output_file_name>_check.txt
for i in $FILES
do
	echo "Running check in: ${OUT_FOLDER}/$i"
	check ${OUT_ACQDIV}/$i > ${OUT_CHECK}/$i\_check.txt 2> /dev/null
done

echo "Finished running check in all files"
echo ""

