#!/bin/bash

prettyprint(){

	DIR=$1
	RECURSIVE=$2
	VERBOSITY=$3
	[[ $DIR = */ ]] || DIR="$DIR/"

	exjson=0

	for file in "$DIR"*.json
	do
		exjson=1
		break
	done

	if [ $exjson -eq 1 ]
	then
		mkdir -p "$DIR"prettyprint/
	fi

	for file in "$DIR"*
	do
		if [ $VERBOSITY -eq 1 ]
		then
			echo "$file"
		fi

		if [[ -f "$file" && "$file" == *.json ]]
		then
			TFN="${file%.json}_pp.json"
			NFN=$(basename $TFN)
			if [ $VERBOSITY -eq -1 ]
			then
				python -m json.tool $file > "$DIR"prettyprint/"$NFN" 2>/dev/null
			else
				python -m json.tool $file > "$DIR"prettyprint/"$NFN"
			fi
		elif [[ $RECURSIVE -eq 1 && -d "$file" && "$file" != *prettyprint ]]
		then
			if [ $VERBOSITY -ne -1 ]
			then
				echo "Entering directory $file"
			fi
			prettyprint $file $RECURSIVE $VERBOSITY
		fi
	done
}

RECURSIVE=0
VERBOSITY=0

if [[ ! $# > 0 ]]
then
	echo "Usage: prettyprinter.sh -r|--recursive -v|--verbose -q|--quiet DIRECTORY"
	exit 1
fi

while [[ $# > 1 ]]
do
	key="$1"

	case $key in
		-r|--recursive)
			RECURSIVE=1
			shift
			;;
		-v|--verbose)
			VERBOSITY=1
			shift
			;;
		-q|--quiet)
			VERBOSITY=-1
			shift
			;;
		-rv|-vr)
			RECURSIVE=1
			VERBOSITY=1
			shift
			;;
		-rq|-qr)
			RECURSIVE=1
			VERBOSITY=-1
			shift
			;;
		*)
			echo "Invalid options: $key"
			exit 1
			;;
	esac
done

DIR=$1
echo "Processing..."
prettyprint $DIR $RECURSIVE $VERBOSITY
echo "Done."
exit
