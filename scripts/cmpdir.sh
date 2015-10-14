#!/bin/bash
# script to check if all files in a folder have a correspondence of the form $name.$ext in the folder
# to use: cmpdir.sh (folder to be compared to) (folder to compare) (file extension the target files should have)
# for instance: ./cmpdir.sh Russian/toolbox Russian/imdi imdi

if [[ $# = 3 ]]
then
	BASE=$1
	HEAD=$2
	EXT=$3


	[[ "$BASE" = */ ]] || BASE="$BASE/" 
	[[ "$HEAD" = */ ]] || HEAD="$HEAD/"

	for file in "$BASE"*
	do
		bfn=$(basename $file)
		if [[ -e "$HEAD"${bfn%.*}."$EXT" ]]
		then
			:
		else
			echo "$file"
		fi
	done
else
	echo "Usage: cmpdir.sh BASE_DIR TARGET_DIR EXTENSION"
fi
