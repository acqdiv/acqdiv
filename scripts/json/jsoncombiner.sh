#!/bin/bash

combinejson() {
	DIR=$1
	OUTDIR=$2
	RECURSIVE=$3

	[[ $DIR = */ ]] || DIR="$DIR/"
	[[ $OUTDIR = */ ]] || OUTDIR="$DIR/"

	echo "target: $DIR"
	echo "out: $OUTDIR"
	echo "r: $RECURSIVE"

	if [ $RECURSIVE -eq 1 ]
	then
		for file in "$DIR"*
		do
			if [[ -d $file && $file != "*./" && $file != "$DIR" ]]
			then
				cat "$file"/*.json > "$OUTDIR"$(basename $file).json
			fi
		done
	else
		cat "$DIR"*.json > "$OUTDIR"$(basename $DIR).json
	fi
}

RECURSIVE=0
QUIET=0

while [[ $# > 2 ]]
do
	key=$1	
	case $key in
		-r|--recursive)
			RECURSIVE=1
			shift
			;;
		-q|--quiet)
			QUIET=1
			shift
			;;
		-rq|-qr)
			RECURSIVE=1
			QUIET=1
			shift
			;;
		*)
			echo "Invalid options: $key"
			exit 1
			;;
	esac
done

DIR=$1
OUTDIR=$2

if [[ $QUIET -ne 1 ]]
then
	echo "Processing..."
	combinejson $DIR $OUTDIR $RECURSIVE
	echo "Done."
else
	combinejson $DIR $OUTDIR $RECURSIVE 2> /dev/null
fi
exit
