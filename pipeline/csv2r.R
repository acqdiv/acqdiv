# read CSV tables and save them as an R object

# path were CSV tables lie
base = "./csv/"
# list of table names
tables = c("morphemes","sessions","speakers","uniquespeakers","utterances","warnings","words")

# read CSV tables from base directory
for (table in tables){
	print(paste("reading table ",table,"...",sep=""))
	path_to_table = paste(base,table,".csv",sep="")
	assign(table, read.csv(path_to_table))
}

# save all tables to an R object named "acqdiv_corpus-YYYY-MM-DD.rda"
date = format(Sys.time(), "%Y-%m-%d")
path_to_R = paste("acqdiv_corpus_",date,".rda",sep="")

save(file=path_to_R, list=tables)
