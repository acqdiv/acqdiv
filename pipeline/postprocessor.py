""" Post-processing processes on the corpora in the ACQDIV-DB.
"""

import age
import sys
import re

import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker

import database_backend as backend
from configparser import ConfigParser
from parsers import CorpusConfigParser

session = None
cleaned_age = re.compile('\d{1,2};\d{1,2}\.\d')
age_pattern = re.compile(".*;.*\..*")

def setup():
    global cfg, session
    engine = sa.create_engine('sqlite:///tests/test.sqlite3')
    # engine = sa.create_engine('sqlite:///../database/beta.sqlite3')
    meta = sa.MetaData(engine, reflect=True)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Load the role mapping.ini for unifying roles
    global roles
    roles = ConfigParser(delimiters=('='))
    roles.optionxform = str
    roles.read("role_mapping.ini")

    # Load the corpus configs
    global chintang, cree, indonesian, inuktitut, miyata, miipro, russian, sesotho, turkish, yucatec
    chintang = CorpusConfigParser()
    chintang.read("ini/Chintang.ini")
    cree = CorpusConfigParser()
    cree.read("ini/Cree.ini")
    indonesian = CorpusConfigParser()
    indonesian.read("ini/Indonesian.ini")
    inuktitut = CorpusConfigParser()
    inuktitut.read("ini/Inuktitut.ini")
    miyata = CorpusConfigParser()
    miyata.read("ini/Japanese_Miyata.ini")
    miipro = CorpusConfigParser()
    miipro.read("ini/Japanese_MiiPro.ini")
    russian = CorpusConfigParser()
    russian.read("ini/Russian.ini")
    sesotho = CorpusConfigParser()
    sesotho.read("ini/Sesotho.ini")
    turkish = CorpusConfigParser()
    turkish.read("ini/Turkish.ini")
    yucatec = CorpusConfigParser()
    yucatec.read("ini/Yucatec.ini")


def commit():
    """ Commits the dictionaries returned from parsing to the database.
    """
    try:
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def get_config(corpus_name):
    """ Return the config
    """
    if corpus_name == "Chintang":
        return chintang
    elif corpus_name == "Cree":
        return cree
    elif corpus_name == "Indonesian":
        return indonesian
    elif corpus_name == "Inuktitut":
        return inuktitut
    elif corpus_name == "Japanese_Miyata":
        return miyata
    elif corpus_name == "Japanese_MiiPro":
        return miipro
    elif corpus_name == "Russian":
        return russian
    elif corpus_name == "Sesotho":
        return sesotho
    elif corpus_name == "Turkish_KULLD":
        return turkish
    elif corpus_name == "Yucatec":
        return yucatec
    else:
        raise Exception


def postprocessor():
    """ Postprocessing postprocesses.
    """
    # Update database tables
    print("Processing utterances...")
    process_utterances()
    print("Processing speakers...")
    process_speakers()
    print("Processing morphemes...")
    process_morphemes()

    # Additional data
    # TODO: duplicate primary keys to additional roles


def clean_tlbx_pos_morphemes(row):
    """ Function that cleans pos and morphemes in Chintang and Indonesian.
        It also cleans the morpheme (for Chintang and Russian) and gloss_raw (Indonesian) column in the utterances
        table because cleaning them within the Toolbox parser messes up the morphemes table.

    Args:
        session: SQLAlchemy session object.
        config: CorpusConfigParser object.
    """
    # if config["corpus"]["corpus"] == "Chintang":
    # get pfx and sfx

    if row.corpus == "Chintang":
        try:
            if row.pos_raw.startswith('-'):
                row.pos = 'sfx'
                row.pos_raw = 'sfx'
            elif row.pos_raw.endswith('-'):
                row.pos = 'pfx'
                row.pos_raw = 'pfx'
            else:
                row.pos_raw = row.pos_raw.strip('-')
                row.pos = row.pos_raw
            # strip '-' from morphemes and gloss_raw
            row.morpheme = row.morpheme.strip('-')
            row.gloss_raw = row.gloss_raw.strip('-')
            row.gloss = row.gloss.strip('-')
        except AttributeError:
            pass

    if row.corpus == "Indonesian":
        try:
            if row.gloss_raw.startswith('-'):
                row.pos = 'sfx'
                row.gloss_raw = row.gloss_raw.strip('-')
            elif row.gloss_raw.endswith('-'):
                row.pos = 'pfx'
                row.gloss_raw = row.gloss_raw.strip('-')
            elif row.gloss_raw == '???':
                row.pos = '???'
            else:
                row.pos = 'stem'
            row.morpheme = row.morpheme.strip('-')
        except AttributeError:
            pass
        except TypeError:
            pass


def process_morphemes():
    table = session.query(backend.Morpheme)
    for row in table:
        # Clean up affix markers "-"; assign sfx, pfx, stem.
        if row.corpus == "Chintang" or row.corpus == "Indonesian":
            clean_tlbx_pos_morphemes(row)
        # Key-value substitutions for morphological glosses and parts-of-speech
        unify_label(row)
        # Infer the word's part-of-speech from the morphemes
        get_word_pos(row)


