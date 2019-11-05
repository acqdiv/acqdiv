#!/bin/bash
sqlite3 production.sqlite3 << EOF
.headers on
.mode csv
.output production.csv
SELECT 
	utterances.id as utterance_id, 
	utterances.source_id as utterance_source_id,
	utterances.corpus,
	utterances.language as corpus_language,
	utterances.speaker_label,
	speakers.id as speaker_id,
	speakers.uniquespeaker_id_fk as uniquespeaker_id,
	speakers.name,
	speakers.age_raw,
	speakers.age,
	speakers.age_in_days,
	speakers.gender,
	speakers.role,
	speakers.macrorole,
	speakers.birthdate,
	utterances.addressee,
	utterances.sentence_type,	
	utterances.childdirected,
	utterances.utterance,
	utterances.translation,
	utterances.morpheme as utterance_morphemes,
	utterances.gloss_raw as utterance_glosses_raw,
	utterances.pos_raw as utterances_poses_raw,
	utterances.start,
	utterances.end,
	utterances.comment,
	words.id as word_id,
	words.word_language,
	words.word,
	words.pos as pos_word_stem,
	words.word_actual,
	words.word_target,
	morphemes.id as morpheme_id,
	morphemes.type as morpheme_type,
	morphemes.morpheme,
	morphemes.gloss_raw,
	morphemes.gloss,
	morphemes.pos_raw,
	morphemes.pos,
	morphemes.morpheme_language,
	sessions.id as session_id,
	sessions.source_id as session_source_id,
	sessions.date
FROM utterances
LEFT JOIN words ON utterances.id = words.utterance_id_fk
LEFT JOIN morphemes ON words.id = morphemes.word_id_fk
LEFT JOIN sessions ON utterances.session_id_fk = sessions.id
LEFT JOIN speakers ON utterances.speaker_id_fk = speakers.id
ORDER BY sessions.id, utterances.id, words.id, morphemes.id;
EOF