# Check for homophones
# Steven Moran <steven.moran@uzh.ch>

# install.packages('RSQLite')
# install.packages('ggplot2')
# install.packages('dplyr')
# install.packages('reshape2')
# install.packages('xtable')

library(reshape2)
library(RSQLite)
library(dplyr)
library(ggplot2)
library(xtable)

# time wrapper if needed
start.time <- Sys.time()
% ...
end.time <- Sys.time()
time.taken <- end.time - start.time
time.taken


### WIP !!! ###


# load db
runsql <- function(sql, dbname="../../database/_acqdiv.sqlite3"){
  require(RSQLite)
  driver <- dbDriver("SQLite")
  connect <- dbConnect(driver, dbname=dbname);
  closeup <- function(){
    sqliteCloseConnection(connect)
    sqliteCloseDriver(driver)
  }
  dd <- tryCatch(dbGetQuery(connect, sql), finally=closeup)
  return(dd)
}

# query utterances, words, morphemes token counts and make bar chart
df <- runsql('select corpus, morpheme, pos_raw from utterances group by morpheme, pos_raw')
glimpse(df)

df <- runsql('select corpus, morpheme, pos_raw from morphemes group by morpheme, pos_raw')
glimpse(df)
table(df$morpheme)



