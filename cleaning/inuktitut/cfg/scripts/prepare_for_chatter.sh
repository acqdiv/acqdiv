# /bin/bash

# Causes shell to echo everything it is executing in stdout.
set -v

./run_acqdiv.sh
./run_timfix.sh

# Where is the output folder of the "acqdiv clean"?
FOLDER='./timfix/'
if [ -n "$1" ]; then
	FOLDER=$1
fi
echo "Folder: $FOLDER"

FILES=$(ls ${FOLDER})
echo $FILES

# Inserts a '\r' in the end of every file
# (Chatter complains when this is not there)
for i in $FILES
do
	echo "PROCESSING FILE: ${FOLDER}/$i"
	echo -e "\r" >> ${FOLDER}/$i
done

