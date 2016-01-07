options(width=260)

# load the nesssary libraries
library(RSQLite)
library(dplyr)
library(xtable)






# ---------------------------
# PREPARE THE DATA
# ---------------------------

TARGET_AGE <- c(2, 3)
CONTEXT_LENGTH <- 2
TEXT_OFFSET <- 12

# load the database
aqcdiv_db <- dbConnect(SQLite(), 'acqdiv.sqlite3')
dbClearResult(dbSendQuery(aqcdiv_db, 'PRAGMA mmap_size=2147483648;'))



# load the speaker table
dbReadTable(aqcdiv_db, 'speaker') %>%
mutate(
  # age in years
  age = age_in_days/365,	
  # adults are 12 or older! or NA
  stype = ifelse(is.na(age), 'adult', NA),
  stype = ifelse(!is.na(age) & age >= 12, 'adult', stype),
  # only interested in children between 2 and 3
  stype = ifelse(!is.na(age) & age <= max(TARGET_AGE) & age >= min(TARGET_AGE), 'child', stype),
  # all other speakers have s(peaker)type NA
  # unique speaker id per session
  speakersessionid = paste(session_id_fk, speaker_label, sep='.')
) %>%
filter(
  # remove all that are neither children in the given age nor adults
  !is.na(stype),
  # also remove duplicated speakers, there is a bunch of those in the data
  !speakersessionid %in% speakersessionid[duplicated(speakersessionid)]
) %>%
select(
  session_id_fk, speaker_label, stype, age
) -> speakers


# load the utterance table
dbReadTable(aqcdiv_db, 'utterance', select.cols='language, session_id_fk, utterance_id, speaker_label, utterance_raw, translation, sentence_type, start, end, gloss_raw') %>%
mutate(
	is_question = (sentence_type %in% c('question', 'interruption question')) | grepl('\\? *$', as.character(translation))
) -> utterances


# link the both together
left_join(utterances, speakers, by = c('speaker_label', 'session_id_fk')) %>%
mutate(
  # make sure the types are correct
  # factors mess stuff up
  speaker_label = as.character(speaker_label),
  stype = as.character(stype)
) -> utterances
# this table now holds all the data we need


# ---------------------------
# Detect repair candidates
# ---------------------------
utterances %>%
group_by(session_id_fk) %>%
mutate(
  # we are looking for A B A utterance patterns, where
  possible_repair = 
    # A and B are different speakers
    (lag(speaker_label) == lead(speaker_label)) & 
    (lag(speaker_label) != speaker_label)       & 
    # B aks a question
    is_question                                 &
    # A is child and B is adult or via versa (they have different stypes)
    lag(stype) != stype,
  # fix the NAs 	
  possible_repair = possible_repair %in% T
) %>% 
ungroup -> utterances

# get the child age of the repair instance
# for some reason dplyr does not work here
child_age = ifelse(utterances$possible_repair, ifelse(!is.na(utterances$age) & utterances$age<=max(TARGET_AGE), utterances$age, lag(utterances$age)), NA)
# cut into age categoty
utterances$child_age_category <- cut(child_age, breaks=seq(from=min(TARGET_AGE), to=max(TARGET_AGE), by=1/12), include.lowest=T)

#saveRDS(utterances, file='repair_enhanced_utterances.rds')	


if(any(is.na(utterances$child_age_category[utterances$possible_repair]))) stop('NAs in child age category, this is not possible!')

# ---------------------------
# Create the repair candidate table, 
# grouped by language, repair initiator, and child age category
# ---------------------------
filter(utterances, possible_repair) %>%
transmute(
	language               = language,
	initiator              = stype,
	child_age_category     = child_age_category,
	position_in_utterances = which(utterances$possible_repair)
) %>%
group_by(
	language, initiator, child_age_category
) %>%
summarize(
	positions_in_utterances = list(position_in_utterances)
) %>%
group_by(
	language
) %>%
mutate(
	filename = paste0(language, 1:n(), '.txt')
) %>%
ungroup -> repair_candidates_grouped

