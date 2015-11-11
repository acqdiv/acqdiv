# read CSV tables from the server and save them as an R object

# path were CSV tables lie
base = "/Volumes/Acqdiv/Database/"

# read CSV tables from server
for (table in c("morphemes","session","speaker","uniquespeaker","utterance","warnings","words")){
	print(paste("reading table ",table,"...",sep=""))
	path_to_table = paste(base,"csv/",table,".csv",sep="")
	assign(table, read.csv(path_to_table))
}

# save all tables to R object on server named "corpus-YYYY-MM-DD.rda"
date = format(Sys.time(), "%Y-%m-%d")
path_to_R = paste(base,"R/corpus-",date,".rda",sep="")

save(file=path_to_R, morphemes, session, speaker, uniquespeaker, utterance, warnings, words)