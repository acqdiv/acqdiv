# /bin/bash

# Causes shell to echo everything it is executing in stdout.
#set -v


# Where will the output folder be?
OUT_FOLDER='output'
if [ -n "$1" ]; then
	OUT_FOLDER=$1
fi

# Where is the output of "acqdiv clean"?
OUT_ACQDIV='../../.output/'
if [ -n "$2" ]; then
	OUT_ACQDIV=$2
fi

# What is the folder where we want to put the output of `check`?
OUT_CHECK='checks'
if [ -n "$3" ]; then
	OUT_CHECK=$3
fi


./run_acqdiv.sh $OUT_ACQDIV $OUT_CHECK
./run_timfix.sh $OUT_FOLDER $OUT_ACQDIV


echo "Will insert a '\r' in the following files in: $OUT_FOLDER"
FILES=$(ls ${OUT_FOLDER})
echo $FILES

# Inserts a '\r' in the end of every file
# (Chatter complains when this is not there)
for i in $FILES
do
	echo "Inserting '\r' to the end of file: ${OUT_FOLDER}/$i"
	echo -e "\r" >> ${OUT_FOLDER}/$i
done

echo "Finished inserting '\r' in all files."
echo ""

