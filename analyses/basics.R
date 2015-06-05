# Get some basic stats from the ACQDIV corpora R object (data resides on server)

library(dplyr)
library(ggplot2)

acqdiv_corpora <- readRDS("acqdiv_corpora.RDS")

# rename the Japanese corpora
acqdiv_corpora$Language[acqdiv_corpora$Language == "Japanese_MiiPro"] <- "Japanese"
acqdiv_corpora$Language[acqdiv_corpora$Language == "Japanese_Miyata"] <- "Japanese"

# sessions count
x <- distinct(select(acqdiv_corpora, Language, session.id))
y <- group_by(x, Language)
z <- summarize(y, count = n())
ggplot(z, aes(Language, count)) + geom_bar(stat="identity")

# utterances count
x <- distinct(select(acqdiv_corpora, Language, utterance.id))
y <- group_by(x, Language)
z <- summarize(y, count = n())
ggplot(z, aes(Language, count)) + geom_bar(stat="identity")

# words count
# x <- distinct(select(acqdiv_corpora, Language, word.id))
y <- group_by(acqdiv_corpora, Language, word.id)
z <- summarize(y, count = n())
ggplot(z, aes(Language, count)) + geom_bar(stat="identity") + scale_y_continuous(labels = comma)

