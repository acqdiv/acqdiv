# Convert the SQLite ACQDIV database into an R data object

library(RSQLite)

# Create conection
con <- dbConnect(SQLite(), "test.sqlite3")

# Which tables?
as.data.frame(dbListTables(con))

# Get tables as dfs
all_data <- dbReadTable(con, 'all_data')
corpora <- dbReadTable(con, 'corpora')
morphemes <- dbReadTable(con, 'morphemes')
sessions <- dbReadTable(con, 'sessions')
speakers <- dbReadTable(con, 'speakers')
uniquespeakers <- dbReadTable(con, 'uniquespeakers')
utterances <- dbReadTable(con, 'utterances')
words <- dbReadTable(con, 'words')

# Be good
dbDisconnect(con)

# Write to Rdata
save(all_data, corpora, morphemes, sessions, speakers, uniquespeakers, utterances, words, file="test.Rdata")

# Be nice
rm(list = ls())