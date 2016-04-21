# check the ACQDIV database for columns which contain more than 99% NAs or empty cells
# load R object, then run
# source("dbchecks.R")

# go through tables (except all_data)
for (table_name in c("sessions","speakers","uniquespeakers","utterances","words","morphemes")){
	cat("\n", "checking", table_name, "\n")
	table <- get(table_name)
	
	# for current table check all corpora
	for (corpus in unique(sessions$corpus)){
		cat("\t", "corpus", corpus, "\n")
		rows_corpus <- nrow(table[table$corpus==corpus,])
		
		# check all columns
		for (column in colnames(table)){
			cat("\t\t", "column", column, ": ")
			
			rows_na <- nrow(table[table$corpus==corpus & (is.na(table[,column]) | table[,column]==""),])
			if (rows_na/rows_corpus > 0.99){
				cat("more than 99% NA - check!")
			}
			else {
				cat("OK")
			}
			
			cat("\n")
			
		}
	}
}