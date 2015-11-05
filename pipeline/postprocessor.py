""" Post-processing processes for ACQDIV corpora
"""

# TODO: implement postprocessing tasks:
#  - normalize all relevant column data, e.g.:
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
from sqlalchemy import create_engine
import database_backend as backend
from parsers import CorpusConfigParser
import age
import sys
import re
import time
import configparser

def db_apply(func):
    """Wrapper for functions that access the database.

    Args:
        func: A function that takes a SQLalchemy session and a configparser object as arguments.

    Returns:
        A function that takes a configparser object and a SQLalchemy engine as arguments and 
        wraps func with the logic for connecting to and modifying the database.
    """
    def update_session(config, engine):
        """Function to connect to and modify the ACQDIV database. This is a wrapper returned by db_apply.

        This function calls the SQLalchemy sessionmaker to create a database session,
        then calls the function it wraps with the config and the session.
        Finally it closes the connection again.

        Args:
            config: A configparser object. The config should be the contents of a corpus-specific .ini file.
            engine: A SQLalchemy engine object. This is the connection to the ACQDIV database.
        """
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
    """Function to process speaker ages in Chat XML corpora.
    
    Finds all speakers from the corpus in the config and calls methods from age.py to
    fill in the age and age_in_days columns.

    Args:
        session: SQLalchemy session object.
        config: configparser object containing the configuration for the current corpus.
    """
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
    """Function to process speaker ages in IMDI corpora.

    Finds all the recording sessions in the corpus in the config, then, for each speaker
    in the session:

    First attempts to calculate ages from the speaker's birth date and the session's
    recording date. For speakers where this fails, looks for speakers that already
    have a properly formatted age, transfers this age from the age_raw column to the
    age column and calculates age_in_days from it.

    Finally, it looks for speakers that only have an age in years and does the same.

    Args:
        session: SQLalchemy session object.
        config: configparser object containing the configuration for the current corpus.
    """
    corpus_name = config["corpus"]["corpus"]

    for db_session_entry in session.query(backend.Session).filter(backend.Session.corpus == corpus_name):
        sid = db_session_entry.session_id
        cleaned_age = re.compile('\d{1,2};\d{1,2}\.\d')

        for db_speaker_entry in session.query(backend.Speaker).filter(~backend.Speaker.birthdate.like("Un%"),
                ~backend.Speaker.birthdate.like("None"),
                backend.Speaker.session_id_fk == sid):
            try:
                recording_date = age.numerize_date(db_session_entry.date)
                birth_date = age.numerize_date(db_speaker_entry.birthdate)
                ages = age.format_imdi_age(birth_date, recording_date)
                db_speaker_entry.age = ages[0]
                db_speaker_entry.age_in_days = ages[1]
            except Exception as e:
                    print("Couldn't calculate age of speaker {0}".format(db_speaker_entry.id), file=sys.stderr)
                    print("Error: {0}".format(e), file=sys.stderr)

        for db_speaker_entry in session.query(backend.Speaker).filter(backend.Speaker.age_raw.like("%;%.%")):
                db_speaker_entry.age = db_speaker_entry.age_raw
                db_speaker_entry.age_in_days = age.calculate_xml_days(db_speaker_entry.age_raw)

        for db_speaker_entry in session.query(backend.Speaker).filter(~backend.Speaker.age_raw.like("None"),
                ~backend.Speaker.age_raw.like("%Un%"),
                backend.Speaker.age == None,
                backend.Speaker.session_id_fk == sid):
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
    """Helper function for age unification.

    Checks the config for the metadata format of the corpus,
    then calls the appropriate function.

    Args:
        session: SQLalchemy session object.
        config: configparser object containing the configuration for the current corpus. This needs to specify the metadata format.
    """
    if config["metadata"]["type"] == "IMDI":
        update_imdi_age(session, config)
    else:
        update_xml_age(session, config)

@db_apply
def apply_gloss_regexes(session, config):
    """Function to apply regex substitutions to the glosses of morphemes in the database.

    Takes regexes specified in the config and applies them to all the morphemes belonging to the
    current corpus.

    Args:
        session: SQLalchemy session object.
        config: configparser object containing the configuration for the current corpus. This needs to specify the metadata format.
    """
    corpus_name = config["corpus"]["corpus"]
    regexes = config["regex"].items() 
    ssq = session.query(backend.Morpheme).filter(backend.Morpheme.corpus == corpus_name)
    for item in regexes:
        pattern = re.compile(item[0][1:-1])
        replacement = item[1][1:-1]
        for row in ssq:
            try:
                if corpus_name == "Russian":
                    row.gloss = re.sub(pattern, replacement, row.gloss_raw)
                else:
                    row.gloss = re.sub(pattern, replacement, row.gloss)
            except TypeError:
                continue
            except Exception as e:
                print("Error applying gloss regex {1} in {0}.ini: {2}".format(corpus_name, item, e), file=sys.stderr)

