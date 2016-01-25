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

end.time <- Sys.time()
time.taken <- end.time - start.time
time.taken


# load the data
runsql <- function(sql, dbname="../database/_acqdiv.sqlite3"){
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
xtable(p)
ggplot(data=p, aes(x=corpus, y=pos)) +
    geom_bar(stat="identity", position=position_dodge(), colour="black")
ggsave("figures/pos.pdf")

# POS labels and counts data
p.labels <- runsql('select corpus, pos_raw from morphemes group by corpus, pos_raw')
# labels and counts
p.labels.counts <- runsql('select corpus, pos_raw, count(pos_raw) from morphemes group by corpus, pos_raw')

# to latex table
# drop variable; change header to variable name



# mlu by participant

# mlm per word per utterance



stop("end script")

### static stuff ###
\begin{table}[h]
 \begin{center}
\begin{tabular}{|l|l|l|l|}
\hline
ISO 639-3 & Language & Speakers & Classification \\
\hline
tur	&	Turkish	&	70,890,130	&	Altaic	\\
jpn	&	Japanese	&	128,056,940	&	Japanese	\\
ind	&	Indonesian	&	23,200,480	&	Austronesian	\\
yua	&	Yucatec	&	766,000	&	Mayan	\\
ike	&	Inuktitut	&	34,510	&	Eskimo-Aleut	\\
ctn	&	Chintang	&	3,710	&	Sino-Tibetan	\\
sot	&	Sesotho	&	5,634,000	&	Niger-Congo \\
rus	&	Russian	&	166,167,860	&	Indo-European	\\
cre	&	Cree	&	87,220	&	Algic	\\
chp	&	Dene	&	11,900	&	Na-Dene	\\
\hline
\end{tabular}
\caption{Language sample}\label{languages}
 \end{center}
\end{table}

\begin{table}[h]
 \begin{center}
\begin{tabular}{|l|l|l|l|l|l|}
\hline
Language	&	Format	&	Kids	&	Sessions	&	Words	\\
\hline
Chintang	&	Toolbox &	3	&	419	&	828272	\\
Cree	&	CHAT	&	1	&	10	& 21525	\\
Indonesian	&	Toolbox	&	8	&	997	& 2496828	\\
Inuktitut	&	CHAT-like	&	5	&	77	& 73302	\\
Japanese	&	XML	&	7	&	341	& 1235364	\\
Russian	&	Toolbox	&	4	&	448	& 2022992	\\
Sesotho	&	XML	&	4	&	129	& 237247	\\
Turkish	&	CHAT-like	&	8	&	373	& 1139877	\\
% RS: This will change considerably once cleaning is finished. The present DB only contains about 40% of all files.
Yucatec	&	CHAT-like	&	3	&	121	& 120441	\\
\hline
\end{tabular}
\caption{Corpora}\label{corpora}
 \end{center}
\end{table}


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
