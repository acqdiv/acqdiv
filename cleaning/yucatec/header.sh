# TODO: run on cha files once they're clean

# get non-error header lines
grep "^@" cha/*.txt > temp/header.tsv

# make tsv -- sed here Mac specific
# sed -i 's/cha:@/cha\t@/g' temp/header.tsv
sed -i 's/txt:@/txt\t@/g' temp/header.tsv
sed -i 's/:\s/:\t@/g' temp/header.tsv

# sed -i 's/:[[:space:]]/:\t/g' temp/header.tsv
# sed -i 's/:[[:blank:]]/:\t/g' temp/header.tsv
# sed -i 's/@[[:alnum:]]*:[[:space:]]*/:\t/g' temp/header.tsv

# look at it with csvkit
# csvstat -t temp/header.tsv

# header tags and their frequencies; split on ":" first to isolate tags
csvcut -t -c 2 temp/header.tsv | sort -gr | uniq -c
