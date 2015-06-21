#!/bin/bash

find_xml_dirs() {
	local ROOT="$1"

	dirarray=$(find "$ROOT" -name xml -type d)

	for sub in $dirarray
	do
		printf "Entering directory $sub\n"
		OUT="$sub/../json/"
		subarray=$(find "$sub" -type d)
		if [ ${#subarray[@]} -gt 0 ] 
		then
			for dir in $subarray
			do
				filearray=($(find "$dir" -maxdepth 1 -name "*.xml"))
				if [ ${#filearray[@]} -gt 0 ]
				then 
					process_xml_dir "$OUT$(basename $dir)" "${filearray[@]}"
				fi
			done
		else
			filearray=($(find "$sub" -maxdepth 1 -name "*.xml"))
			if [ ${#filearray[@]} -gt 0 ]
			then 
				process_xml_dir "$OUT" "${filearray[@]}"
			fi
		fi

	done
}

process_xml_dir() {
	local OUT="$1"
	shift
	local SOURCE=($@)

	mkdir -p "$OUT"
	[[ $OUT = */ ]] || OUT="$OUT/"

	for file in ${SOURCE[@]}
	do
		printf "Processing file $file\n"
		BN=$(basename "$file")

		< "$file" xml2json > "$OUT${BN%.xml}.json"
	done
}

IN="$1"
[[ $IN = */ ]] || IN="$IN/"
[[ $IN = /* ]] || IN="$(pwd)/$IN"

printf "Processing...\n"
find_xml_dirs "$IN"
printf "Done.\n"

exit 0
