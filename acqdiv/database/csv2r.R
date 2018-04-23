# read CSV tables and save them as an R object

library(dplyr)

# path were CSV tables lie
base = "./csv/"
# list of table names
tables = c("morphemes","sessions","speakers","uniquespeakers","utterances","words")

# read CSV tables from base directory
for (table in tables){
	print(paste("reading table ",table,"...",sep=""))
	path_to_table = paste(base,table,".csv",sep="")
	assign(table, read.csv(path_to_table, na.strings=""))
}

# generate additional big flat table
print("merging to big flat table...")

# change "id" columns to unique names -> change once fixed in DB!
utterances <- utterances %>% rename(utterance_id=id, utterance_id_source=source_id, utterance_morphemes=morpheme, utterance_gloses_raw=gloss_raw, utterance_poses_raw=pos_raw)
words <- words %>% rename(word_id=id, pos_word_stem=pos)
morphemes <- morphemes %>% rename(morpheme_id=id, morpheme_type=type)
speakers <- speakers %>% rename(speaker_id=id)
uniquespeakers <- uniquespeakers %>% rename(unique_speaker_id=id)
sessions <- sessions %>% rename(session_id=id, session_id_source=source_id)

# create alternative tables without columns that would only create duplicates, including warnings
utterances_slim <- utterances %>% select(utterance_id, session_id_fk, utterance_id_source, corpus, language, speaker_id_fk, speaker_label, addressee, childdirected, utterance, translation, utterance_morphemes, start, end, comment, warning)
words_slim <- words %>% select(word_id, utterance_id_fk, word, pos_word_stem, word_actual, word_target)
morphemes_slim <- morphemes %>% select(morpheme_id, word_id_fk, morpheme_type, morpheme, gloss_raw, gloss, pos_raw, pos, morpheme_language)
morphemes_slim <- morphemes_slim %>% filter(!is.na(word_id_fk)) # take out NA foreign keys for easier merging
sessions_slim <- sessions %>% select(session_id, session_id_source, date, target_child_fk)
speakers_slim <- speakers %>% select(speaker_id, session_id_fk, uniquespeaker_id_fk, name, age_raw, age, age_in_days, gender_raw, gender, role_raw, role, macrorole, languages_spoken, birthdate)

# merge tables one by one
left_join(utterances_slim, words_slim, by=c("utterance_id"="utterance_id_fk")) -> u_w
left_join(u_w, morphemes_slim, by=c("word_id"="word_id_fk")) -> u_w_m
left_join(sessions_slim, u_w_m, by=c("session_id"="session_id_fk")) -> u_w_m_s
# left_join(u_w_m_s, speakers_slim, by=c("session_id"="session_id_fk", "speaker_label"="speaker_label")) -> all_data # this is how we had to merge earlier
left_join(u_w_m_s, speakers_slim, by=c("speaker_id_fk"="speaker_id")) -> all_data

# final set of columns
all_data <- all_data %>% select(corpus, language, session_id, session_id_source, target_child_fk, date, speaker_id_fk, speaker_label, name, birthdate, age_raw, age, age_in_days, gender_raw, gender, role_raw, role, macrorole, addressee, childdirected, utterance_id, utterance_id_source, start, end, utterance, translation, utterance_morphemes, comment, word_id, word, word_actual, word_target, pos_word_stem, morpheme_id, morpheme_type, morpheme, gloss_raw, gloss, pos_raw, pos, morpheme_language)

# drop slim tables
rm(words_slim, morphemes_slim, sessions_slim, speakers_slim)

# sort big table so morphemes are displayed in order
all_data <- all_data[order(all_data$corpus, all_data$session_id, all_data$utterance_id, all_data$word_id, all_data$morpheme_id),]

# save all tables to an R object named "acqdiv_corpus-YYYY-MM-DD.rda"
date = format(Sys.time(), "%Y-%m-%d")
path_to_R = paste("acqdiv_corpus_",date,".rda",sep="")
save(file=path_to_R, list=c(tables,"all_data"))
