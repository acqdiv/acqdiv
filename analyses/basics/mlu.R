# Plot MLU from ACQDIV-DB languages
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


# return utterances from target children between 2-2.6
df <- runsql('
select utterances.id, utterances.corpus, utterances.speaker_label, utterances.utterance, utterances.pos_raw, speakers.age, speakers.macrorole, speakers.age_in_days
from utterances, speakers
where utterances.session_id_fk = speakers.session_id_fk
and utterances.speaker_label = speakers.speaker_label
and macrorole = "Target_Child"
and speakers.age_in_days > 700
and speakers.age_in_days < 950
')
glimpse(df)
dim(df)
# table(df$age)

# remove missing utterances
df <- df[complete.cases(df$utterance),]
glimpse(df)

# calculate utterance length -- IS THIS CORRECT?
df$utterance.length <- sapply(gregexpr("\\W+", df$utterance), length)
glimpse(df)
# qplot(df$age_in_days)

# bin em by 50 day age ranges
df$bins <- cut(df$age_in_days, breaks=c(700, 750, 800, 850, 900, 950), labels=c('(700,750]', '(750,800]', '(800,850]', '(850,900]', '(900,950]'))

# get subset of data and calculate MLU
results <- df %>% group_by(bins, corpus) %>% summarise(mean(utterance.length))
glimpse(results)
colnames(results) <- c('age.in.days', 'corpus', 'mlu')

# line plot of MLU per bin
ggplot(data=results, aes(x=age.in.days, y=mlu, group=corpus, colour=corpus)) + 
geom_line(aes(linetype=corpus))
# + geom_point()
ggsave("figures/mlu_target_children.pdf")

# get vocabulary size





### WIP BELOW ###

4380
6205
8030
9855

# return CDS
df <- runsql('
select utterances.id, utterances.speaker_label, utterances.utterance, utterances.pos_raw, speakers.age, speakers.macrorole
from utterances, speakers
where utterances.session_id_fk = speakers.session_id_fk
and utterances.speaker_label = speakers.speaker_label
and macrorole = "Adult"
')
glimpse(df)

# remove missing utterances
df <- df[complete.cases(df$utterance),]
glimpse(df)

# calculate utterance length -- IS THIS CORRECT?
df$utterance.length <- sapply(gregexpr("\\W+", df$utterance), length)
glimpse(df)
# qplot(df$age_in_days)

# bin em by 50 day age ranges
df$bins <- cut(df$age_in_days, breaks=c(700, 750, 800, 850, 900, 950), labels=c('(700,750]', '(750,800]', '(800,850]', '(850,900]', '(900,950]'))

# get subset of data and calculate MLU
results <- df %>% group_by(bins, corpus) %>% summarise(mean(utterance.length))
glimpse(results)
colnames(results) <- c('age.in.days', 'corpus', 'mlu')

# line plot of MLU per bin
ggplot(data=results, aes(x=age.in.days, y=mlu, group=corpus, colour=corpus)) + 
geom_line(aes(linetype=corpus))
# + geom_point()
ggsave("figures/mlu_target_children.pdf")



