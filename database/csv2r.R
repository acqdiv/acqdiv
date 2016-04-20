# read CSV tables and save them as an R object

# path were CSV tables lie
base = "./csv/"
# list of table names
tables = c("morphemes","sessions","speakers","uniquespeakers","utterances","warnings","words")

# read CSV tables from base directory
for (table in tables){
	print(paste("reading table ",table,"...",sep=""))
	path_to_table = paste(base,table,".csv",sep="")
	assign(table, read.csv(path_to_table, na.strings=""))
}

# generate additional big flat table
print("merging to big flat table...")

# change "id" columns to unique names -> change once fixed in DB!
names(utterances)[names(utterances)=="id"] <- "utterance_id"
names(words)[names(words)=="id"] <- "word_id"
names(morphemes)[names(morphemes)=="id"] <- "morpheme_id"
names(speakers)[names(speakers)=="id"] <- "speaker_id"
names(uniquespeakers)[names(uniquespeakers)=="id"] <- "unique_speaker_id"
names(sessions)[names(sessions)=="id"] <- "session_id"
# other renamers
names(utterances)[names(utterances)=="source_id"] <- "utterance_id_source"
names(utterances)[names(utterances)=="morpheme"] <- "utterance_morphemes"
names(utterances)[names(utterances)=="gloss_raw"] <- "utterance_glosses_raw"
names(utterances)[names(utterances)=="pos_raw"] <- "utterance_poses_raw"
names(words)[names(words)=="pos"] <- "pos_word_stem"
names(sessions)[names(sessions)=="source_id"] <- "session_id_source"
names(morphemes)[names(morphemes)=="type"] <- "morpheme_type"

# merge tables one by one
merge(utterances, words, by.x="utterance_id", by.y="utterance_id_fk", all.x=TRUE, all.y=FALSE) -> u_w
merge(u_w, morphemes, by.x="word_id", by.y="word_id_fk", all.x=TRUE, all.y=FALSE) -> u_w_m
u_w_m <- u_w_m[,c("session_id_fk", "utterance_id", "utterance_id_source", "word_id", "morpheme_id", "speaker_label", "addressee", "utterance_raw", "utterance", "translation", "utterance_morphemes", "utterance_glosses_raw", "utterance_poses_raw", "sentence_type", "start", "end", "start_raw", "end_raw", "comment", "corpus", "language", "word", "pos_word_stem", "word_actual", "word_target", "morpheme", "morpheme_type", "gloss_raw", "gloss", "pos_raw", "pos")]
merge(sessions, u_w_m, by.x="session_id", by.y="session_id_fk", all.x=FALSE, all.y=TRUE) -> u_w_m_s
# speakers can only be merged in by composite key -> change once fixed in DB
merge(u_w_m_s, speakers, by.x=c("session_id","speaker_label"), by.y=c("session_id_fk","speaker_label"), all.x=TRUE, all.y=FALSE) -> all_data
all_data <- all_data[,c("corpus", "language", "session_id", "session_id_source", "date", "speaker_id", "speaker_label", "name", "birthdate", "age_raw", "age", "age_in_days", "gender_raw", "gender", "role_raw", "role", "macrorole", "addressee", "utterance_id", "utterance_id_source", "utterance_raw", "start_raw", "start", "end_raw", "end", "utterance", "translation", "utterance_morphemes", "utterance_glosses_raw", "utterance_poses_raw", "sentence_type", "comment", "word_id", "word", "word_actual", "word_target", "pos_word_stem", "morpheme_id", "morpheme_type", "morpheme", "gloss_raw", "gloss", "pos_raw", "pos")]

# dropped from final table:
# "media"
# "media_type"
# "languages_spoken"
# "uniquespeaker_id_fk"
# all duplicate columns (.x, .y)

# save all tables to an R object named "acqdiv_corpus-YYYY-MM-DD.rda"
date = format(Sys.time(), "%Y-%m-%d")
path_to_R = paste("acqdiv_corpus_",date,".rda",sep="")

save(file=path_to_R, list=c(tables,"all_data"))
