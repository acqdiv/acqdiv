# TODO: run on cha files once they're clean

# get non-error header lines
grep "^@" cha/*.cha > temp/header.tsv

# make tsv -- sed here Mac specific
sed -i 's/cha:@/cha\t@/g' temp/header.tsv
# sed -i 's/txt:@/txt\t@/g' temp/header.tsv
# sed -i 's/:[[:space:]]/:\t/g' temp/header.tsv
# sed -i 's/:[[:blank:]]/:\t/g' temp/header.tsv
# sed -i 's/@[[:alnum:]]*:[[:space:]]*/:\t/g' temp/header.tsv


# look at it with csvkit
csvstat -t -H temp/header.tsv

# header tags and their frequencies; split on ":" first to isolate tags
csvcut -t -c 2 temp/header.tsv | sort -gr | uniq -c

# extract stuff

# skip non-unique per file header categories
# grep "@Situation" cha/*.txt > temp/Situation.tsv
# sed -i 's/txt:@/txt\t@/g' temp/Situation.tsv

grep "@Transcriber" cha/*.cha > temp/Transcriber.tsv
echo "filename\tcategory\t@Transcriber:" | cat - temp/Transcriber.tsv > temp/Transcriber.tsv.tmp
mv temp/Transcriber.tsv.tmp temp/Transcriber.tsv
sed -i 's/cha:@/cha\t@/g' temp/Transcriber.tsv
tr -s '\t' '\t' < temp/Transcriber.tsv > temp/Transcriber.tsv.tmp
mv temp/Transcriber.tsv.tmp temp/Transcriber.tsv

grep "@Timing" cha/*.cha > temp/Timing.tsv
echo "filename\tcategory\t@Timing:" | cat - temp/Timing.tsv > temp/Timing.tsv.tmp
mv temp/Timing.tsv.tmp temp/Timing.tsv
sed -i 's/cha:@/cha\t@/g' temp/Timing.tsv
tr -s '\t' '\t' < temp/Timing.tsv > temp/Timing.tsv.tmp
mv temp/Timing.tsv.tmp temp/Timing.tsv


csvjoin -t -c filename --outer temp/Transcriber.tsv temp/Timing.tsv > metadata.csv

csvcut -c filename,@Transcriber:,@Timing: metadata.csv

exit

grep "@Date" cha/*.txt > temp/Date.tsv
echo "filename\tcategory\t@Date:" | cat - temp/Date.tsv > temp/Date.tsv.tmp
mv temp/Date.tsv.tmp temp/Date.tsv
sed -i 's/txt:@/txt\t@/g' temp/Date.tsv
tr -s '\t' '\t' < temp/Date.tsv > temp/Date.tsv.tmp
mv temp/Date.tsv.tmp temp/Date.tsv

grep "@File" cha/*.txt > temp/File.tsv
echo "filename\tcategory\t@File:" | cat - temp/File.tsv > temp/File.tsv.tmp
mv temp/File.tsv.tmp temp/File.tsv
sed -i 's/txt:@/txt\t@/g' temp/File.tsv
tr -s '\t' '\t' < temp/File.tsv > temp/File.tsv.tmp
mv temp/File.tsv.tmp temp/File.tsv

grep "@Location" cha/*.txt > temp/Location.tsv
echo "filename\tcategory\t@Location:" | cat - temp/Location.tsv > temp/Location.tsv.tmp
mv temp/Location.tsv.tmp temp/Location.tsv
sed -i 's/txt:@/txt\t@/g' temp/Location.tsv
tr -s '\t' '\t' < temp/Location.tsv > temp/Location.tsv.tmp
mv temp/Location.tsv.tmp temp/Location.tsv

grep "@Portion" cha/*.txt > temp/Portion.tsv
echo "filename\tcategory\t@Portion:" | cat - temp/Portion.tsv > temp/Portion.tsv.tmp
mv temp/Portion.tsv.tmp temp/Portion.tsv
sed -i 's/txt:@/txt\t@/g' temp/Portion.tsv
tr -s '\t' '\t' < temp/Portion.tsv > temp/Portion.tsv.tmp
mv temp/Portion.tsv.tmp temp/Portion.tsv

grep "@Time" cha/*.txt > temp/Time.tsv
echo "filename\tcategory\t@Time:" | cat - temp/Time.tsv > temp/Time.tsv.tmp
mv temp/Time.tsv.tmp temp/Time.tsv
sed -i 's/txt:@/txt\t@/g' temp/Time.tsv
tr -s '\t' '\t' < temp/Time.tsv > temp/Time.tsv.tmp
mv temp/Time.tsv.tmp temp/Time.tsv

grep "@Enterer" cha/*.txt > temp/Enterer.tsv
echo "filename\tcategory\t@Enterer:" | cat - temp/Enterer.tsv > temp/Enterer.tsv.tmp
mv temp/Enterer.tsv.tmp temp/Enterer.tsv
sed -i 's/txt:@/txt\t@/g' temp/Enterer.tsv
tr -s '\t' '\t' < temp/Enterer.tsv > temp/Enterer.tsv.tmp
mv temp/Enterer.tsv.tmp temp/Enterer.tsv

grep "@Section" cha/*.txt > temp/Section.tsv
echo "filename\tcategory\t@Section:" | cat - temp/Section.tsv > temp/Section.tsv.tmp
mv temp/Section.tsv.tmp temp/Section.tsv
sed -i 's/txt:@/txt\t@/g' temp/Section.tsv
tr -s '\t' '\t' < temp/Section.tsv > temp/Section.tsv.tmp
mv temp/Section.tsv.tmp temp/Section.tsv

grep "@Participants" cha/*.txt > temp/Participants.tsv
echo "filename\tcategory\t@Participants" | cat - temp/Participants.tsv > temp/Participants.tsv.tmp
mv temp/Participants.tsv.tmp temp/Participants.tsv
sed -i 's/txt:@/txt\t@/g' temp/Participants.tsv
tr -s '\t' '\t' < temp/Participants.tsv > temp/Participants.tsv.tmp
mv temp/Participants.tsv.tmp temp/Participants.tsv


grep "@Coder" cha/*.txt > temp/Coder.tsv
echo "filename\tcategory\t@Coder:" | cat - temp/Coder.tsv > temp/Coder.tsv.tmp
mv temp/Coder.tsv.tmp temp/Coder.tsv
sed -i 's/txt:@/txt\t@/g' temp/Coder.tsv
tr -s '\t' '\t' < temp/Coder.tsv > temp/Coder.tsv.tmp
mv temp/Coder.tsv.tmp temp/Coder.tsv

grep "@Checker" cha/*.txt > temp/Checker.tsv
echo "filename\tcategory\t@Checker:" | cat - temp/Checker.tsv > temp/Checker.tsv.tmp
mv temp/Checker.tsv.tmp temp/Checker.tsv
sed -i 's/txt:@/txt\t@/g' temp/Checker.tsv
tr -s '\t' '\t' < temp/Checker.tsv > temp/Checker.tsv.tmp
mv temp/Checker.tsv.tmp temp/Checker.tsv

grep "@Coding" cha/*.txt > temp/Coding.tsv
echo "filename\tcategory\t@Coding:" | cat - temp/Coding.tsv > temp/Coding.tsv.tmp
mv temp/Coding.tsv.tmp temp/Coding.tsv
sed -i 's/txt:@/txt\t@/g' temp/Coding.tsv
tr -s '\t' '\t' < temp/Coding.tsv > temp/Coding.tsv.tmp
mv temp/Coding.tsv.tmp temp/Coding.tsv

grep "@Other Info" cha/*.txt > temp/OtherInfo.tsv
echo "filename\tcategory\t@Other Info:" | cat - temp/OtherInfo.tsv > temp/OtherInfo.tsv.tmp
mv temp/OtherInfo.tsv.tmp temp/OtherInfo.tsv
sed -i 's/txt:@/txt\t@/g' temp/OtherInfo.tsv
tr -s '\t' '\t' < temp/OtherInfo.tsv > temp/OtherInfo.tsv.tmp
mv temp/OtherInfo.tsv.tmp temp/OtherInfo.tsv

grep "@Reviser" cha/*.txt > temp/Reviser.tsv
echo "filename\tcategory\t@Reviser:" | cat - temp/Reviser.tsv > temp/Reviser.tsv.tmp
mv temp/Reviser.tsv.tmp temp/Reviser.tsv
sed -i 's/txt:@/txt\t@/g' temp/Reviser.tsv
tr -s '\t' '\t' < temp/Reviser.tsv > temp/Reviser.tsv.tmp
mv temp/Reviser.tsv.tmp temp/Reviser.tsv

grep "@Tape Location" cha/*.txt > temp/TapeLocation.tsv
echo "filename\tcategory\t@Tape Location:" | cat - temp/TapeLocation.tsv > temp/TapeLocation.tsv.tmp
mv temp/TapeLocation.tsv.tmp temp/TapeLocation.tsv
sed -i 's/txt:@/txt\t@/g' temp/TapeLocation.tsv
tr -s '\t' '\t' < temp/TapeLocation.tsv > temp/TapeLocation.tsv.tmp
mv temp/TapeLocation.tsv.tmp temp/TapeLocation.tsv

grep "@Birth of MAE" cha/*.txt > temp/BirthofMAE.tsv
echo "filename\tcategory\t@Birth of MAE:" | cat - temp/BirthofMAE.tsv > temp/BirthofMAE.tsv.tmp
mv temp/BirthofMAE.tsv.tmp temp/BirthofMAE.tsv
sed -i 's/txt:@/txt\t@/g' temp/BirthofMAE.tsv
tr -s '\t' '\t' < temp/BirthofMAE.tsv > temp/BirthofMAE.tsv.tmp
mv temp/BirthofMAE.tsv.tmp temp/BirthofMAE.tsv

grep "@Tape" cha/*.txt > temp/Tape.tsv
echo "filename\tcategory\t@Tape:" | cat - temp/Tape.tsv > temp/Tape.tsv.tmp
mv temp/Tape.tsv.tmp temp/Tape.tsv
sed -i 's/txt:@/txt\t@/g' temp/Tape.tsv
tr -s '\t' '\t' < temp/Tape.tsv > temp/Tape.tsv.tmp
mv temp/Tape.tsv.tmp temp/Tape.tsv

grep "@Birth of JUP" cha/*.txt > temp/BirthofJUP.tsv
echo "filename\tcategory\t@Birth of JUP:" | cat - temp/BirthofJUP.tsv > temp/BirthofJUP.tsv.tmp
mv temp/BirthofJUP.tsv.tmp temp/BirthofJUP.tsv
sed -i 's/txt:@/txt\t@/g' temp/BirthofJUP.tsv
tr -s '\t' '\t' < temp/BirthofJUP.tsv > temp/BirthofJUP.tsv.tmp
mv temp/BirthofJUP.tsv.tmp temp/BirthofJUP.tsv

grep "@Comment" cha/*.txt > temp/Comment.tsv
echo "filename\tcategory\t@Comment:" | cat - temp/Comment.tsv > temp/Comment.tsv.tmp
mv temp/Comment.tsv.tmp temp/Comment.tsv
sed -i 's/txt:@/txt\t@/g' temp/Comment.tsv
tr -s '\t' '\t' < temp/Comment.tsv > temp/Comment.tsv.tmp
mv temp/Comment.tsv.tmp temp/Comment.tsv

grep "@Birth of SUP" cha/*.txt > temp/BirthofSUP.tsv
echo "filename\tcategory\t@Birth of SUP:" | cat - temp/BirthofSUP.tsv > temp/BirthofSUP.tsv.tmp
mv temp/BirthofSUP.tsv.tmp temp/BirthofSUP.tsv
sed -i 's/txt:@/txt\t@/g' temp/BirthofSUP.tsv
tr -s '\t' '\t' < temp/BirthofSUP.tsv > temp/BirthofSUP.tsv.tmp
mv temp/BirthofSUP.tsv.tmp temp/BirthofSUP.tsv

grep "@Break" cha/*.txt > temp/Break.tsv
echo "filename\tcategory\t@Break:" | cat - temp/Break.tsv > temp/Break.tsv.tmp
mv temp/Break.tsv.tmp temp/Break.tsv
sed -i 's/txt:@/txt\t@/g' temp/Break.tsv
tr -s '\t' '\t' < temp/Break.tsv > temp/Break.tsv.tmp
mv temp/Break.tsv.tmp temp/Break.tsv

grep "@Age of MAE" cha/*.txt > temp/AgeofMAE.tsv
echo "filename\tcategory\t@Age of MAE:" | cat - temp/AgeofMAE.tsv > temp/AgeofMAE.tsv.tmp
mv temp/AgeofMAE.tsv.tmp temp/AgeofMAE.tsv
sed -i 's/txt:@/txt\t@/g' temp/AgeofMAE.tsv
tr -s '\t' '\t' < temp/AgeofMAE.tsv > temp/AgeofMAE.tsv.tmp
mv temp/AgeofMAE.tsv.tmp temp/AgeofMAE.tsv

grep "@Age of SUP" cha/*.txt > temp/AgeofSUP.tsv
echo "filename\tcategory\t@Age of SUP:" | cat - temp/AgeofSUP.tsv > temp/AgeofSUP.tsv.tmp
mv temp/AgeofSUP.tsv.tmp temp/AgeofSUP.tsv
sed -i 's/txt:@/txt\t@/g' temp/AgeofSUP.tsv
tr -s '\t' '\t' < temp/AgeofSUP.tsv > temp/AgeofSUP.tsv.tmp
mv temp/AgeofSUP.tsv.tmp temp/AgeofSUP.tsv

grep "@Birth of CH1" cha/*.txt > temp/BirthofCH1.tsv
echo "filename\tcategory\t@Birth of CH1:" | cat - temp/BirthofCH1.tsv > temp/BirthofCH1.tsv.tmp
mv temp/BirthofCH1.tsv.tmp temp/BirthofCH1.tsv
sed -i 's/txt:@/txt\t@/g' temp/BirthofCH1.tsv
tr -s '\t' '\t' < temp/BirthofCH1.tsv > temp/BirthofCH1.tsv.tmp
mv temp/BirthofCH1.tsv.tmp temp/BirthofCH1.tsv

grep "@Age of ALI" cha/*.txt > temp/AgeofALI.tsv
echo "filename\tcategory\t@Age of ALI:" | cat - temp/AgeofALI.tsv > temp/AgeofALI.tsv.tmp
mv temp/AgeofALI.tsv.tmp temp/AgeofALI.tsv
sed -i 's/txt:@/txt\t@/g' temp/AgeofALI.tsv
tr -s '\t' '\t' < temp/AgeofALI.tsv > temp/AgeofALI.tsv.tmp
mv temp/AgeofALI.tsv.tmp temp/AgeofALI.tsv

grep "@Age of CHI" cha/*.txt > temp/AgeofCHI.tsv
echo "filename\tcategory\t@Age of CHI:" | cat - temp/AgeofCHI.tsv > temp/AgeofCHI.tsv.tmp
mv temp/AgeofCHI.tsv.tmp temp/AgeofCHI.tsv
sed -i 's/txt:@/txt\t@/g' temp/AgeofCHI.tsv
tr -s '\t' '\t' < temp/AgeofCHI.tsv > temp/AgeofCHI.tsv.tmp
mv temp/AgeofCHI.tsv.tmp temp/AgeofCHI.tsv

grep "@Age of JUP" cha/*.txt > temp/AgeofJUP.tsv
echo "filename\tcategory\t@Age of JUP:" | cat - temp/AgeofJUP.tsv > temp/AgeofJUP.tsv.tmp
mv temp/AgeofJUP.tsv.tmp temp/AgeofJUP.tsv
sed -i 's/txt:@/txt\t@/g' temp/AgeofJUP.tsv
tr -s '\t' '\t' < temp/AgeofJUP.tsv > temp/AgeofJUP.tsv.tmp
mv temp/AgeofJUP.tsv.tmp temp/AgeofJUP.tsv

grep "@Birth of ALI" cha/*.txt > temp/BirthofALI.tsv
echo "filename\tcategory\t@Birth of ALI:" | cat - temp/BirthofALI.tsv > temp/BirthofALI.tsv.tmp
mv temp/BirthofALI.tsv.tmp temp/BirthofALI.tsv
sed -i 's/txt:@/txt\t@/g' temp/BirthofALI.tsv
tr -s '\t' '\t' < temp/BirthofALI.tsv > temp/BirthofALI.tsv.tmp
mv temp/BirthofALI.tsv.tmp temp/BirthofALI.tsv

grep "@Birth of CHI" cha/*.txt > temp/BirthofCHI.tsv
echo "filename\tcategory\t@Birth of CHI:" | cat - temp/BirthofCHI.tsv > temp/BirthofCHI.tsv.tmp
mv temp/BirthofCHI.tsv.tmp temp/BirthofCHI.tsv
sed -i 's/txt:@/txt\t@/g' temp/BirthofCHI.tsv
tr -s '\t' '\t' < temp/BirthofCHI.tsv > temp/BirthofCHI.tsv.tmp
mv temp/BirthofCHI.tsv.tmp temp/BirthofCHI.tsv

grep "@Entererer" cha/*.txt > temp/Entererer.tsv
echo "filename\tcategory\t@Entererer:" | cat - temp/Entererer.tsv > temp/Entererer.tsv.tmp
mv temp/Entererer.tsv.tmp temp/Entererer.tsv
sed -i 's/txt:@/txt\t@/g' temp/Entererer.tsv
tr -s '\t' '\t' < temp/Entererer.tsv > temp/Entererer.tsv.tmp
mv temp/Entererer.tsv.tmp temp/Entererer.tsv

grep "@Comments" cha/*.txt > temp/Comments.tsv
echo "filename\tcategory\t@Comments:" | cat - temp/Comments.tsv > temp/Comments.tsv.tmp
mv temp/Comments.tsv.tmp temp/Comments.tsv
sed -i 's/txt:@/txt\t@/g' temp/Comments.tsv
tr -s '\t' '\t' < temp/Comments.tsv > temp/Comments.tsv.tmp
mv temp/Comments.tsv.tmp temp/Comments.tsv

# tr -s '[[:punct:][:space:]]' '\n' < temp # get a list of words without punctuation

# left joins; remove repeatedable per session categories, e.g. temp/Situation.tsv 
csvjoin -t -c filename --outer temp/Transcriber.tsv temp/Date.tsv temp/File.tsv temp/Portion.tsv temp/Time.tsv temp/Location.tsv temp/Enterer.tsv temp/Section.tsv temp/Participants.tsv temp/Timing.tsv temp/Coder.tsv temp/Checker.tsv temp/Coding.tsv temp/OtherInfo.tsv temp/Reviser.tsv temp/TapeLocation.tsv temp/BirthofMAE.tsv temp/Tape.tsv temp/BirthofJUP.tsv temp/Comment.tsv temp/BirthofSUP.tsv temp/Break.tsv temp/AgeofMAE.tsv temp/AgeofSUP.tsv temp/BirthofCH1.tsv temp/AgeofALI.tsv temp/AgeofCHI.tsv temp/AgeofJUP.tsv temp/BirthofALI.tsv temp/BirthofCHI.tsv temp/Entererer.tsv temp/Comments.tsv > metadata.csv


# cut the crud

csvcut -c 1,3,6 metadata.csv
