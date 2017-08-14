""" Post-processing processes on the corpora in the ACQDIV-DB.
"""

import logging
import pipeline_logging
import re
import sys

import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker

import database_backend as backend
from configparser import ConfigParser
from parsers import CorpusConfigParser
from processors import age

session = None
cfg = None
cleaned_age = re.compile('\d{1,2};\d{1,2}\.\d')
age_pattern = re.compile(".*;.*\..*")


pos_index = {}

def setup(args):
    """
    Global setup
    """
    global cfg, session

    # If testing mode
    if args.t:
        engine = sa.create_engine('sqlite:///database/test.sqlite3')
    else:
        engine = sa.create_engine('sqlite:///database/acqdiv.sqlite3')

    meta = sa.MetaData(engine, reflect=True)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Load the role mapping.ini for unifying roles
    global roles
    roles = ConfigParser(delimiters=('='))
    roles.optionxform = str
    roles.read("ini/role_mapping.ini")

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
    elif corpus_name == "Turkish":
        return turkish
    elif corpus_name == "Yucatec":
        return yucatec
    else:
        raise Exception


def postprocessor():
    """ Postprocessing postprocesses.
    """
    # Update database tables
    print("Processing speakers...")
    process_speakers()
    print("Processing utterances...")
    process_utterances()
    print("Processing morphemes...")
    process_morphemes()
    print("Processing words...")
    process_words()

    # Additional data
    # TODO: duplicate primary keys to additional roles


def infer_pos(row):
    """ Chintang and Indonesian part-of-speech inference. Also removes hyphens from raw input data.
    """

    # Linguistic-specific stuff
    if row.corpus == "Indonesian":
        if row.gloss_raw is not None:
            if row.gloss_raw.startswith('-'):
                row.pos_raw = 'sfx'
            elif row.gloss_raw.endswith('-'):
                row.pos_raw = 'pfx'
            elif row.gloss_raw == '???':
                row.pos_raw = '???'
            else:
                if row.pos_raw not in {'sfx', 'pfx', '???'}:
                    row.pos_raw = 'stem'

    if row.corpus == "Chintang":
        if not row.pos_raw is None:
            if row.pos_raw.startswith('-'):
                row.pos_raw = 'sfx'
            elif row.pos_raw.endswith('-'):
                row.pos_raw = 'pfx'

    # Clean everything
    if not row.morpheme is None:
        row.morpheme = row.morpheme.replace('-', '')
    if not row.gloss_raw is None:
        row.gloss_raw = row.gloss_raw.replace('-', '')
    if not row.pos_raw is None:
        row.pos_raw = row.pos_raw.replace('-', '')


def process_morphemes():
    """
    Process the morphemes table

    # TODO: break this down by corpus and profile if it's faster
    """
    table = session.query(backend.Morpheme)
    for row in table:
        # Clean up affix markers "-"; assign sfx, pfx, stem.
        if row.corpus == "Chintang" or row.corpus == "Indonesian":
            infer_pos(row)
        # Key-value substitutions for morphological glosses and parts-of-speech
        infer_label(row)
        unify_label(row)
        # Infer the word's part-of-speech from the morphemes table as index for word pos assignment
        get_pos_index(row)


def get_pos_index(row):
    if not row.pos in ["sfx", "pfx"]:
        # row.id will be int type in other tables when look up occurs; type it int here for convenience
        try:
            pos_index[int(row.word_id_fk)] = row.pos
        except TypeError:
            pass

def process_words():
    table = session.query(backend.Word)
    for row in table:
        if row.id in pos_index:
            row.pos = pos_index[row.id]


def process_utterances():
    """
    Process utterances table
    """
    table = session.query(backend.Utterance)
    for row in table:
        # Unify the time stamps
        if row.start_raw: #.isnot(None):
            try:
                row.start = age.unify_timestamps(row.start_raw)
                row.end = age.unify_timestamps(row.end_raw)
            except Exception as e:
                # TODO: log this
                logger.warning('Error unifying timestamps: {}'.format(
                    row, e), exc_info=sys.exc_info())

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
            change_speaker_labels(row)

        # set speaker-utterance links
        uniquespeakers_utterances(row)
        if row.corpus != "Chintang":
            row.childdirected = get_directedness(row)


