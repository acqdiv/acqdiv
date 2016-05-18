sqlite3 -header -csv test.sqlite3 "select * from morphemes left join words on morphemes.word_id_fk = words.id left join utterances on morphemes.utterance_id_fk = utterances.id left join speakers on morphemes.session_id_fk = speakers.id left join sessions on morphemes.session_id_fk = sessions.id left join uniquespeakers on uniquespeaker_id_fk = uniquespeakers.id;" > test.csv

csvformat -T test.csv > final.tsv
csvcut -c 1,2,4,5 test.csv > final.csv

