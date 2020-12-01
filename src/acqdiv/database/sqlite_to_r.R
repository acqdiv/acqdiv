# Convert the SQLite ACQDIV database into an R data object
# Make sure to set the db connection sqlite file below

library(RSQLite)

args = commandArgs(trailingOnly=TRUE)

# Create conection
con <- dbConnect(SQLite(), args[1])

# Which tables?
as.data.frame(dbListTables(con))

# Get tables as dfs
all_data <- dbReadTable(con, 'v_all_data')
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
save(all_data, corpora, morphemes, sessions, speakers, uniquespeakers, utterances, words, file="acqdiv.Rdata")

# Be nice
rm(list = ls())
