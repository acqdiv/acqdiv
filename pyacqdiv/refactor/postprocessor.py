""" Post-processing processes for ACQDIV corpora
"""

# TODO: implement postprocessing tasks:
#  - metadata label unification
#  - date reformatting from the all the various input formats...
#  - additionally calculated stuff like AgeInDays?
#  - morphological label unification
#  - BB's wish for MorphemeID+MorphemeID, WordID+WordID, etc.
#  - deal with age conversion, etc.
#  - add additional inferred info, e.g. Russian ends_at time stamps
#  - should we do unique word, morpheme, etc., id assignment in post-processing?

# TODO: identify body parsing errors and fixes

# TODO: infer blank cells from the (non-existent input data) existing data?
#  e.g. in Russian Alja is gender x; Sabine is role y...

from sqlalchemy.orm import sessionmaker
from database_backend import *

def db_apply(func):
    def update_session(config, cfunc):
        # cfunc is the function that connects to the db
        engine = cfunc()
        Session = sessionmaker(bind=engine)
        session = Session()
        try:
            func(session, config)
            session.commit()
        except Exception as e:
            session.rollback()
            print("Error {0}: {1}".format(type(e), e))
        finally:
            session.close()
    return update_session

def update_xml_age(session, config):
    corpus_name = config["corpus"]["corpus"]
    for db_session_entry in session.query(Session).filter(Session.corpus == corpus_name):
        sid = db_session_entry.session_id
        for row in session.query(Speaker).filter(Speaker.age != None, Speaker.parent_id == sid):
            nage = age.format_xml_age(row.age)
            if nage:
                row.age = nage
                aid = age.calculate_xml_days(nage)
                row.age_in_days = aid

def update_imdi_age(session, config):
    corpus_name = config["corpus"]["corpus"]
    for db_session_entry in session.query(Session).filter(Session.corpus == corpus_name):
        sid = db_session_entry.session_id
        for db_speaker_entry in session.query(Speaker).filter(~Speaker.birthdate.like("Un%"),
                Speaker.parent_id == sid):
            try:
                recdate = age.numerize_date(db_session_entry.date)
                bdate = age.numerize_date(db_speaker_entry.birthdate)
                ages = age.format_imdi_age(bdate, recdate)
                db_speaker_entry.age = ages[0]
                db_speaker_entry.age_in_days = ages[1]
            except Exception as e:
                    print("Couldn't calculate age of speaker {0}".format(db_speaker_entry.id))
                    print("Error: {0}".format(e))
        for db_speaker_entry in session.query(Speaker).filter(Speaker.age != None, ~Speaker.age.like("%Un%"), 
                Speaker.birthdate.like("Un%"), Speaker.parent_id == sid):
            try:
                ages = age.clean_year_only_ages(db_speaker_entry.age)
                db_speaker_entry.age = ages[0]
                db_speaker_entry.age_in_days = ages[1]
            except Exception as e:
                    print("Couldn't calculate age of speaker {0}".format(db_speaker_entry.id))
                    print("Error: {0}".format(e))

@db_apply
def update_age(session, config):
    if config["metadata"]["type"] == "IMDI":
        update_imdi_age(session, config)
    else:
        update_xml_age(session, config)


@db_apply
def unify_glosses(session, config):
    for row in session.query(Morpheme):
        old_gloss = row.gloss
        try:
            if old_gloss in config["gloss"]:
                new_gloss = config["gloss"][old_gloss]
                row.gloss = new_gloss
        except KeyError:
            print("Error: .ini file for corpus {0} does not have gloss replacement rules configured!".format(config["corpus"]["corpus"]))
            return

if __name__ == "__main__":
    cfg = ccp()
    cfg.read("Russian.ini")

    update_age(cfg)
    unify_glosses(cfg)
