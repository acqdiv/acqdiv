#!/bin/bash

OUT=$1
shift
while [[ $# > 0 ]]
do
	echo "Processing file $1"
	cat "$1" >> $OUT
	rm "$1"
	shift
done
echo "Formatting..."
ed -s "$OUT" <<< $'1,$j\nwq'
sed -i 's/\]}{"metadata": \[/,/g' "$OUT"
echo "Done."
exit
