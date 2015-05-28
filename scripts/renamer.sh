#!/bin/bash

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
