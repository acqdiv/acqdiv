#!/bin/bash

prettyprint(){

	DIR=$1
	[[ $DIR = */ ]] || DIR="$DIR/"

	mkdir -p "$DIR"prettyprint/
	for file in "$DIR"*
	do
		if [ ! -d "$file" ]
		then
			TFN="${file%.json}_pp.json"
			NFN=$(basename $TFN)
			python -m json.tool $file > "$DIR"prettyprint/"$NFN"
		fi
	done
}

prettyprint $1
exit
