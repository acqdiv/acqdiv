# Check ACQDIV-DB for missing utterances
# Steven Moran <steven.moran@uzh.ch>
#
# install.packages('RSQLite')
# install.packages('dplyr')
# install.packages('ggplot2')

library(RSQLite)
library(dplyr)
library(ggplot2)


# load db
runsql <- function(sql, dbname="../../database/acqdiv.sqlite3"){
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

# get utterances
df <- runsql('
select corpus, utterance from utterances
')
glimpse(df)
format(df)

x <- head(df)
format(x)
head(x)

xtable(x)

# getting NAs
df$missing <- is.na(df$utterance)
glimpse(df)

x <- df %>% group_by(corpus) %>% summarize(utterance=length(which(!missing)), missing=length(which(missing)))
glimpse(x)
y <- melt(x, id.var="corpus")
head(y)

ggplot(y, aes(x = corpus, y = value, fill = variable)) + 
  geom_bar(stat = "identity")
ggsave("figures/missing_utterances.pdf")
