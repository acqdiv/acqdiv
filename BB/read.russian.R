# reading the Russian corpus with moving comments into a separate comments column.
# Requires: 
#       7 cores (or else set mc.cores to another figure)
#       all tbx files and this script in the same directory
#       inside this directory another directory called "imdis"
#
# Usage:
#       R CMD BATCH --slave read.ctncl.R &

source('http://www.uni-leipzig.de/~autotyp/tb.r')
library(multicore)
ru.words  <-  do.call(rbind, mclapply(dir(pattern='.txt'), function(x) {
cat("Reading file ", x, " word-by-word\n")
read.tb(pipe(paste("cat ", x, " | sed -e 's/^\\\\EUDICOp/\\speaker/g' | gsed -r '/^\\\\text/s/(.*?)(\\[.*?\\])(.*)/\\1\\3\\n\\\\comment \\2/g'", sep="")), format.desc = list(ref='id', speaker = 'single', age='single', text='word', mor='word', comment='single')) 
}, mc.cores=7))
ru.words$session <- gsub('\\_.*', '', ru.words$ref)

ru.clauses  <-  do.call(rbind, mclapply(dir(pattern='.txt'), function(x) {
cat("Reading file ", x, " clause-by-clause\n")
read.tb(pipe(paste("cat ", x, " | sed -e 's/^\\\\EUDICOp/\\speaker/g' | gsed -r '/^\\\\text/s/(.*?)(\\[.*?\\])(.*)/\\1\\3\\n\\\\comment \\2/g'", sep="")), format.desc = list(ref='id', speaker = 'single', age='single', text='single', mor='single', comment='single'))
}, mc.cores=7))
ru.clauses$session <- gsub('\\_.*', '', ru.clauses$ref)

#######################################
cat("Cleaning up file and ref names\n")

ru.words$ref <- gsub('-latin', '', ru.words$ref)
ru.words$session <- gsub('-latin', '', ru.words$session)
ru.words$session <- gsub('B', 'A', ru.words$session)
ru.words$session <- gsub('Y', 'V', ru.words$session)
ru.words$session <- gsub('L', 'J', ru.words$session)

ru.clauses$ref <- gsub('-latin', '', ru.clauses$ref)
ru.clauses$session <- gsub('-latin', '', ru.clauses$session)
ru.clauses$session <- gsub('B', 'A', ru.clauses$session)
ru.clauses$session <- gsub('Y', 'V', ru.clauses$session)
ru.clauses$session <- gsub('L', 'J', ru.clauses$session)

#######################################
cat("Reading the metadata\n")
library(XML)
library(chron)
library(zoo)
target.children <- c("ALJ", "VAN", "PAS", "ANJ", "JAS")
setwd('./imdis')
speaker.ages <- do.call(rbind, lapply(dir(pattern='\\.imdi'), function(session) {
file <- xmlTreeParse(paste(session),asTree=F, useInternalNodes=T)
code <- xpathSApply(file, "//o:Session//o:MDGroup//o:Actors//o:Code", xmlValue, namespaces=c(o="http://www.mpi.nl/IMDI/Schema/IMDI"))
birth.date <- xpathSApply(file, "//o:Session//o:MDGroup//o:Actors//o:BirthDate", xmlValue, namespaces=c(o="http://www.mpi.nl/IMDI/Schema/IMDI"))
recording.date <- xpathSApply(file, "//o:Session//o:Date", xmlValue, namespaces=c(o="http://www.mpi.nl/IMDI/Schema/IMDI"))
rec.date <- recording.date[1] # the one in the first <Date> field.
session <- gsub('\\.imdi','', session)
data.list <- data.frame(session=rep(session, length.out=length(code)), code=code, birth.date=birth.date, rec.date=rep(rec.date,length.out=length(code)))
return(data.list)
}))
ru.metadata <- subset(speaker.ages, code %in% target.children)
ru.metadata$birth.date <- dates(as.character(ru.metadata$birth.date), format=c(dates='y-m-d'))
ru.metadata$rec.date <- dates(as.character(ru.metadata$rec.date), format=c(dates='y-m-d'))
ru.metadata$age.in.days <- ru.metadata$rec.date-ru.metadata$birth.date
# for printing labels, we use the representation in \age in the toolbox files
ru.metadata$session <- gsub('\\_','', ru.metadata$session) 

ru.metadata$session <- gsub('B', 'A', ru.metadata$session)
ru.metadata$session <- gsub('Y', 'V', ru.metadata$session)
ru.metadata$session <- gsub('L', 'J', ru.metadata$session)

cat("Saving...\n")

setwd('../')
today <- format(Sys.Date(), "%d%b%Y")
save(list=ls(), file=paste('ru.corpus', today, 'rda', sep='.'))	
