import configparser
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from nose.tools import assert_equal, assert_in


session = None

def setup():
    global cfg, session
    engine = sa.create_engine('sqlite:///../../database/beta.sqlite3')
    meta = sa.MetaData(engine, reflect=True)
    Session = sessionmaker(bind=engine)
    session = Session()


def test_counts():
    cfg = configparser.ConfigParser()
    cfg.read("session_counts.ini")
    for section in cfg:
        if section == "default":
            continue
        for option in cfg[section]:
            yield check_counts, section, option, int(cfg[section][option])


def check_counts(corpus, attr, target):
    res = session.execute("select count(*) from %s where corpus = '%s'" % (attr, corpus))
    actual = res.fetchone()[0]
    assert_equal(actual, target, msg='%s %s: expected %s, got %s' % (corpus, attr, target, actual))


def test_database_integrity():
    # Note: SQL "NULL" returns as Python None

    # Check various value sets
    query = "select gloss from morphemes group by gloss"
    gloss = ["0", "1", "2", "3", "4", "4SYL", "A", "ABIL", "ABL", "ABS", "ACC", "ACROSS", "ACT", "ADESS", "ADJ", "ADJZ", "ADN", "ADV", "ADVZ", "AFF", "AGT", "AGR", "ALL", "ALT", "AMBUL", "ANIM", "ANTIP", "AOR", "APPL", "ART", "ASP", "ASS", "ASSOC", "ATTN", "AUTOBEN", "AUX", "AV", "BABBLE", "BEN", "CAUS", "CHOS", "CLF", "CLIT", "CM", "COM", "COMP", "COMPAR", "COMPL", "CONC", "COND", "CONJ", "CONJ", "CON", "CONT", "CONTEMP", "CONTING", "CONTR", "COP", "CVB", "DAT", "DECL", "DEF", "DEICT", "DEM", "DEP", "DEPR", "DESID", "DESTR", "DET", "DETR", "DIM", "DIR", "DIR", "DIST", "DISTR", "DOWN", "DU", "DUB", "DUR", "DYN", "ECHO", "EMPH", "EQU", "ERG", "EVID", "EXCL", "EXCLA", "EXIST", "EXT", "F", "FILLER", "FOC", "FUT", "GEN", "HAB", "HES", "HHON", "HON", "HORT", "IDEOPH", "IMIT", "IMP", "IMPERS", "INAL", "INAN", "INCEP", "INCH", "INCL", "INCOMPL", "IND", "INDF", "INDIR", "INF", "INS", "INSIST", "INTJ", "INTR", "INTRG", "INV", "IPFV", "IRR", "LNK", "LOC", "M", "MED", "MHON", "MIR", "MOD", "MOOD", "MV", "N", "N", "N", "NAG", "NAME", "NC", "NEG", "NICKNAMER", "NMLZ", "NOM", "NPST", "NSG", "NTVZ", "NUM", "OBJ", "OBJVZ", "OBL", "OBLIG", "OBV", "ONOM", "OPT", "ORD", "P", "PARTIT", "PASS", "PEJ", "PERL", "PERMIS", "PERSIST", "PFV", "PL", "POL", "POSS", "POT", "PRAG", "PRED", "PREDADJ", "PREP", "PREP", "PRF", "PRO", "PROB", "PROG", "PROH", "PROP", "PROX", "PRS", "PST", "PTCL", "PTCP", "PURP", "PV", "PVB", "Q", "QUANT", "QUOT", "RECENT", "RECNF", "RECP", "REF", "REFL", "REL", "REM", "REP", "RES", "REVERS", "S", "SBJ", "SBJV", "SEQ", "SG", "SIM", "SOC", "SPEC", "STAT", "STEM", "SUPERL", "SURP", "TEASER", "TEL", "TEMP", "TENSE", "TERM", "TOP", "TR", "UP", "V", "V2", "V.AUX", "V.CAUS", "V.IMP", "V.ITR", "V.PASS", "V.POS", "V.TR", "VBZ", "VOICE", "VN", "VOC", "VOL", "WH", "???"]
    yield check_values, query, gloss

    query = "select sentence_type from utterances group by sentence_type"
    sentence_type = [None, "default", "question", "exclamation", "imperative", "action", "trail off", "interruption", "trail off question", "self interruption", "quotation precedes", "interruption question"]
    yield check_values, query, sentence_type

    query = "select pos from morphemes group by pos"
    pos = ["ADJ", "ADV", "ART", "AUX", "CLF", "CONJ", "IDEOPH", "INTJ", "N", "NUM", "pfx", "POST", "PREP", "PRODEM", "PTCL", "QUANT", "sfx", "stem", "V", "???"]
    yield check_values, query, pos

    query = "select gender from speakers group by gender"
    gender = ["Female", "Male", "Unknown"]
    yield check_values, query, gender

    query = "select role from speakers group by role"
    role = ["Adult", "Aunt", "Babysitter", "Brother", "Caller", "Caretaker", "Cousin", "Daughter", "Family_Friend", "Father", "Friend", "Grandfather", "Grandmother", "Great-Grandmother", "Host", "Housekeeper", "Mother", "Neighbour", "Niece", "Playmate", "Research_Team", "Sibling", "Sister", "Sister-in-law", "Son", "Speaker", "Student", "Subject", "Target_Child", "Teacher", "Toy", "Twin_Brother", "Uncle", "Unknown", "Visitor"]
    yield check_values, query, role

    query = "select macrorole from speakers group by macrorole"
    macrorole = ["Adult", "Child", "Target_Child", "Unknown"]
    yield check_values, query, macrorole

    # Check columns for NULL
    query = "select count(*) from sessions where date is null"
    yield check_null, query

    query = "select count(*) from sessions where media is null"
    yield check_null, query

    query = "select count(*) from utterances where speaker_label is null"
    yield check_null, query

    query = "select count(*) from utterances where utterance_raw is null"
    yield check_null, query

    query = "select count(*) from utterances where utterance is null"
    yield check_null, query

    query = "select count(*) from utterances where sentence_type is null"
    yield check_null, query

    query = "select count(*) from words where word is null"
    yield check_null, query

    query = "select count(*) from speakers where speaker_label is null"
    yield check_null, query

    query = "select count(*) from speakers where name is null"
    yield check_null, query

    query = "select count(*) from speakers where macrorole is null"
    yield check_null, query

    query = "select count(*) from uniquespeakers where speaker_label is null"
    yield check_null, query

    query = "select count(*) from uniquespeakers where name is null"
    yield check_null, query

    query = "select count(*) from uniquespeakers where corpus is null"
    yield check_null, query


def check_values(query, values):
    res = session.execute(query)
    rows = res.fetchall()
    for row in rows:
        label = row[0]
        assert_in(label, values, msg='%s in database, but not in valid labels' % (label))


def check_null(query):
    res = session.execute(query)
    actual = res.fetchone()[0]
    assert_equal(actual, 0, msg='Column contains NULL')
