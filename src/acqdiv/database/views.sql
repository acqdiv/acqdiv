CREATE VIEW IF NOT EXISTS all_data
AS
SELECT
corpora.id as corpus,
corpora.language,
sessions.id as session_id,
sessions.source_id as session_source_id,
sessions.date,
speakers.id as speaker_id,
uniquespeakers.id as uniquespeaker_id,
uniquespeakers.speaker_label,
uniquespeakers.name,
uniquespeakers.birthdate,
speakers.age_raw,
speakers.age,
speakers.age_in_days,
uniquespeakers.gender,
speakers.role,
speakers.macrorole,
utterances.addressee_id_fk as addressee_id,
utterances.id as utterance_id,
utterances.source_id as utterance_source_id,
utterances.utterance,
utterances.morpheme as utterance_morphemes,
utterances.gloss_raw as utterance_glosses_raw,
utterances.pos_raw as utterances_poses_raw,
utterances.translation,
utterances.sentence_type,
utterances.childdirected,
utterances.start,
utterances.end,
utterances.comment,
words.id as word_id,
words.word,
words.pos as pos_word_stem,
words.pos_ud,
words.word_actual,
words.word_target,
words.language as word_language,
morphemes.id as morpheme_id,
morphemes.morpheme,
morphemes.gloss_raw,
morphemes.gloss,
morphemes.pos_raw,
morphemes.pos as pos_morpheme,
morphemes.language as morpheme_language,
morphemes.type as morpheme_type
FROM utterances
LEFT JOIN words ON utterances.id = words.utterance_id_fk
LEFT JOIN morphemes ON words.id = morphemes.word_id_fk
LEFT JOIN sessions ON utterances.session_id_fk = sessions.id
LEFT JOIN corpora on sessions.corpus = corpora.id
LEFT JOIN speakers ON utterances.speaker_id_fk = speakers.id
LEFT JOIN uniquespeakers ON speakers.uniquespeaker_id_fk = uniquespeakers.id
ORDER BY sessions.id, utterances.id, words.id, morphemes.id
;