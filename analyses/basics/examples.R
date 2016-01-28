# Examples for corpus manual
# Steven Moran <steven.moran@uzh.ch>
# install.packages('dplyr')

### WIP ###

library(dplyr)

# check unique speaker mappings
df <- read.csv("uniquespeakers.csv", header=F, stringsAsFactors=FALSE)
colnames(df) <- c('name', 'speaker_label', 'birthdate')
glimpse(df)
table(df$birthdate)
df$birthdate[df$birthdate == 'None'] <- NA

speakers <- runsql('select name, speaker_label, birthdate from speakers')
glimpse(speakers)
table(speakers$birthdate)
length(which(!is.na(speakers$birthdate)))


df$name %in% speakers$name
df$name.missing <- df$name %in% speakers$name
df$speaker_label %in% speakers$speaker_label
df$label.missing <- df$speaker_label %in% speakers$speaker_label
df$birthdate.missing <- df$birthdate %in% speakers$birthdate
head(df)

df$birthdate %in% speakers$birthdate
speakers$birthdate %in% df$birthdate


# Get all utterances
df <- runsql('SELECT * FROM utterances')
glimpse(df)



# Get all Turkish utterances
df <- runsql('SELECT * FROM utterances WHERE corpus="Turkish_KULLD"')
glimpse(df)

x <- df[df$corpus=="Turkish_KULLD", ]
glimpse(x)

### original ###
\begin{itemize}
	\item \textbf{Show all utterances} \\[0.2cm]
		\texttt{SELECT * FROM utterances} \\[0.19cm]
		\texttt{utterances}
		
	\item \textbf{Show all utterances from the Turkish corpus} \\[0.2cm]
		\texttt{SELECT * FROM utterances WHERE corpus="Turkish\und KULLDD"} \\[0.19cm]
		\texttt{utterances[utterances\$corpus=="Turkish\und KULLDD", ]}
		
	\item \textbf{Show only transcriptions and translations for Turkish utterances} \\[0.2cm]
		\texttt{SELECT utterance, translation FROM utterances WHERE corpus="Turkish\und KULLDD"} \\[0.19cm]
		\texttt{utterances[utterances\$corpus=="Turkish\und KULLDD", c("utterance",\\ "translation")]}
		
	\item \textbf{Get the types of unified part-of-speech tags used in Sesotho} \\[0.2cm]
		\texttt{SELECT DISTINCT pos FROM morphemes WHERE corpus="Sesotho"} \\[0.19cm]
		\texttt{unique(morphemes[morphemes\$corpus=="Sesotho", "pos"])} % unique(droplevels(morphemes[morphemes$corpus=="Chintang","pos_raw"]))
		
	\item \textbf{Count how often every part-of-speech type occurs in the individual corpora} \\[0.2cm]
		\texttt{SELECT corpus, pos, COUNT(*) AS `frequency` FROM morphemes GROUP BY corpus, pos} \\[0.19cm]
		\texttt{table(morphemes[ , c("corpus", "pos")])} % table(droplevels(morphemes[,c("corpus","pos_raw")]))
		
	\item \textbf{Get all utterances consisting of a negation marker} \\[0.2cm]
		\texttt{SELECT utterances.* FROM utterances \\
				INNER JOIN morphemes ON utterances.corpus=morphemes.corpus AND utterances.\\utterance\und id=morphemes.utterance\und id\und fk \\ 
				WHERE morphemes.gloss="NEG"} \\[0.19cm]
		\texttt{merge(utterances, morphemes, by.x=c("corpus", "utterance\und id"), by.y=\\c("corpus", "utterance\und id\und fk")) -> all; all[all\$gloss=="NEG", ]}
		
	\item \textbf{Get all utterances containing a negation marker, group by corpus} \\[0.2cm]
		\texttt{SELECT utterances.* FROM utterances \\
				INNER JOIN morphemes ON utterances.corpus=morphemes.corpus AND utterances.\\utterance\und id=morphemes.utterance\und id\und fk \\
				WHERE morphemes.gloss LIKE "\%NEG\%" ORDER BY utterances.corpus} \\[0.19cm]
		\texttt{merge(utterances, morphemes, by.x=c("corpus", "utterance\und id"), by.y=\\c("corpus", "utterance\und id\und fk")) -> all \\
				all[grep("NEG", all\$gloss), ]}
		
	\item \textbf{Get all utterances whose speaker is younger than 4 years} \\[0.2cm]
		\texttt{SELECT utterances.corpus, utterances.session\und id\und fk, utterances.utterance, utterances.speaker\und label, speakers.age, utterances.translation \\
				FROM utterances \\
				INNER JOIN speakers \\
				ON utterances.corpus=speakers.corpus AND utterances.session\und id\und fk=speakers.\\session\und id\und fk AND utterances.speaker\und\ label=speakers.speaker\und label \\
				WHERE speakers.age\und in\und days<1460} \\[0.19cm]
		\texttt{merge(utterances, speakers, by=c("corpus", "session\und id\und fk", "speaker\und label")) -> all \\
				all <- all[complete.cases(all\$age\und in\und days), ] \\
				all[all\$age\und in\und days<1460, c("corpus", "session\und id\und fk", "utterance",\\"speaker\und label", "age", "translation")]}
\end{itemize}


# fire off sql queries to the test database
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