@db_apply
def unify_gloss_labels(session, config):
    """Performs simple key-value substitution on morphological glosses in the database.

    This function iterates through all morpheme rows belonging to the current corpus,
    then searches for the gloss from the gloss_raw column in the "gloss" section of the config.

    If the gloss is found, the gloss column is filled with the value from the config.
    Otherwise, the raw gloss is carried over unchanged.

    Args:
        session: SQLalchemy session object.
        config: configparser object containing the configuration for the current corpus. This needs to specify the metadata format.
    """
    corpus_name = config["corpus"]["corpus"]
    for row in session.query(backend.Morpheme).filter(backend.Morpheme.corpus == corpus_name):
        old_gloss = None
        if corpus_name == "Russian":
            old_gloss = row.gloss
        else:
            old_gloss = row.gloss_raw
        try:
            if old_gloss in config["gloss"]:
                new_gloss = config["gloss"][old_gloss]
                # TODO:
                # this is a debug print to find out what is and isn't getting replaced
                # we need to automate this
                # print(old_gloss, new_gloss)
                row.gloss = new_gloss
            else:
                row.gloss = old_gloss
        except KeyError:
            print("Error: .ini file for corpus {0} does not have gloss replacement rules properly configured!".format(config["corpus"]["corpus"]), file=sys.stderr)
            return

def unify_glosses(config, engine):
    """Helper function for unifying glosses.

    For most corpora, the regexes must operate on glosses already substituted.
    However, for Russian, the regex substitutions must occur first.
    This function checks if the corpus name in the config is Russian or not
    and applies the functions in the corresponding order.


    Args:
        config: configparser object containing the configuration for the current corpus. This needs to specify the metadata format.
        engine: SQLalchemy engine object.
    """
    if config["corpus"]["corpus"] == "Russian":
        apply_gloss_regexes(config, engine)
        unify_gloss_labels(config, engine)
    else:
        unify_gloss_labels(config, engine)
        apply_gloss_regexes(config, engine)

@db_apply
def unify_roles(session,config):
    """Function to unify speaker roles.

    Each corpora has its own set of speaker roles. This function uses
    "role_mapping.ini" to assign an unified role to each speaker according
    to the mappings in role_mapping.ini. The mapping is either based on the original
    role or the speaker_label (depending on how the corpora handles role encoding).
    The role column in the speaker table contains the unified roles.

    Args:
        config: configparser object containing the configuration for the current corpus. This needs to specify the metadata format.
        engine: SQLalchemy engine object.
    """
    table = session.query(backend.Speaker)
    cfg_mapping = configparser.ConfigParser()
    #option names resp. keys case-sensitive
    cfg_mapping.optionxform = str
    cfg_mapping.read("role_mapping.ini")
    for row in table:
        row.role = cfg_mapping['role_mapping'][row.role_raw]
        if row.role == "Unknown" and row.language in cfg_mapping:
            try:
                row.role = cfg_mapping[row.language][row.speaker_label]
            except KeyError:
                pass
        elif row.role in ["Adult", "Child", "old","Teenager"] and row.age_in_days != None:
            row.role = "Unknown"
        elif row.role in ["Boy", "Girl", "Female", "Male"] and row.gender_raw != None:
            row.role = "Unknown"

@db_apply
def unify_gender(session, config):
    """Function to unify speaker genders.

    There are different ways to write a speaker's gender. This
    function unifies the spelling. The column gender in the speakertable
    contains the unified genders.

    Args:
        config: configparser object containing the configuration for the current corpus. This needs to specify the metadata format.
        engine: SQLalchemy engine object.
    """
    table = session.query(backend.Speaker)
    for row in table:
        if row.gender_raw != None:
            if row.gender_raw.lower() == 'female':
                row.gender = 'Female'
            elif row.gender_raw.lower() == 'male':
                row.gender = 'Male'
            else:
                row.gender = "Unspecified"
        else:
            row.gender = "Unspecified"

@db_apply
def macrorole(session,config):
    """Function to define macrorole resp. age category.

    This function assigns an age category to each speaker. If there is
    no information on age available it uses "role_mappings.ini" to define 
    which age category a speaker belongs to. The mapping is based on either
    the speaker's original role or speaker_label (depending on how the corpora
    handles role encoding).

    Args:
        config: configparser object containing the configuration for the current corpus. This needs to specify the metadata format.
        engine: SQLalchemy engine object.
    """
    table = session.query(backend.Speaker)
    cfg_mapping = configparser.ConfigParser()
    #option names resp. keys case-sensitive
    cfg_mapping.optionxform = str
    cfg_mapping.read("role_mapping.ini")
    for row in table:
        if row.role == "Target_Child":
            macro = "Target_Child"
        elif row.age_in_days != None:
            if row.age_in_days <= 4380:
                macro = "Child"
            else:
                macro = "Adult"
        else:
            try:
                macro = cfg_mapping['macrorole_mapping'][row.role_raw]
            except KeyError:
                try:
                    macro = cfg_mapping['macrorole_mapping'][row.speaker_label]
                except KeyError:
                    macro = "Unknown"
        row.macrorole = macro

