#!/bin/bash
# Bulk rename files to FOLDERNAME_FILENAME.XXX
# Intended for renaming the Indonesian files or similar things
# usage: $ ./renamer.sh one/ or/ more/ directories/

while [[ $# > 0 ]]
do

	DIR=$1
	[[ "$DIR" = */ ]] || DIR="$DIR/" 

	echo "Entering directory $(basename $DIR)"

	for file in "$DIR"*
	do
		mv $file "$DIR"$(basename $DIR)"_"$(basename $file)
	done

	shift
done
exit
