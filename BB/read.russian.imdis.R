library(XML)
library(chron)
library(zoo)
target.children <- c("ALJ", "VAN", "PAS", "ANJ", "JAS")
setwd('/Users/bickel/Documents/in_progress/language_acquisition/russian/imdis')
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
save(ru.metadata, file='ru.metadata.rda')