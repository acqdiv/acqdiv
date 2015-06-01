#!/bin/bash

combinejson() {
	DIR=$1
	OUTDIR=$2
	RECURSIVE=$3

	[[ $DIR = */ ]] || DIR="$DIR/"
	[[ $OUTDIR = */ ]] || OUTDIR="$OUTDIR/"

	echo "target: $DIR"
	echo "out: $OUTDIR"
	echo "r: $RECURSIVE"

	if [ $RECURSIVE -eq 1 ]
	then
		for sub in "$DIR"*
		do
			if [[ -d $sub && $sub != "*./" && $sub != "$DIR" ]]
			then
				OUT="$OUTDIR"$(basename $sub).json
				echo '{"metadata": [' > "$OUT"
				for file in "$sub"/*.json
				do
					cat "$file" >> "$OUT"
					echo "," >> "$OUT"
				done
				sed -i '$s/,$//' "$OUT"
				echo ']}' >> "$OUT"
				ed -s "$OUT" <<< $'1,$j\nwq'
			fi
		done
	else
		OUT="$OUTDIR"$(basename $DIR)".json"
		echo '{"metadata": [' > "$OUT"
		for file in "$DIR"*.json
		do
			cat "$file" >> "$OUT"
			echo "," >> "$OUT"
		done
		sed -i '$s/,$//' "$OUT"
		echo ']}' >> "$OUT"
		ed -s "$OUT" <<< $'1,$j\nwq'
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
