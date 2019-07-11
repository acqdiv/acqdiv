"""Encrypt the ACQDIV-DB"""

import sqlalchemy as sa
import hashlib
import acqdiv.database.database_backend as db

engine = None
conn = None
metadata = None

# Corpora affected
exceptions = ['Chintang', 'Inuktitut', 'Russian', 'Turkish', 'Yucatec']


def setup(args):
    """Global database setup."""
    global engine, conn, metadata

    # Testing vs production database.
    if args.t:
        engine = sa.create_engine('sqlite:///database/test.sqlite3')
        metadata = sa.MetaData(bind=engine)
        metadata.reflect(engine)
    else:
        engine = sa.create_engine('sqlite:///database/acqdiv.sqlite3')
    conn = engine.connect()


def main(args):
    """Process the database."""
    setup(args)
    with engine.begin() as conn:
        conn.execute('PRAGMA synchronous = OFF')
        conn.execute('PRAGMA journal_mode = MEMORY')
        conn.execution_options(compiled_cache={})

        _drop_columns()
        _encrypt()


def _drop_columns():
    """Empty columns."""
    morphemes = {'type':'', 'warning':''}
    stmt = db.Morpheme.__table__.update().where(db.Morpheme.__table__.c.corpus.in_(exceptions)).values(morphemes)
    conn.execute(stmt)

    sessions = {'source_id':'', 'date':''}
    stmt = db.Session.__table__.update().where(db.Session.__table__.c.corpus.in_(exceptions)).values(sessions)
    conn.execute(stmt)

    speakers = {'speaker_label':'', 'name':'', 'age_raw':'', 'age':'', 'gender_raw':'', 'gender':'', 'role_raw':'',
                'languages_spoken':'', 'birthdate':''}
    stmt = db.Speaker.__table__.update().where(db.Speaker.__table__.c.corpus.in_(exceptions)).values(speakers)
    conn.execute(stmt)

    uniquespeakers = {'speaker_label':'', 'name':'', 'birthdate':'', 'gender':'', 'corpus':''}
    stmt = db.UniqueSpeaker.__table__.update().where(db.UniqueSpeaker.__table__.c.corpus.in_(exceptions)).values(uniquespeakers)
    conn.execute(stmt)

    utterances = {'source_id':'', 'speaker_id_fk':'', 'speaker_label':'', 'addressee':'', 'utterance_raw':'',
                  'gloss_raw':'', 'pos_raw':'', 'morpheme':'', 'translation':'', 'sentence_type':'', 'childdirected':'', 'start_raw':'', 'end_raw':'',
                  'comment':'', 'warning':'', }
    stmt = db.Utterance.__table__.update().where(db.Utterance.__table__.c.corpus.in_(exceptions)).values(utterances)
    conn.execute(stmt)

    words = {'word_actual':'', 'word_target':'', 'warning':''}
    stmt = db.Word.__table__.update().where(db.Word.__table__.c.corpus.in_(exceptions)).values(words)
    conn.execute(stmt)


def _encrypt():
    """Encrypt columns."""
    # Words
    s = sa.select([db.Word.id, db.Word.word, db.Word.corpus])
    rows = conn.execute(s)
    results = []
    for row in rows:
        if row.corpus in exceptions:
            if row.word:
                h = hashlib.sha1(row.word.encode())
                results.append({'word_id': row.id, 'word': str(h.hexdigest())})
            else:
                results.append({'word_id': row.id, 'word': None})
    rows.close()
    stmt = db.Word.__table__.update().where(db.Word.__table__.c.id == sa.bindparam('word_id')).values()
    conn.execute(stmt, results)

    # Utterances
    s = sa.select([db.Utterance.id, db.Utterance.utterance, db.Utterance.corpus])
    rows = conn.execute(s)
    results = []
    for row in rows:
        if row.corpus in exceptions:
            if row.utterance:
                result = []
                words = row.utterance.split()
                # An utterance contains multiple words delimited by space; hash each word.
                for word in words:
                    h = hashlib.sha1(word.encode())
                    result.append(str(h.hexdigest()))
                results.append({'utterance_id': row.id, 'utterance': " ".join(result)})
            else:
                results.append({'utterance_id': row.id, 'utterance': None})
    rows.close()
    stmt = db.Utterance.__table__.update().where(db.Utterance.__table__.c.id == sa.bindparam('utterance_id')).values()
    conn.execute(stmt, results)

    # Morphemes
    s = sa.select([db.Morpheme.id, db.Morpheme.morpheme, db.Morpheme.gloss_raw, db.Morpheme.pos_raw,
                   db.Morpheme.gloss, db.Morpheme.pos, db.Morpheme.corpus])
    rows = conn.execute(s)
    morphemes = []
    gloss_raw = []
    gloss = []
    pos_raw = []
    pos = []
    for row in rows:
        if row.corpus in exceptions:
            # Apparently you can't mix columns in the bulk insert in sqlalchemy.
            if row.morpheme:
                h = hashlib.sha1(row.morpheme.encode())
                morphemes.append({'morpheme_id': row.id, 'morpheme': str(h.hexdigest())})
            else:
                morphemes.append({'morpheme_id': row.id, 'morpheme': None})

            if row.gloss_raw:
                h = hashlib.sha1(row.gloss_raw.encode())
                gloss_raw.append({'morpheme_id': row.id, 'gloss_raw': str(h.hexdigest())})
            else:
                gloss_raw.append({'morpheme_id': row.id, 'morpheme': None})

            if row.gloss:
                h = hashlib.sha1(row.gloss.encode())
                gloss.append({'morpheme_id': row.id, 'gloss': str(h.hexdigest())})
            else:
                gloss.append({'morpheme_id': row.id, 'gloss': None})

            if row.pos_raw:
                h = hashlib.sha1(row.pos_raw.encode())
                pos_raw.append({'morpheme_id': row.id, 'pos_raw': str(h.hexdigest())})
            else:
                pos_raw.append({'morpheme_id': row.id, 'pos_raw': None})

            if row.pos:
                h = hashlib.sha1(row.pos.encode())
                pos.append({'morpheme_id': row.id, 'pos': str(h.hexdigest())})
            else:
                pos.append({'morpheme_id': row.id, 'pos': None})
    rows.close()

    stmt = db.Morpheme.__table__.update().where(db.Morpheme.__table__.c.id == sa.bindparam('morpheme_id')).values()
    conn.execute(stmt, morphemes)

    stmt = db.Morpheme.__table__.update().where(db.Morpheme.__table__.c.id == sa.bindparam('morpheme_id')).values()
    conn.execute(stmt, gloss_raw)

    stmt = db.Morpheme.__table__.update().where(db.Morpheme.__table__.c.id == sa.bindparam('morpheme_id')).values()
    conn.execute(stmt, gloss)

    stmt = db.Morpheme.__table__.update().where(db.Morpheme.__table__.c.id == sa.bindparam('morpheme_id')).values()
    conn.execute(stmt, pos_raw)

    stmt = db.Morpheme.__table__.update().where(db.Morpheme.__table__.c.id == sa.bindparam('morpheme_id')).values()
    conn.execute(stmt, pos)


if __name__ == "__main__":
    import time
    import argparse

    start_time = time.time()

    p = argparse.ArgumentParser()
    p.add_argument('-t', action='store_true')
    p.add_argument('-s', action='store_true')
    args = p.parse_args()

    main(args)

    print("%s seconds --- Finished" % (time.time() - start_time))
