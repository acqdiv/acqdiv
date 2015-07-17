# Get some basic stats from the ACQDIV corpora R object (data resides on server)

# library(plyr) # plyr doesn't play well with dplyr @cazim
library(dplyr)
library(ggplot2)

acqdiv_corpora <- readRDS("acqdiv_corpora.RDS")
load("acqdiv_metadata.Rdata")

# rename the Japanese corpora
acqdiv_corpora$Language[acqdiv_corpora$Language == "Japanese_MiiPro"] <- "Japanese"
acqdiv_corpora$Language[acqdiv_corpora$Language == "Japanese_Miyata"] <- "Japanese"

participant.metadata$Language <- revalue(participant.metadata$Language, c(Japanese_Miyata="Japanese", Japanese_Miipro="Japanese"))
session.metadata$Language <- revalue(session.metadata$Language, c(Japanese_Miyata="Japanese", Japanese_Miipro="Japanese"))

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
ggplot(z, aes(Language, count)) + geom_bar(stat="identity") + scale_y_continuous()

# -- metadata --

# participants:
# participant count
x <- distinct(select(participant.metadata, Language, participant.code))
y <- group_by(x, Language)
z <- summarize(y, count = n())
ggplot(z, aes(Language, count)) + geom_bar(stat="identity") + scale_y_continuous()

# by name
x <- distinct(select(participant.metadata, Language, participant.code))
y <- group_by(x, Language)
z <- summarize(y, count = n())
ggplot(z, aes(Language, count)) + geom_bar(stat="identity") + scale_y_continuous()

# sex
x <- group_by(participant.metadata, participant.sex)
y <- summarize(x, count=n())
y <- rename(y, sex = participant.sex)
ggplot(y, aes(sex, count)) + geom_bar(stat="identity") + scale_y_continuous()

# excluding NAs

y <- y[!y$sex %in% c(NA),]
ggplot(y, aes(sex, count)) + geom_bar(stat="identity") + scale_y_continuous()

# sessions:
# sessions by continent
x <- distinct(select(session.location.continent, session.code))
y <- group_by(x, session.location.continent)
z <- summarize(y, count = n())
z <- z[!z$session.location.continent %in% c("Unspecified", NA),]
z <- rename(z, Continent = session.location.continent)
ggplot(z, aes(Continent, count)) + geom_bar(stat="identity") + scale_y_continuous()
