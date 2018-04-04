#!/bin/bash
sqlite3 acqdiv_corpus_2017-09-16.sqlite3 << EOF
.headers on
.mode csv
.output acqdiv_corpus_2017-09-16.csv
select * 
from morphemes as m
join utterances as u on m.utterance_id_fk = u.id
left join words as w on m.word_id_fk = w.id
join sessions s on u.session_id_fk = s.id
left join speakers sp on u.speaker_id_fk = sp.id
left join uniquespeakers on sp.uniquespeaker_id_fk = uniquespeakers.id
order by s.id, u.id, w.id, m.id;
EOF