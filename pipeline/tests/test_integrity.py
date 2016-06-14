import configparser
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from nose.tools import assert_equal, assert_in, assert_not_equal


session = None

def setup():
    global cfg, session
    engine = sa.create_engine('sqlite:///test.sqlite3')
    meta = sa.MetaData(engine, reflect=True)
    Session = sessionmaker(bind=engine)
    session = Session()


def test_database_integrity():
    # Note: SQL "NULL" returns as Python None

    # Check various value sets
    # TODO: should not be None once we implement BB's suggestion
    table = "morphemes"
    column = "gloss"
    values = [None, "0", "1", "2", "3", "4", "4SYL", "A", "ABIL", "ABL", "ABS", "ACC", "ACROSS", "ACT", "ADESS", "ADJ", "ADJZ", "ADN", "ADV", "ADVZ", "AFF", "AGT", "AGR", "ALL", "ALT", "AMBUL", "ANIM", "ANTIP", "AOR", "APPL", "ART", "ASP", "ASS", "ASSOC", "ATTN", "AUTOBEN", "AUX", "AV", "BABBLE", "BEN", "CAUS", "CHOS", "CLF", "CLIT", "CM", "COM", "COMP", "COMPAR", "COMPL", "CONC", "COND", "CONJ", "CONJ", "CON", "CONT", "CONTEMP", "CONTING", "CONTR", "COP", "CVB", "DAT", "DECL", "DEF", "DEICT", "DEM", "DEP", "DEPR", "DESID", "DESTR", "DET", "DETR", "DIM", "DIR", "DIR", "DIST", "DISTR", "DOWN", "DU", "DUB", "DUR", "DYN", "ECHO", "EMPH", "EQU", "ERG", "EVID", "EXCL", "EXCLA", "EXIST", "EXT", "F", "FILLER", "FOC", "FUT", "GEN", "HAB", "HES", "HHON", "HON", "HORT", "IDEOPH", "IMIT", "IMP", "IMPERS", "INAL", "INAN", "INCEP", "INCH", "INCL", "INCOMPL", "IND", "INDF", "INDIR", "INF", "INS", "INSIST", "INTJ", "INTR", "INTRG", "INV", "IPFV", "IRR", "LNK", "LOC", "M", "MED", "MHON", "MIR", "MOD", "MOOD", "MV", "N", "N", "N", "NAG", "NAME", "NC", "NEG", "NICKNAMER", "NMLZ", "NOM", "NPST", "NSG", "NTVZ", "NUM", "OBJ", "OBJVZ", "OBL", "OBLIG", "OBV", "ONOM", "OPT", "ORD", "P", "PARTIT", "PASS", "PEJ", "PERL", "PERMIS", "PERSIST", "PFV", "PL", "POL", "POSS", "POT", "PRAG", "PRED", "PREDADJ", "PREP", "PREP", "PRF", "PRO", "PROB", "PROG", "PROH", "PROP", "PROX", "PRS", "PST", "PTCL", "PTCP", "PURP", "PV", "PVB", "Q", "QUANT", "QUOT", "RECENT", "RECNF", "RECP", "REF", "REFL", "REL", "REM", "REP", "RES", "REVERS", "S", "SBJ", "SBJV", "SEQ", "SG", "SIM", "SOC", "SPEC", "STAT", "STEM", "SUPERL", "SURP", "TEASER", "TEL", "TEMP", "TENSE", "TERM", "TOP", "TR", "UP", "V", "V2", "V.AUX", "V.CAUS", "V.IMP", "V.ITR", "V.PASS", "V.POS", "V.TR", "VBZ", "VOICE", "VN", "VOC", "VOL", "WH", "???"]
    yield check_values, table, column, values

    table = "utterances"
    column = "sentence_type"
    values = [None, "default", "question", "exclamation", "imperative", "action", "trail off", "interruption", "trail off question", "self interruption", "quotation precedes", "interruption question"]
    yield check_values, table, column, values

    table = "morphemes"
    column = "pos"
    values = [None, "ADJ", "ADV", "ART", "AUX", "CLF", "CONJ", "IDEOPH", "INTJ", "N", "NUM", "pfx", "POST", "PREP", "PRODEM", "PTCL", "QUANT", "sfx", "stem", "V", "???"]
    yield check_values, table, column, values

    table = "speakers"
    column = "gender"
    values = ["Female", "Male", "Unknown"]
    yield check_values, table, column, values

    # TODO: https://github.com/uzling/acqdiv/issues/351
    table = "speakers"
    column = "role"
    values = ["Adult", "Aunt", "Babysitter", "Brother", "Caller", "Caretaker", "Cousin", "Daughter", "Family_Friend", "Father", "Friend", "Grandfather", "Grandmother", "Great-Grandmother", "Host", "Housekeeper", "Mother", "Neighbour", "Niece", "Playmate", "Research_Team", "Sibling", "Sister", "Sister-in-law", "Son", "Speaker", "Student", "Subject", "Target_Child", "Teacher", "Toy", "Twin_Brother", "Uncle", "Unknown", "Visitor"]
    yield check_values, table, column, values

    table = "speakers"
    column = "macrorole"
    values = ["Adult", "Child", "Target_Child", "Unknown"]
    yield check_values, table, column, values

    # Check columns for at least one NULL
    for check in (("sessions","date"),("utterances","speaker_label"),("utterances","utterance_raw"),("utterances","utterance"),("words","word"),("speakers","speaker_label"),("speakers","macrorole"),("uniquespeakers","speaker_label"),("uniquespeakers","corpus")):
        table = check[0]
        column = check[1]
        yield check_any_null, table, column    
    
    # XXX, XX1, etc., and AUX create NULL
    # query = "select count(*) from speakers where name is null"
    # yield check_any_null, query

    # Check columns for all NULL
    for check in (("utterances","translation"),("utterances","morpheme"),("utterances","gloss_raw"),("utterances","pos_raw"),("words","pos"),("morphemes","morpheme"),("morphemes","gloss_raw"),("morphemes","gloss"),("morphemes","pos_raw"),("morphemes","pos"),("speakers","name"),("speakers","age_raw"),("speakers","age"),("speakers","age_in_days"),("speakers","gender_raw"),("speakers","gender"),("speakers","role_raw"),("speakers","role")):
        table = check[0]
        column = check[1]
        yield check_all_null, table, column

