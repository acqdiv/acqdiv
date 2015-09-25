""" Post-processing processes for ACQDIV corpora
"""

# TODO: implement postprocessing tasks:
#  - keep all original data and add new columns for calculated and inferred stuff
#  - morphological label unification
#  - calculate age (date reformatting ("P25Y", etc. ??)
#  - calculate age_in_days
#  - normalize all relevant column data, e.g.:
#    role: target_child, Target Child, Target_child, etc. --> Target_Child (per CHAT specification!)
#    gender: female, Female, etc. -> Female
#    language: check that the language codes are correct (ie valid)
#    birthday: is this normalize-able? is it important?
#  - unique word, morpheme, etc., id assignment in post-processing, i.e.
#    assign a unique ID to each unique word, morpheme, etc., and then populate a new column
#  - remove these bullet points when you've implemented this stuff above, please!

# for the future:
#  - add additional inferred info, e.g. Russian ends_at time stamps
#  - BB's wish for MorphemeID+MorphemeID, WordID+WordID, etc.
#  - infer gender, etc., from things like "Grandmother" once these labels have been unified
#  - infer blank cells from the (non-existent input data) existing data?
#    e.g. in Russian Alja is gender x; Sabine is role y...

# TODO: identify body parsing errors and fixes

from sqlalchemy.orm import sessionmaker
from database_backend import *
import age

def db_apply(func):
    def update_session(config, engine):
        # cfunc is the function that connects to the db
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
        for row in session.query(Speaker).filter(Speaker.age != None, Speaker.session_id_fk == sid):
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
                Speaker.session_id_fk == sid):
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
                Speaker.birthdate.like("Un%"), Speaker.session_id_fk == sid):
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