def get_directedness(utt):
    if utt.addressee is not None:
        addressee = session.query(backend.Speaker).filter(
            backend.Speaker.speaker_label == utt.addressee).filter(
                backend.Speaker.session_id_fk == utt.session_id_fk).first()
        if addressee is not None:
            if (addressee.macrorole == 'Target_Child'
                and utt.speaker_label != utt.addressee):
                return True
            else:
                return False
        else:
            return False
    else:
        return False


def change_speaker_labels(row):
    if row.speaker_label is not None:
        if not 'EXP' in row.speaker_label:
            row.speaker_label = row.speaker_label[0:3]
        else:
            row.speaker_label = row.speaker_label[3:]


def process_speakers():
    """
    Process speakers table
    """
    table = session.query(backend.Speaker)
    for row in table:
        indonesian_experimenters(row)
        update_age(row)
        gender(row)
        role(row)
        macrorole(row)
    # Run the unique speaker algorithm -- requires full table
    unique_speakers(table)
    # set session target child
    target_children(table)


def indonesian_experimenters(row):
    if row.corpus == 'Indonesian':
        cfg = get_config(row.corpus)
        if row.speaker_label == 'EXP':
            row.speaker_label = cfg['exp_labels'][row.name]


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


def uniquespeakers_utterances(row):
    """
    Link Unique speakers / utterances
    """
    speaker = session.query(backend.Speaker).\
        filter(backend.Speaker.speaker_label == row.speaker_label).\
        filter(backend.Speaker.session_id_fk == row.session_id_fk).\
        filter(backend.Speaker.corpus == row.corpus).first()
    if speaker is not None:
        row.uniquespeaker_id_fk = speaker.uniquespeaker_id_fk
        row.speaker_id_fk = speaker.id


def target_children(table):
    """
    Set target children for sessions.

    Also adapt roles and macroroles if there are multiple target children
    per session.
    """
    # store target children per session first
    targets_per_session = {}
    for row in table.filter(backend.Speaker.role == "Target_Child"):
        if row.session_id_fk in targets_per_session:
            targets_per_session[row.session_id_fk].add(row.uniquespeaker_id_fk)
        else:
            targets_per_session[row.session_id_fk] = {row.uniquespeaker_id_fk}

    # go through all session ids
    for session_id in targets_per_session:

        # get the target children for this session
        targets = targets_per_session[session_id]

        # get session row
        rec = session.query(backend.Session).\
            filter(backend.Session.id == session_id).first()

        # if there is one target child only
        if len(targets) == 1:
            # just set target child for the session
            rec.target_child_fk = targets.pop()
        # if there are several target children
        else:
            # infer target child from source id
            if rec.corpus == "Chintang":
                # get target child label
                label = rec.source_id[2:7]
                # get right target child id
                tc_id = session.query(backend.UniqueSpeaker).\
                    filter(backend.UniqueSpeaker.corpus == rec.corpus).\
                    filter(backend.UniqueSpeaker.speaker_label == label).\
                    first().id
            elif rec.corpus == "Russian":
                # session code's first letter matches that of speaker label
                letter = rec.source_id[0]
                # get right target child id
                tc_id = session.query(backend.Speaker).\
                    filter(backend.Speaker.corpus == rec.corpus).\
                    filter(backend.Speaker.role == "Target_Child").\
                    filter(backend.Speaker.speaker_label.like(
                            "{}%".format(letter))).\
                    first().uniquespeaker_id_fk
            elif rec.corpus == "Yucatec":
                label = rec.source_id[:3]
                tc_id = session.query(backend.UniqueSpeaker).\
                    filter(backend.UniqueSpeaker.corpus == rec.corpus).\
                    filter(backend.UniqueSpeaker.speaker_label == label).\
                    first().id
            else:
                logger.warning(
                    "Multiple target children for session {} in {}".format(
                        session_id, rec.corpus))
                continue

            # set this target child for the session
            rec.target_child_fk = tc_id

            # adapt role and macrorole of children that are not target anymore
            non_targets = table.\
                filter(backend.Speaker.role == "Target_Child").\
                filter(backend.Speaker.session_id_fk == session_id).\
                filter(backend.Speaker.uniquespeaker_id_fk != tc_id)
            for row in non_targets:
                row.role = "Child"
                row.macrorole = "Child"