@db_apply
def unique_speaker(session, config):
    """Function to create a table containing every unique speaker from all corpora.

    Queries the speaker table in the database and extracts non-session-specific data
    for every unique speaker.

    Uniqueness is determined by a combination of speaker label, name, and birthdate.

    Args:
        session: SQLalchemy session object.
        config: configparser object containing the configuration for the current corpus.
    """
    # create a table of unique speakers
    unique_speaker_entries = []
    unique_name_date_label = set()
    table = session.query(backend.Speaker)

    for db_speaker_entry in table:
        unique_tuple = (db_speaker_entry.name, db_speaker_entry.birthdate,db_speaker_entry.speaker_label)
        if unique_tuple not in unique_name_date_label:
            unique_name_date_label.add(unique_tuple)
            d = {}
            d['speaker_label'] = db_speaker_entry.speaker_label
            d['name'] = db_speaker_entry.name
            d['birthdate'] = db_speaker_entry.birthdate
            d['gender'] = db_speaker_entry.gender
            d['language'] = db_speaker_entry.language
            d['macrorole'] = db_speaker_entry.macrorole
            unique_speaker_entries.append(backend.Unique_Speaker(**d))

    session.add_all(unique_speaker_entries)

@db_apply
def unify_indonesian_labels(session, config):
    """Function to match the labels of Indonesian speakers with the labels in the Indonesian utterances.
        
    Labels in the Indonesian utterances are longer and more specific than those in the metadata files.
    This function changes the labels in the speaker table to the corresponding labels in the utterances.
    For most speakers, this is done by appending the first three letters of the session label to the 
    speaker label. For those that are coded in the original metadata files as EXP, their identity is determined by their
    name and the appropriate label assigned as coded in the config.

    Finally, some specifically excluded labels (also in the config) are not changed at all.

    Args:
        session: SQLalchemy session object.
        config: configparser object containing the configuration for the current corpus.
    """
    for db_session_entry in session.query(backend.Session).filter(backend.Session.corpus == "Indonesian"):
        session_id = db_session_entry.session_id
        session_set = session_id[0:3]
        for db_speaker_entry in session.query(backend.Speaker).filter(backend.Speaker.session_id_fk == session_id):
            if db_speaker_entry.name in config["exp_labels"]:
                db_speaker_entry.speaker_label = config["exp_labels"][db_speaker_entry.name]
            elif db_speaker_entry.speaker_label not in config["excluded_labels"] and db_speaker_entry.speaker_label[-3:] != session_set:
                db_speaker_entry.speaker_label = db_speaker_entry.speaker_label + session_set
@db_apply
def unify_timestamps(session, config):
    """Helper function to change utterance timestamps to a consistent format.

    This function queries the database for all timestamps and then calls the
    unify_timestamps function from age.py to unify the format.

    Args:
        session: SQLalchemy session object.
        config: configparser object containing the configuration for the current corpus.
    """
    corpus_name = config["corpus"]["corpus"]
    for db_session_entry in session.query(backend.Session).filter(backend.Session.corpus == corpus_name):
        sid = db_session_entry.session_id
        for db_utterance_entry in session.query(backend.Utterance).filter(backend.Utterance.start_raw.isnot(None), 
                backend.Utterance.session_id_fk == sid):
            try:
                db_utterance_entry.start = age.unify_timestamps(db_utterance_entry.start_raw)
                db_utterance_entry.end = age.unify_timestamps(db_utterance_entry.end_raw)
            except Exception as e:
                print("Error unifying timestamps in corpus {}: {}".format(corpus_name, e))

if __name__ == "__main__":
    start_time = time.time()
    
    configs = ['Chintang.ini', 'Cree.ini', 'Indonesian.ini', 'Inuktitut.ini', 'Japanese_Miyata.ini',
              'Japanese_MiiPro.ini', 'Russian.ini', 'Sesotho.ini', 'Turkish.ini']
    engine = backend.db_connect()
    cfg = CorpusConfigParser()
    for config in configs:
        cfg.read(config)
        print("Postprocessing database entries for {0}...".format(config.split(".")[0]))
        update_age(cfg, engine)
        unify_timestamps(cfg, engine)
        unify_glosses(cfg, engine)
        unify_gender(cfg, engine)
    #    if config == 'Indonesian.ini':
    #        unify_indonesian_labels(cfg, engine)
    #print("Creating Unique Speaker table...")
    unify_roles(cfg, engine)
    macrorole(cfg,engine)
    unique_speaker(cfg, engine)
        
    print("--- %s seconds ---" % (time.time() - start_time))
