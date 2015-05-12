source('tb.R')
library(multicore)
ru.clauses  <-  do.call(rbind, mclapply(dir(pattern='.txt'), function(x) {
cat("Reading file ", x, " clause-by-clause\n")
read.tb(pipe(paste("cat ", x, " | sed -e 's/\\EUDICOp/\\speaker/g'", sep="")), format.desc = list(ref='id', speaker = 'single', age='single', text='single', mor='single'))
}, mc.cores=7))
ru.clauses$session <- gsub('\\_.*', '', ru.clauses$ref)
save(ru.clauses, file="ru.clauses.rda")	