def unify_label(row):
    """ Key-value substitutions for morphological glosses and parts-of-speech in the database. If no key is
        defined in the corpus ini file, then None (NULL) is written to the database.
    """
    # TODO: Insert some debugging here if the labels are missing?
    config = get_config(row.corpus)
    row.gloss = config['gloss'].get(row.gloss_raw, None)
    row.pos = config['pos'].get(row.pos_raw, None)


def infer_label(row):
    config = get_config(row.corpus)
    if config['morphemes']['substitutions'] == 'yes':
        source_tier = config['morphemes']['source_tier']
        target_tier = config['morphemes']['target_tier']
        exec("row.{0} = config['substitutions'].get(row.{1}, row.{0})".format(
            target_tier, source_tier)
        )


def get_session_date(session_id):
    """
    Return the session data
    """
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

    if row.birthdate is None:
        return

    if not (row.birthdate.__contains__("Un") or row.birthdate.__contains__("None")):
        try:
            session_date = get_session_date(row.session_id_fk)
            recording_date = age.numerize_date(session_date)
            birth_date = age.numerize_date(row.birthdate)
            ages = age.format_imdi_age(birth_date, recording_date)
            row.age = ages[0]
            row.age_in_days = ages[1]
        except age.BirthdateError as e:
            logger.warning('Couldn\'t calculate age of speaker {} '
                           'from birth and recording dates: '
                           'Invalid birthdate.'.format(
                               row.id), exc_info=sys.exc_info())
        except age.SessionDateError as e:
            logger.warning('Couldn\'t calculate age of speaker {} '
                           'from birth and recording dates: '
                           'Invalid recording date.'.format(
                               row.id), exc_info=sys.exc_info())

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
                logger.warning('Couldn\'t transform age of '
                               'speaker {}'.format(row.id),
                               exc_info=sys.exc_info())


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
    # overwrite role mapping (except target child) if speaker is under 12
    # (e.g. if child is an aunt which is mapped to 'Adult' per default)
    if row.age_in_days is not None and row.macrorole != "Target_Child":
        # Adults are >= 12yrs, i.e. > 4380 days
        if row.age_in_days <= 4380:
            row.macrorole = "Child"
        else:
            row.macrorole = "Adult"
    # Second check corpus-specific lists of speaker labels
    elif row.macrorole is None:
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
        for item in not_found:
            logger.warning('\'{}\' from {} not found in '
                           'role_mapping.ini'.format(item[0], item[1]),
                           exc_info=sys.exc_info())


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

def main(args):
    setup(args)
    postprocessor()
    commit()

if __name__ == "__main__":
    import time
    import argparse

    start_time = time.time()

    p = argparse.ArgumentParser()
    p.add_argument('-t', action='store_true')
    p.add_argument('-s', action='store_true')
    args = p.parse_args()

    global logger
    logger = logging.getLogger('pipeline.postprocessor')
    handler = logging.FileHandler('errors.log', mode='a')
    handler.setLevel(logging.INFO)
    if args.s:
        formatter = logging.Formatter('%(asctime)s - %(name)s - '
                                        '%(levelname)s - %(message)s')
    else:
        formatter = pipeline_logging.SuppressingFormatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    main(args)

    print("%s seconds --- Finished" % (time.time() - start_time))
    print()
    print('Next, run tests:')
    print('python3 -m "nose" -s -w tests test_regression.py')
    print('python3 -m "nose" -s -w tests test_integrity.py:ValidationTest_DevDB')
