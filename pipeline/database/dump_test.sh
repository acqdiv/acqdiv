#!/bin/bash
sqlite3 test.sqlite3 << EOF
.headers on
.mode csv
.output test.csv
select
	s.id as session_id,
	s.source_id as session_source_id,
	s.date,
	u.id as utterance_id,
	u.source_id as utterance_source_id,
	u.corpus,
	u.language as language,
	u.speaker_label,
	sp.id as speaker_id,
	sp.uniquespeaker_id_fk as uniquespeaker_id,
	sp.name,
	sp.age_raw,
	sp.age,
	sp.age_in_days,
	sp.gender,
	sp.role,
	sp.macrorole,
	sp.birthdate,
	u.addressee,
	u.childdirected,
	u.utterance,
	u.translation,
	u.morpheme as utterance_morphemes,
	u.gloss_raw as utterance_glosses_raw,
	u.pos_raw as utterances_poses_raw,
	u.start,
	u.end,
	u.comment,
	w.id as word_id,
	w.word,
	w.pos as pos_word_stem,
	w.word_actual,
	w.word_target,
	m.id as morpheme_id,
	m.type as morpheme_type,
	m.morpheme,
	m.gloss_raw,
	m.gloss,
	m.pos_raw,
	m.pos,
	m.morpheme_language
from morphemes as m
	join utterances as u on m.utterance_id_fk = u.id
	left join words as w on m.word_id_fk = w.id
	join sessions s on u.session_id_fk = s.id
	left join speakers sp on u.speaker_id_fk = sp.id
	left join uniquespeakers on sp.uniquespeaker_id_fk = uniquespeakers.id
order by s.id, u.id, w.id, m.id;
EOF