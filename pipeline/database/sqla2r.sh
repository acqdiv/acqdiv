# convert an SQL database to an R object consisting of several dataframes
# usage: 
# 	sh sqla2r.sh path/to/db 	# standard usage with existing DB
# 	sh -l sqla2r.sh path/to/db 	# -l option additionally calls loader.py to create the DB from scratch
# run this from the acqdiv/pipeline directory and make sure the following files are available: acqdiv/pipeline/sqla2csv.py, acqdiv/pipeline/csv2r.R. When using the -l option, you'll also need acqdiv/pipeline/loader.py and acqdiv/corpora. 
# author: Robert Schikowski, 2015-01-05


# check options; if -l is set run loader to generate DB
while getopts "l" opt; do
	case $opt in
		l)
			echo '\n*** Running loader.py to generate DB ***\n'
			python3 loader.py
			if [ $? -eq 1 ]; then
				SUCCESS='fail'
			fi
			;;
	    \?)
	      	echo "Usage: sh sqla2r.sh [-l] file"
			;;
	esac
done
shift $((OPTIND-1))

# run other scripts
echo '\n*** Running sqla2csv.py to generate CSV ***'
python3 sqla2csv.py $1
if [ $? -eq 1 ]; then
	SUCCESS='fail'
fi	
echo '\n*** Running csv2r.py to generate R object ***\n'
Rscript csv2r.R
rm -R csv/
if [ $? -eq 1 ]; then
	SUCCESS='fail'
fi

# check if all scripts exited successfully and produce corresponding message
echo $SUCCESS
if [ "$SUCCESS" == 'fail' ]; then
	echo '*** Could not create R object - see above for possible errors ***\n'
else
	echo '*** Successfully created acqdiv_corpus_'`date +%Y-%m-%d`'.rda ***\n'
fi


<<COMMENTS

(1) loader.py: source files to SQL DB
	in: repo/corpora and repo/pipeline; corpora taken from server (Acqdiv/Corpora/corpora).
	out: DB in repo/pipeline/_acqdiv.sqlite3
(2) sqla2csv.py: DB to CSV
	in: DB in repo/pipeline/_acqdiv.sqlite3
	out: several tables in repo/pipeline/csv
(3) csv2r.R: CSV to R
	in: CSV tables in repo/pipeline/csv
	out: R object repo/pipeline/acqdiv_corpus_YYYY-MM-DD.rda

option 1: run everything on server
	+ automatisation, output instantly available for everyone
	- loader must be moved and run on server; regular updates are necessary
option 2: run offline
	+ simple
	- manual, requires somebody to keep their computer switched on while the loader runs

-> start with option 2; later extension to option 1 possible (change directories, best clone project repo directly to server?)

COMMENTS