prefix <- paste0('AnnotationData-', format(Sys.time(), "%d-%b-%Y"))
dir.create(prefix, showWarnings = F)
    
# save the data so that we know what is what!
saveRDS(repair_candidates_grouped, file=file.path(prefix, 'repair_candidates_grouped.rds'))	



# ---------------------------
# Write the files
# ---------------------------
repair_candidates_to_text <- function(iii) {
    # get the relevant items
    sapply(iii, function(i) {
        # the uid of the utterance
        uid <- with(utterances, paste0('/', session_id_fk[i], '/', utterance_id[i], '/', i))
        
        # extract the relevant text
        session_range <- which(utterances$session_id_fk %in% utterances$session_id_fk[i])
        #session_range <- c(min(session_range), max(session_range))
        
        # buidl speaker codes
        i_range <- (i-CONTEXT_LENGTH):(i+CONTEXT_LENGTH)
        speaker_labels <- factor(utterances$speaker_label[i_range])
        
        
        # we want to recode the spaeker labels as A, B, other1, other2 etc. 
        # for this, we want to build an ordered list of all attested speakers
        labels_order <- c(as.character(utterances$speaker_label[i]), as.character(utterances$speaker_label[i+1]))
        labels_order <- c(labels_order, setdiff(levels(speaker_labels), labels_order))
        labels_coded <- c('B', 'A', if(length(labels_order)>2)  paste0('other', 1:(length(labels_order)-2)) else character())
        
        stopifnot(length(labels_coded) == length(levels(speaker_labels)))
        stopifnot(length(labels_coded) == length(labels_order))
                
        levels(speaker_labels) <- labels_coded[match(levels(speaker_labels), labels_order)]
        
        # construct the text
        text <- utterances$utterance_raw[i_range]
        prefix <- paste0(i_range-i, '  ', speaker_labels, ':')

        padToLen <- function(x, len) paste0(x, paste0(rep(' ', max(0, len - nchar(x))), collapse=''))
        
        text <- paste0(sapply(prefix, function(x) padToLen(x, TEXT_OFFSET)), text)
        
        padding <- padToLen('', TEXT_OFFSET)
        glosses <- paste0(padding, utterances$gloss_raw[i_range])
        translation <- paste0(padding, utterances$translation[i_range])
        
        text <- paste(text, glosses, translation, sep='\n')
        
        # text <- sapply(seq_along(text), function(i)  paste(na.omit(c(text[i], glosses[i], translation[i])), collapse='\n'))
        # print(text)
        #
        # cut out everything that does not belong into the session
        text <- text[i_range %in% session_range]
        text <- paste0(text, collapse='\n')
        
        # put it all together
        paste(uid, text, 'Repair type:\nNotes:', sep='\n')
    }) -> repair_candidates_text

    repair_candidates_text
}

for(X in split(repair_candidates_grouped, repair_candidates_grouped$language, drop=T)) {

    # get the textual representation of the files
    texts <- lapply(X$positions_in_utterances, repair_candidates_to_text)


    # and write them to the files
    path_prefix = file.path(prefix, 'text', X$language[1])
    unlink(path_prefix, recursive=T)
    dir.create(path_prefix, showWarnings=F, recursive=T)
    filenames <- file.path(path_prefix, X$filename)

    for(i in seq_along(texts)) writeLines(texts[[i]], con=filenames[i], sep='\n\n')
}


# ---------------------------
# Write the files
# ---------------------------
x <- filter(utterances, possible_repair)

# counts
table(utterances$possible_repair)

# repair initiator speaker type?
xtabs( ~ language, x)
#xtabs( ~ language, x) %>% xtable

# repair initiator speaker type?
xtabs( ~ stype + language, x)
#xtabs( ~ stype + language, x) %>% xtable

# languages vs age
xtabs(~child_age_category + language + stype, data=x)
#xtabs(~child_age_category + language, data=x) %>% xtable