def get_word_pos(row):
    """
    Populates word POS from morphemes table by taking the first non "pfx" or "sfx" value.

    # TODO: Insert some debugging here if the labels are missing?
    """
    # get word_id_fk
    word_id_fk = row.word_id_fk
    pos = row.pos

    table = session.query(backend.Word).filter(backend.Word.id==word_id_fk)
    for result in table:
        if not pos in ["sfx", "pfx"]:
            result.pos = pos


def process_utterances():
    table = session.query(backend.Utterance)
    for row in table:
        # Unify the time stamps
        if row.start_raw: #.isnot(None):
            try:
                row.start = age.unify_timestamps(row.start_raw)
                row.end = age.unify_timestamps(row.end_raw)
            except Exception as e:
                # TODO: log this
                print("Error unifying timestamps: {}".format(row, e))

        # TODO: talk to Robert; remove if not needed
        if row.corpus == "Chintang":
            row.morpheme = None if row.morpheme is None else re.sub('\*\*\*', '???', row.morpheme)
            row.gloss_raw = None if row.gloss_raw is None else re.sub('\*\*\*', '???', row.gloss_raw)
            row.pos_raw = None if row.pos_raw is None else re.sub('\*\*\*', '???', row.pos_raw)

        if row.corpus == "Russian":
            row.morpheme = None if row.morpheme is None else re.sub('xxx?|www', '???', row.morpheme)

        if row.corpus == "Indonesian":
            row.morpheme = None if row.morpheme is None else re.sub('xxx?|www', '???', row.morpheme)
            row.gloss_raw = None if row.gloss_raw is None else re.sub('xxx?|www', '???', row.gloss_raw)
            # TODO: this should be above?
            row.utterance_raw = None if row.utterance_raw is None else re.sub('xxx?|www', '???', row.utterance_raw)
            row.translation = None if row.translation is None else re.sub('xxx?|www', '???', row.translation)


def process_speakers():
    table = session.query(backend.Speaker)
    for row in table:
        update_age(row)
        gender(row)
        role(row)
        macrorole(row)
    # Run the unique speaker algorithm -- requires full table
    unique_speakers(table)


def unique_speakers(table):
    """ Populate the the unique speakers table. Also populate uniquespeaker_id_fk in the speakers table.

    Uniqueness is determined by a combination of speaker: name, speaker label, birthdate. Yikes!
    """
    unique_speakers = [] # unique speaker dicts for uniquespeakers table
    identifiers = [] # keep track of unique (name, label, birthdate) speaker tuples

    for row in table:
        t = (row.name, row.birthdate, row.speaker_label)
        if t not in identifiers:
            identifiers.append(t)
            # create unique speaker row
            d = {}
            d['id'] = identifiers.index(t) + 1 # Python lists start at 0!
            d['corpus'] = row.corpus
            d['speaker_label'] = row.speaker_label
            d['name'] = row.name
            d['birthdate'] = row.birthdate
            d['gender'] = row.gender
            unique_speakers.append(backend.UniqueSpeaker(**d))

        # insert uniquespeaker_fk_id in speakers table
        row.uniquespeaker_id_fk = identifiers.index(t) + 1

    # Add all unique speakers entries to uniquespeakers table; skip if the table is already populated.
    if session.query(backend.UniqueSpeaker).count() == 0:
        session.add_all(unique_speakers)


def unify_label(row):
    """ Key-value substitutions for morphological glosses and parts-of-speech in the database. If no key is
        defined in the corpus ini file, then None (NULL) is written to the database.
    """
    # TODO: Insert some debugging here if the labels are missing?
    config = get_config(row.corpus)
    row.gloss = config['gloss'].get(row.gloss_raw, None)
    row.pos = config['pos'].get(row.pos_raw, None)


def get_session_date(session_id):
    rows = session.query(backend.Session).filter(backend.Session.id == session_id)
    return rows[0].date


