# Some basic descriptive stats on the acqdiv-db
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
us <- runsql('select corpus, count(*) from utterances group by corpus')
colnames(us) <- c('corpus', 'utterances')
ws <- runsql('select corpus, count(*) from words group by corpus')
colnames(ws) <- c('corpus', 'words')
ms <- runsql('select corpus, count(*) from morphemes group by corpus')
colnames(ms) <- c('corpus', 'morphemes')
x <- merge(us, ws)
y <- merge(x, ms)

# to latex table
y.tex <- xtable(y)
print(y.tex, type="latex", file="tables/utterance-word-morpheme.tex")

z <- melt(y)
head(z)
# qplot(corpus, value, data=z, color=variable)
ggplot(data=z, aes(x=corpus, y=value, fill=variable)) +
    geom_bar(stat="identity", position=position_dodge(), colour="black") +
	ggtitle("Tokens per corpus")
ggsave("figures/tokens.pdf")


# query utterances, words, morphemes type counts and make bar chart
us <- runsql('select corpus, count(distinct utterance) from utterances group by corpus')
colnames(us) <- c('corpus', 'utterances')
ws <- runsql('select corpus, count(distinct word) from words group by corpus')
colnames(ws) <- c('corpus', 'words')
ms <- runsql('select corpus, count(distinct morpheme) from morphemes group by corpus')
colnames(ms) <- c('corpus', 'morphemes')
a <- merge(us, ws)
b <- merge(a, ms)
c <- melt(b)
head(c)
# qplot(corpus, value, data=z, color=variable)
ggplot(data=c, aes(x=corpus, y=value, fill=variable)) +
    geom_bar(stat="identity", position=position_dodge(), colour="black") +
	ggtitle("Types per corpus")
ggsave("figures/types.pdf")


# bar chart number of sessions
ss <- runsql('select corpus, count(*) from sessions group by corpus')
colnames(ss) <- c('corpus', 'sessions')
ggplot(data=ss, aes(x=corpus, y=sessions)) +
    geom_bar(stat="identity", position=position_dodge(), colour="black")
ggsave("figures/sessions.pdf")


# number of speakers by gender per corpus
s <- runsql('select corpus, gender, count(gender) from uniquespeakers group by corpus, gender')
colnames(s) <- c('corpus', 'gender', 'participants')
t <- melt(s)
ggplot(data=s, aes(x=corpus, y=participants, fill=gender)) +
    geom_bar(stat="identity", position=position_dodge(), colour="black")
ggsave("figures/participants.pdf")


# number and kinds of POS labels in full acqdiv corpus
p <- runsql('select corpus, count(distinct pos_raw) from morphemes group by corpus')
colnames(p) <- c('corpus', 'pos')
# to latex table
p.tex <- xtable(p)
print(p.tex, type="latex", file="tables/corpus-pos.tex")
# as bar plot
ggplot(data=p, aes(x=corpus, y=pos)) +
    geom_bar(stat="identity", position=position_dodge(), colour="black")
ggsave("figures/pos.pdf")

# POS labels and counts data
p.labels <- runsql('select corpus, pos_raw from morphemes group by corpus, pos_raw')
p.labels.counts <- runsql('select corpus, pos_raw, count(pos_raw) from morphemes group by corpus, pos_raw')
glimpse(p.labels)

p.labels <- runsql('select corpus, pos_raw from morphemes')
x <- p.labels %>% group_by(corpus, pos_raw) %>% summarize(pos.count=n())
glimpse(x)

# subset per language

# flip data

# plot



# to latex table
# drop variable; change header to variable name


# mlm per word per utterance
stop("end script")




# number of labels

# number of utterances in CDS for each corpus where the children ~2-2.6 yrs

# query it
data <- runsql('
SELECT utterances.id, sessions.date, utterances.utterance, speakers.speaker_label, 
speakers.age_in_days, sessions.corpus 
FROM speakers 
INNER JOIN utterances ON utterances.session_id_fk = speakers.session_id_fk 
INNER JOIN sessions ON sessions.session_id = utterances.session_id_fk 
WHERE speakers.speaker_label = "ALJ" AND sessions.corpus = "Russian" 
AND role_raw = "Target_Child"
')

# query it
data <- runsql('
SELECT language, utterance from utterances
')

# have a look
glimpse(data)
summary(data)

# add utterance length
data$utterance.length <- sapply(gregexpr("\\W+", data$utterance), length)
glimpse(data)

# get subset of data and calculate MLU
results <- data %>% group_by(date) %>% summarise(mean(utterance.length))
glimpse(results)
colnames(results) <- c("date", "mlu")

# join the results to the data
data <- left_join(data, results)
glimpse(data)

# bar plot
ggplot(data=data, aes(date,mlu)) + geom_bar(stat = "identity")
