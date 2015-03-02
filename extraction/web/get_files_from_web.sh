#!/bin/bash
# Use: sh get_files_from_web.sh
# What it does: This script downloads media files from the internet. The download URL and all relevant directories must be specified directly in this file. 
# Author: Robert Schikowski, 2014-09-05. Last update: 2014-09-11

download_base='http://childes.psy.cmu.edu/media/'
upload_base='/Volumes/Acqdiv/Corpora/'

dirs=(
'EastAsian/Indonesian/hiz/' 'EastAsian/Indonesian/ido/' 'EastAsian/Indonesian/lar/' 'EastAsian/Indonesian/mic/' 'EastAsian/Indonesian/pit/' 'EastAsian/Indonesian/pri/' 'EastAsian/Indonesian/ris/' 'EastAsian/Indonesian/tim/' 'EastAsian/Japanese/Ishii/' 'EastAsian/Japanese/Ishii/0wav/' 'EastAsian/Japanese/Kohe/' 'EastAsian/Japanese/MiiPro/ArikaF/' 'EastAsian/Japanese/MiiPro/ArikaF/0wav/' 'EastAsian/Japanese/MiiPro/ArikaM/' 'EastAsian/Japanese/MiiPro/ArikaM/0wav/' 'EastAsian/Japanese/MiiPro/Asato/' 'EastAsian/Japanese/MiiPro/Asato/0wav/' 'EastAsian/Japanese/MiiPro/Nanami/' 'EastAsian/Japanese/MiiPro/Nanami/0wav/' 'EastAsian/Japanese/MiiPro/Tomito/' 'EastAsian/Japanese/MiiPro/Tomito/0wav/' 'EastAsian/Japanese/Miyata/Tai/' 'EastAsian/Japanese/Miyata/Tai/0wav/' 'EastAsian/Japanese/Ota/' 'EastAsian/Japanese/Ota/Hiromi/' 'EastAsian/Japanese/Ota/Hiromi/0wav/' 'EastAsian/Japanese/Ota/Kenta/' 'EastAsian/Japanese/Ota/Kenta/0wav/' 'EastAsian/Japanese/Ota/Takeru/' 'EastAsian/Japanese/Ota/Takeru/0wav/' 'EastAsian/Japanese/Paidologos/' 'EastAsian/Japanese/Paidologos/0wav/' 'EastAsian/Japanese/Stanford/' 'EastAsian/Japanese/Stanford/0wav/' 'Other/Cree/Ani/' 'Other/Cree/Ani/0wav/' 'Other/Sesotho/' 'Other/Sesotho/0wav/' 
)

# go through directories in list 
for ((i=0; i<${#dirs[*]}; i++)) do
	# create local directory path if necessary
	mkdir -p $upload_base${dirs[i]}
	
	# download page where media files are listed, extract links to files
	curl $download_base${dirs[i]}  |
	perl -pe 's/^.*href=\"([^\"]+\.(mp3|wav|mpg))\".*$/$1/g' |
	egrep 'mp3|wav|mpg' |
	
	# download media files to local directory (unless they already exist)
	while read line
	do
		if [ -e "$upload_base${dirs[i]}$line" ]
		then
			echo $upload_base${dirs[i]}$line': file already exists, skipping it'
		else
			curl $download_base${dirs[i]}$line -o $upload_base${dirs[i]}$line
		fi
	done
	
done