def check_values(table, column, values):
    query = "select " + column + " from " + table + " group by " + column
    res = session.execute(query)
    rows = res.fetchall()
    for row in rows:
        label = row[0]
        assert_in(label, values, msg='%s in database, but not in valid labels' % (label))

def check_any_null(table, column):
    for corpus in ('Chintang', 'Cree', 'Indonesian', 'Inuktitut', 'Japanese_Miyata', 'Japanese_MiiPro', 'Russian', 'Sesotho', 'Turkish', 'Yucatec'):
        query = 'select count(*) from ' + table + ' where corpus="' + corpus + '" and ' + column + ' is null'
        res = session.execute(query)
        actual = res.fetchone()[0]
        assert_equal(actual, 0, msg=corpus+'.'+table+'.'+column+' contains NULL')

def check_all_null(table, column):
    for corpus in ('Chintang', 'Cree', 'Indonesian', 'Inuktitut', 'Japanese_Miyata', 'Japanese_MiiPro', 'Russian', 'Sesotho', 'Turkish', 'Yucatec'):
        query = 'select count(*) from ' + table + ' where corpus="' + corpus + '" and ' + column + ' is not null'
        res = session.execute(query)
        actual = res.fetchone()[0]
        assert_not_equal(actual, 0, msg=corpus+'.'+table+'.'+column+' contains only NULL')

# def check_words_actual_target():
#     pass
#
#     # count NULL in words_target, words_actual
#     # test is okay if
#     #   either one of the two counts is 0 (but not both)
#     #   or there are >0 rows where word_target != word_actual
#
# def check_characters():
#     pass
#
#     # word shouldn't be ^\s*$
#     # word should not contain [\'()*\"^_[]]
#     # word should not start with [-.̃]
#     # word should be "???" or not contain any "?" at all
#
#     # speaker_label should be [a-zA-Z\d]{2,}
#
#     # speaker.name can't contain numerals
#
# def time_checks():
#     pass
#
#     # date, age - is this needed at all? already tested in postprocessing?
#     # sessions.date is ^((19|20)\d\d(-(0[1-9]|1[012])-([012][1-9]|3[01]))?)$
#     # speakers.age is ^(\d\d?(;([0-9]|1[01]).([12]?[0-9]|30))?)$ or NULL
#     # speakers., uniquespeakers.birthdate is like sessions.date or "Unknown"
#
# # more complicated stuff
# # name can be anything or "Unknown" but not "Unspecified" or "None" (the problem with these values is that they can create additional unique pseudo-speakers)
# # the majority of rows should not have NULL in macrorole. A threshold of 15% should be realistic.
# # extract list of all speakers where out of {speaker_label, name, birthdate} two are identical. Sort by speaker label and check manually for mistakes (two speakers as one, one speaker as two)


"""
# TODO: add more tests... on the corpus by corpus level
def test_percent_nulls():
    corpora = ['Chintang', 'Cree', 'Indonesian', 'Inuktitut', 'Japanese_Miyata',
               'Japanese_MiiPro', 'Russian', 'Sesotho', 'Turkish', 'Yucatec']
    res = session.execute("select count(*) from ")
    actual = res.fetchone()[0]
    assert_equal(actual, 0, msg='Column contains NULL')

def test_types():
    # e.g. that no numbers are in speaker_label fields, etc.
    pass
"""