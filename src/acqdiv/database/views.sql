CREATE VIEW IF NOT EXISTS vmorphemes
AS 
    SELECT corpora.id AS corpus, morphemes.*
    FROM morphemes, utterances, sessions, corpora
    WHERE morphemes.utterance_id_fk = utterances.id
        AND utterances.session_id_fk = sessions.id
        AND sessions.corpus = corpora.id
;


CREATE VIEW IF NOT EXISTS vwords
AS 
    SELECT corpora.id AS corpus, words.*
    FROM words, utterances, sessions, corpora
    WHERE words.utterance_id_fk = utterances.id
        AND utterances.session_id_fk = sessions.id
        AND sessions.corpus = corpora.id
;


CREATE VIEW IF NOT EXISTS vutterances
AS
    SELECT corpora.id AS corpus, utterances.*
    FROM utterances, sessions, corpora
    WHERE utterances.session_id_fk = sessions.id
        AND sessions.corpus = corpora.id
;


CREATE VIEW IF NOT EXISTS vsessions
AS
    SELECT DISTINCT sessions.*, uniquespeakers.id AS target_child_fk
    FROM sessions, speakers, uniquespeakers
    WHERE sessions.id = speakers.session_id_fk
        AND speakers.uniquespeaker_id_fk = uniquespeakers.id
		AND speakers.role = 'Target_Child'
;


CREATE VIEW IF NOT EXISTS vspeakers
AS
    SELECT speakers.*,
        uniquespeakers.corpus,
        uniquespeakers.birthdate,
        uniquespeakers.gender,
        uniquespeakers.name,
        uniquespeakers.speaker_label
    FROM speakers, uniquespeakers
    WHERE speakers.uniquespeaker_id_fk = uniquespeakers.id
;


CREATE VIEW IF NOT EXISTS vuniquespeakers
AS
    SELECT *
    FROM uniquespeakers
;