""" Post-processing processes for ACQDIV corpora
"""

# TODO: implement postprocessing tasks:
#  - keep all original data and add new columns for calculated and inferred stuff
#  - morphological label unification
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
import database_backend as backend
import age
import sys
import parsers
import re

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
            print("Error {0}: {1}".format(type(e), e), file=sys.stderr)
        finally:
            session.close()
    return update_session

def update_xml_age(session, config):
    corpus_name = config["corpus"]["corpus"]
    for db_session_entry in session.query(backend.Session).filter(backend.Session.corpus == corpus_name):
        sid = db_session_entry.session_id
        for row in session.query(backend.Speaker).filter(backend.Speaker.age != None, backend.Speaker.session_id_fk == sid):
            new_age = age.format_xml_age(row.age)
            if new_age:
                row.clean_age = new_age
                aid = age.calculate_xml_days(new_age)
                row.age_in_days = aid

def update_imdi_age(session, config):
    corpus_name = config["corpus"]["corpus"]
    for db_session_entry in session.query(backend.Session).filter(backend.Session.corpus == corpus_name):
        sid = db_session_entry.session_id
        cleaned_age = re.compile('\d{1,2};\d\.\d')
        for db_speaker_entry in session.query(backend.Speaker).filter(~backend.Speaker.birthdate.like("Un%"),
                backend.Speaker.session_id_fk == sid):
            try:
                recording_date = age.numerize_date(db_session_entry.date)
                birth_date = age.numerize_date(db_speaker_entry.birthdate)
                ages = age.format_imdi_age(birth_date, recording_date)
                db_speaker_entry.clean_age = ages[0]
                db_speaker_entry.age_in_days = ages[1]
            except Exception as e:
                    print("Couldn't calculate age of speaker {0}".format(db_speaker_entry.id), file=sys.stderr)
                    print("Error: {0}".format(e), file=sys.stderr)
        for db_speaker_entry in session.query(backend.Speaker).filter(backend.Speaker.age != None, ~backend.Speaker.age.like("%Un%"), 
                backend.Speaker.birthdate.like("Un%"), backend.Speaker.session_id_fk == sid):
            if not cleaned_age.fullmatch(db_speaker_entry.age):
                try:
                    ages = age.clean_year_only_ages(db_speaker_entry.age)
                    db_speaker_entry.clean_age = ages[0]
                    db_speaker_entry.age_in_days = ages[1]
                except Exception as e:
                        print("Couldn't calculate age of speaker {0}".format(db_speaker_entry.id), file=sys.stderr)
                        print("Error: {0}".format(e), file=sys.stderr)

@db_apply
def update_age(session, config):
    if config["metadata"]["type"] == "IMDI":
        update_imdi_age(session, config)
    else:
        update_xml_age(session, config)

#WARNING: UNFINISHED CODE // DO NOT CALL
#TODO
def apply_gloss_regex(session, config):
    regex = re.compile(config["gloss"]["regex"])
    for db_session_entry in session.query(backend.Session).filter(backend.Session.corpus == corpus_name):
        sid = db_session_entry.session_id
#        for row in session.query(backend.Morpheme).filter(

@db_apply
def unify_glosses(session, config):
    corpus_name = config["corpus"]["corpus"]
    for row in session.query(backend.Morpheme).filter(backend.Morpheme.corpus == corpus_name):
        old_gloss = None
        if row.gloss:
            old_gloss = row.gloss
        elif row.gloss_target:
            old_gloss = row.gloss_target
        elif row.pos:
            old_gloss = row.pos
        elif row.pos_target:
            old_gloss = row.pos_target
        try:
            if old_gloss in config["gloss"]:
                new_gloss = config["gloss"][old_gloss]
                # TODO:
                # this is a debug print to find out what is and isn't getting replaced
                # we need to automate this
                # print(old_gloss, new_gloss)
                row.clean_gloss = new_gloss
        except KeyError:
            print("Error: .ini file for corpus {0} does not have gloss replacement rules properly configured!".format(config["corpus"]["corpus"]), file=sys.stderr)
            return

if __name__ == "__main__":
    
    configs = ['Chintang.ini', 'Cree.ini', 'Indonesian.ini', 'Inuktitut.ini', 'Japanese_Miyata.ini',
              'Japanese_MiiPro.ini', 'Russian.ini', 'Sesotho.ini', 'Turkish.ini']

    engine = backend.db_connect()
    cfg = parsers.CorpusConfigParser()
    for config in configs:
        cfg.read(config)
        print("Postprocessing database entries for {0}...".format(config.split(".")[0]))
        update_age(cfg, engine)
        unify_glosses(cfg, engine)


#normalizing roles section
@db_apply
def unifyRoles(session, config):
    #lists of roles which have to be recognized
    corpus_name = config["corpus"]["corpus"]
    linguists = ["collector", "researcher", "investigator", "annotator","observer"]
    helper = ["helper", "facilitator"]
    for a_session in session.query(backend.Session).filter(backend.Session.corpus == corpus_name):
        #we iterate through every session of current corpus
        sessionID = a_session.session_id
        for row in session.query(backend.Speaker).filter(backend.Speaker.session_id_fk == sessionID):
            #we iterate through every row of current session, looking at table "Speaker"
            currRole = row.role
            #finding out what kind of role we have and map it to equivalent normalized role
            if "target" in currRole.lower() or "focus" in currRole.lower():
                newRole = "target_child"
            elif len([item for item in linguists if item in currRole.lower()]) >= 1:
                #condition "complicated" because there are roles that contain multiple words
                newRole = "linguist"
            elif len([item for item in helper if item in currRole.lower()]) >= 1:
                newRole = "helper"
            else:
                newRole = "others/non-humans"
            #writing normalized role into column "normalized_role"
            row.normalized_role = newRole


