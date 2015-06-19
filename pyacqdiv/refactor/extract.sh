#!/bin/bash

# Bash script to format ACQDIV corpus JSON
# currently handles only CHAT XML
# usage: extract.sh [-r|--recursive][-t|--target OUT][-d|--directory IN]|LIST OF FILES 
# Written by Cazim Hysi
# cazim dot hysi at uzh dot ch

# The heart of the script
# This basically just deletes the utterances and shuffles a few tiers around
extract_XML_JSON() {
	local FILE="$1"
	local SESSIONF="$2"
	local OUT="$3"
	local VERBOSE="$4"
	if [ $VERBOSE -eq 1 ] 
	then
		printf "Processing file $FILE\n"
	fi
	< "$FILE" jq -jf 'xml-session.jq' >> "$SESSIONF""_session_md.csv"
	printf "\n" >> "$SESSIONF""_session_md.csv"
	< "$FILE" jq -jf 'xml-participants.jq' > "$OUT"
}

# For recursively processing directories
rec_ext_XML_JSON() {
	# it is extremely important that these function variables be declared as local
	# otherwise things will not end well
	local DIR="$1"
	local OUT="$2"
	local VERBOSE="$3"
	[[ $DIR = */ ]] || DIR="$DIR/"
	[[ $OUT = */ ]] || OUT="$OUT/"
	for sub in "$DIR"*
	do
		BN=$(basename $sub)
		DIRBN=$(basename $DIR)
		# is the item a directory we can walk?
		if [[ -d $sub && $sub != *./ && $sub != "$DIR" ]]
		then
			# recurse
			rec_ext_XML_JSON "$sub" "$OUT""$BN" "$VERBOSE"
		elif [[ -f $sub && $sub = *.json ]]
		then
			# make sure our output directory exists
			mkdir -p "$OUT"
			FOUT="$OUT${BN%.json}_md.csv"
			# call jq formatter and write
			extract_XML_JSON "$sub" "$OUT$DIRBN" "$FOUT" "$VERBOSE"
		else
			continue
		fi
	done
}


# for glob mode
declare -a FILELIST
ARRAYPTR=0

# operation variables
# do we want detailed info
VERBOSE=0
# do we read in files from a directory?
BATCH=0
# if yes, do we also go into subdirectories?
RECURSIVE=0
# and from which directory?
IN=0
# where do we put the output?
# for sanity reasons forgetting to pass this on a recursive operation is highly not recommended
OUT="./"

# Loop through args and get them
while [[ $# > 0 ]]
do
	KEY=$1
	case $KEY in
		-d|--directory)
			BATCH=1
			IN="$2"
			shift
			shift
			;;
		-t|--target)
			OUT="$2"
			shift
			shift
			;;
		-r|--recursive)
			RECURSIVE=1
			shift
			;;
		-q|--quiet)
			VERBOSE=1
			shift
			;;
		-rd)
			RECURSIVE=1
			BATCH=1
			IN="$2"
			shift
			shift
			;;
		-rt)
			RECURSIVE=1
			OUT="$2"
			shift
			shift
			;;
		-vrd)
			RECURSIVE=1
			BATCH=1
			VERBOSE=1
			IN="$2"
			shift
			shift
			;;
		-vrt)
			RECURSIVE=1
			VERBOSE=1
			OUT="$2"
			shift
			shift
			;;
		-rvd)
			RECURSIVE=1
			BATCH=1
			VERBOSE=1
			IN="$2"
			shift
			shift
			;;
		-rvt)
			RECURSIVE=1
			VERBOSE=1
			OUT="$2"
			shift
			shift
			;;
		-*)
			echo "Unknown option: $KEY"
			exit 1
			;;
		*)
			FILELIST[$ARRAYPTR]="$KEY"
			let "ARRAYPTR += 1"
			shift
			;;
	esac
done

# make sure the output directory name is correctly formatted

[[ $OUT = */ ]] || OUT="$OUT/"
[[ $OUT = /* ]] || ABSPATH="$(pwd)/$OUT" && OUT="./$OUT"

# now for the actual script
printf "Processing...\n"
# case 1: files to process are passed in from the command line
if [[ $BATCH == 0 ]]
then
	# this is where we use our fancy filename array
	for file in ${FILELIST[@]}
	do
		# make sure file names are correctly formatted
		[[ $file = /* ]] || file="./$file"
		BN=$(basename $file)
		extract_XML_JSON "$file" "$OUT""json"  "$OUT""${BN%.json}_md.csv" "$VERBOSE" 
	done
# case 2: files are read from a directory
else 
	[[ $IN = */ ]] || IN="$IN/"
	[[ $IN = /* ]] || IN="./$IN"
	# case 2.1: directory processing is recursive
	if [[ $RECURSIVE == 1 ]]
	then
		# pass the args to the recursive processing function and let that worry about it
		rec_ext_XML_JSON "$IN" "$ABSPATH" "$VERBOSE"
	# case 2.2: we don't go into subdirectories
	else
		DIRBN=$(basename $IN)
		EXOUT="$OUT$DIRBN"
		for file in "$IN"*
		do
			if [[ -f "$file" && $file = *.json ]]
			then
				BN=$(basename $file)
				FOUT="$OUT""${BN%.json}_md.csv"
				extract_XML_JSON  "$file" "$EXOUT" "$FOUT" "$VERBOSE"
			fi
		done
	fi
fi
printf "Done.\n"
exit 0
