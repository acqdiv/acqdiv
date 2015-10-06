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
        for row in session.query(backend.Speaker).filter(backend.Speaker.age_raw != None, backend.Speaker.session_id_fk == sid):
            new_age = age.format_xml_age(row.age_raw)
            if new_age:
                row.age = new_age
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
                # db_speaker_entry.clean_age = ages[0]
                db_speaker_entry.age = ages[0]
                db_speaker_entry.age_in_days = ages[1]
            except Exception as e:
                    print("Couldn't calculate age of speaker {0}".format(db_speaker_entry.id), file=sys.stderr)
                    print("Error: {0}".format(e), file=sys.stderr)
        for db_speaker_entry in session.query(backend.Speaker).filter(backend.Speaker.age_raw != None, ~backend.Speaker.age_raw.like("%Un%"),
                backend.Speaker.birthdate.like("Un%"), backend.Speaker.session_id_fk == sid):
            if not cleaned_age.fullmatch(db_speaker_entry.age_raw):
                try:
                    ages = age.clean_year_only_ages(db_speaker_entry.age_raw)
                    db_speaker_entry.age = ages[0]
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

#normalizing roles section
@db_apply
def unify_roles(session, config):
    #lists of roles which have to be recognized
    corpus_name = config["corpus"]["corpus"]
    linguists = ["collector", "researcher", "investigator", "annotator", "observer"]
    helper = ["helper", "facilitator"]
    for a_session in session.query(backend.Session).filter(backend.Session.corpus == corpus_name):
        #we iterate through every session of current corpus
        session_id = a_session.session_id
        for row in session.query(backend.Speaker).filter(backend.Speaker.session_id_fk == session_id):
            #we iterate through every row of current session, looking at table "Speaker"
            curr_role = row.role_raw
            #finding out what kind of role we have and map it to equivalent normalized role
            if "target" in curr_role.lower() or "focus" in curr_role.lower():
                new_role = "target_child"
            elif len([item for item in linguists if item in curr_role.lower()]) >= 1:
                #condition "complicated" because there are roles that contain multiple words
                new_role = "linguist"
            elif len([item for item in helper if item in curr_role.lower()]) >= 1:
                new_role = "helper"
            else:
                new_role = "others"
            #writing normalized role into column "normalized_role"
            row.role = new_role

@db_apply
def unify_gender(session,config):
    table = session.query(backend.Speaker)
    for row in table:
        if row.gender_raw == None:
            row.gender = 'unspecified'
        elif row.gender_raw.lower() == 'female':
            row.gender = 'female'
        elif row.gender_raw.lower() == 'male':
            row.gender = 'male'
        else:
            row.gender = 'unspecified'

#deleting duplication, duplicate then when name and birthdate the same
@db_apply
def unique_speaker(session, config):
    #to keep speaker unique
    unique_name_date = set()
    table = session.query(backend.Unique_Speaker)
    for row in table:
        curr_tuple = (row.name,row.birthdate)
        #if name-birthdate combi already exists, delete row
        if curr_tuple in unique_name_date:
            session.delete(session.query(backend.Unique_Speaker).filter_by(id=row.id).first())
        else:
            unique_name_date.add(curr_tuple)

        to_get_gender = session.query(backend.Speaker).filter(backend.Speaker.name == row.name)
        row.gender = to_get_gender[0].gender

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