def update_imdi_age(row):
    """ Process speaker ages in IMDI corpora.

    Finds all the recording sessions in the corpus in the config, then, for each speaker
    in the session:

    First attempts to calculate ages from the speaker's birth date and the session's
    recording date. For speakers where this fails, looks for speakers that already
    have a properly formatted age, transfers this age from the age_raw column to the
    age column and calculates age_in_days from it.

    Finally, it looks for speakers that only have an age in years and does the same.
    """

    # Check birthdate
    # ["Un%", "None"]
    # TODO: Cazim fix this part
    if not (row.birthdate.__contains__("Un") or row.birthdate.__contains__("None")):
        try:
            session_date = get_session_date(row.session_id_fk)
            recording_date = age.numerize_date(session_date)
            birth_date = age.numerize_date(row.birthdate)
            ages = age.format_imdi_age(birth_date, recording_date)
            row.age = ages[0]
            row.age_in_days = ages[1]
        except age.BirthdateError as e:
            print("Warning: couldn't calculate age of speaker {} from birth and recording dates".format(row.id), file=sys.stderr)
            print("Invalid birthdate: {}. Check data in {} file {}".format(e.bad_data, row.corpus, row.id), file=sys.stderr)
        except age.SessionDateError as e:
            print("Warning: couldn't calculate age of speaker {} from birth and recording dates".format(row.id), file=sys.stderr)
            print("Invalid session recording date: \"{}\"\nCheck data in {} file {}".format(e.bad_data, row.corpus, row.id), file=sys.stderr)

    # age_raw.like("%;%.%")
    if re.fullmatch(age_pattern, row.age_raw):
        row.age = row.age_raw
        row.age_in_days = age.calculate_xml_days(row.age_raw)

    # Check age again?
    if not row.age_raw.__contains__("None") or not row.age_raw.__contains__("Un") or row.age == None:
        if not cleaned_age.fullmatch(row.age_raw):
            try:
                ages = age.clean_incomplete_ages(row.age_raw)
                row.age = ages[0]
                row.age_in_days = ages[1]
            except ValueError as e:
                print("Error: Couldn't transform age of speaker {}".format(row.id), file=sys.stderr)
                print("Age data {} could not be converted to int\nCheck data in {} file {}".format(row.age_raw, row.corpus, row.id), file=sys.stderr)
                print("Warning: this speaker is likely to be completely without age data in the DB!")


# TODO: age is format dependent
def update_age(row):
    """ Age unification. Checks the config for the metadata format of the corpus,
        then calls the appropriate function.
    """
    config = get_config(row.corpus)
    if config["metadata"]["type"] == "imdi":
        update_imdi_age(row)
    else:
        update_xml_age(row)


def update_xml_age(row):
    """ Process speaker ages in Chat XML corpora.

    Finds all speakers from the corpus in the config and calls methods from age.py to
    fill in the age and age_in_days columns.
    """
    if row.age_raw is not None:
        new_age = age.format_xml_age(row.age_raw)
        # TODO: why the check here?
        if new_age:
            row.age = new_age
            aid = age.calculate_xml_days(new_age)
            row.age_in_days = aid


def macrorole(row):
    """ Define macrorole (= Adult, Child, Target_Child, Unknown)

    This function assigns an age category to each speaker. If there is
    no information on age available it uses "role_mappings.ini" to define
    which age category a speaker belongs to. The mapping is based on either
    the speaker's original role or speaker_label (depending on how the corpora
    handles role encoding).
    """
    # TODO: this method is completely dependent on ages -- no warnings are given if the age input is wrong!
    # Check if macrorole is not already filled by roles()
    if row.macrorole is None:
        # First check age: Adults are >= 12yrs, i.e. > 4380 days
        if row.age_in_days is not None:
            if row.age_in_days <= 4380:
                row.macrorole = "Child"
            else:
                row.macrorole = "Adult"
        # Second check corpus-specific lists of speaker labels
        else:
            try:
                row.macrorole = roles[row.corpus][row.speaker_label]
            except KeyError:
                row.macrorole = "Unknown"


def role(row):
    """ Unify speaker roles and draw inferences to related values.

    Each corpus has its own set of speaker roles. This function uses
    "role_mapping.ini" to assign a unified role to each speaker according
    to the mappings in role_mapping.ini. The mapping is either based on the original
    role or the speaker_label (depending on how the corpora handles role encoding).
    The role column in the speaker table contains the unified roles.
    """
    not_found = set()

    try:
        row.role = roles['role_mapping'][row.role_raw]
    # otherwise remember role
    except KeyError:
        row.role = row.role_raw
        not_found.add((row.role_raw,row.corpus))

    # inference to gender
    if (row.gender_raw is None or row.gender_raw in ['Unspecified', 'Unknown']):
        try:
            row.gender = roles['role2gender'][row.role_raw]
        except KeyError:
            pass

    # inference to age (-> macrorole)
    if (row.macrorole is None or row.macrorole in ['Unspecified', 'Unknown']):
        try:
            row.macrorole = roles['role2macrorole'][row.role_raw]
            # make sure None is not taken as a string
            if row.macrorole == 'None':
                row.macrorole = None
        except KeyError:
            pass

    if len(not_found) > 0:
        print("-- WARNING --")
        for item in not_found:
            print("'"+item[0]+"'","from",item[1])
        print("not found in role_mapping.ini\n--------")


def gender(row):
    """Function to unify speaker genders.
    """
    # if not row.gender_raw.lower().strip() in ['male', 'female']:
    #    row.gender = "Unspecified"

    if row.gender_raw is not None:
        if row.gender_raw.lower() == 'female':
            row.gender = 'Female'
        elif row.gender_raw.lower() == 'male':
            row.gender = 'Male'
        else:
            row.gender = "Unspecified"
    else:
        row.gender = "Unspecified"


def main():
    setup()
    postprocessor()
    commit()

if __name__ == "__main__":
    import time
    start_time = time.time()
    main()
    print("%s seconds --- Finished" % (time.time() - start_time))
    print()
    print('Next, run tests:')
    print('python3 -m "nose" -s -w tests test_counts.py')
    print('python3 -m "nose" -s -w tests test_regression.py')
    print()