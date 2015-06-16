#!/bin/bash

# Bash script to format ACQDIV corpus JSON
# currently handles only CHAT XML
# usage: metex.sh [-r|--recursive][-t|--target OUT][-d|--directory IN]|LIST OF FILES 
# Written by Cazim Hysi
# cazim dot hysi at uzh dot ch

# The heart of the script
# This basically just deletes the utterances and shuffles a few tiers around
extract_XML_JSON() {
< "$1" jq -c 'del(.CHAT.u) | .CHAT.Participants = .CHAT.Participants.participant | . = .CHAT'
}

# For recursively processing directories
rec_ext_XML_JSON() {
	# it is extremely important that these function variables be declared as local
	# otherwise things will not end well
	local DIR="$1"
	local OUT="$2"
	[[ $DIR = */ ]] || DIR="$DIR/"
	[[ $OUT = */ ]] || OUT="$OUT/"
	for sub in "$DIR"*
	do
		BN=$(basename $sub)
		# is the item a directory we can walk?
		if [[ -d $sub && $sub != *./ && $sub != "$DIR" ]]
		then
			# recurse
			rec_ext_XML_JSON "$sub" "$OUT""$BN"
		elif [[ -f $sub && $sub = *.json ]]
		then
			# make sure our output directory exists
			mkdir -p "$OUT"
			# call jq formatter and write
			extract_XML_JSON "$sub" > "$OUT""${BN%.json}_md.json"
		else
			continue
		fi
	done
}


# for glob mode
FILELIST[0]=0
ARRAYPTR=0

# operation variables
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
		-rd)
			RECURSIVE=1
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
# case 1: files to process are passed in from the command line
if [[ $BATCH == 0 ]]
then
	# this is where we use our fancy filename array
	for file in ${FILELIST[@]}
	do
		# make sure file names are correctly formatted
		[[ $file = /* ]] || file="./$file"
		BN=$(basename $file)
		extract_XML_JSON "$file" > "$OUT""${BN%.json}_md.json"
	done
# case 2: files are read from a directory
else 
	[[ $IN = */ ]] || IN="$IN/"
	[[ $IN = /* ]] || IN="./$IN"
	# case 2.1: directory processing is recursive
	if [[ $RECURSIVE == 1 ]]
	then
		# pass the args to the recursive processing function and let that worry about it
		rec_ext_XML_JSON "$IN" "$ABSPATH"
	# case 2.2: we don't go into subdirectories
	else
		for file in "$IN"*
		do
			if [[ -f "$file" && "$file" = *.json ]]
			then
				BN=$(basename $file)
				extract_XML_JSON "$file" > "$OUT""${BN%.json}_md.json"
			fi
		done
	fi
fi

exit 0

