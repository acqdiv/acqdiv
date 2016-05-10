from sqlalchemy import *
from sqlalchemy.orm import create_session
from sqlalchemy.ext.declarative import declarative_base

# Create and engine and get the metadata
Base = declarative_base()
engine = create_engine('sqlite:///../acqdiv.sqlite3')
metadata = MetaData(bind=engine)


# Reflect each database table we need to use, using metadata
class Utterances(Base):
    __table__ = Table('Utterances', metadata, autoload=True)

# class Users(Base):
#    __table__ = Table('Users', metadata, autoload=True)

# Create a session to use the tables
session = create_session(bind=engine)

testlist = session.query(Utterances).all()

# for test in testlist:
#    print(test)


import sqlite3

#
conn = sqlite3.connect('../acqdiv.sqlite3')
c = conn.cursor()

# counts
morphemes = 648
sessions = 10
speakers = 49
utterances = 164
uniquespeakers = 49
warnings = 1
words = 496


# basic stats
# self.assertEqual(session.query(db.Utterance).count(),  2246)
cc = c.execute('select count(*) from utterances')
for i in cc:
    print("Utterances:", i, i[0]==164, "Total: 164")
    print()

cc = c.execute('select count(*) from sessions')
for i in cc:
    print("Utterances:", i, i[0]==164, "Total: 164")
    print()

# dump this into a function; return data frame
print("Chintang:")
cc = c.execute('select count(*) from utterances where corpus = "Chintang"')
for i in cc:
    print(i)
cc = c.execute('select count(*) from words where corpus = "Chintang"')
for i in cc:
    print(i)
cc = c.execute('select count(*) from morphemes where corpus = "Chintang"')
for i in cc:
    print(i)

print("Russian:")

cc = c.execute('select count(*) from utterances where corpus = "Russian"')
for i in cc:
    print(i)
cc = c.execute('select count(*) from words where corpus = "Russian"')
for i in cc:
    print(i)
cc = c.execute('select count(*) from morphemes where corpus = "Russian"')
for i in cc:
    print(i)

print("Indonesian:")

cc = c.execute('select count(*) from utterances where corpus = "Indonesian"')
for i in cc:
    print(i)
cc = c.execute('select count(*) from words where corpus = "Indonesian"')
for i in cc:
    print(i)
cc = c.execute('select count(*) from morphemes where corpus = "Indonesian"')
for i in cc:
    print(i)
# assert equal to the stuff below...

""" Counts
# Chintang
utterances	17
words	42
morphemes	84

glosses	83
pos	85

# Indonesian
utterances	19
words	43
morphemes	56

glosses	58
pos	56

# Russian
utterances	20
words	40
morphemes	40

glosses	38
pos	38
"""


def test_corpus_counts(self):
    # self.assertEqual(session.query(db.Utterance).count(),  2246)
    pass


def test_toolbox_corpora_counts(self):
    # self.assertEqual(session.query(db.Utterance).count(),  2246)
    # where corpus="Chintang"
    # etc.
    pass


def test_toolbox_utterances(self):
    """
    Test if utterances for Toolbox test files are loaded correctly
    """
#    session = make_session()
    self.assertEqual(session.query(db.Utterance).count(),  2246)
    s_chntng = select([db.Utterance], and_(db.Utterance.utterance_id=="CLDLCh1R01S01.002"))
    s_ru = select([db.Utterance], and_(db.Utterance.utterance_id=="A00210817_3"))
    s_indon = select([db.Utterance], and_(db.Utterance.utterance_id=="447883094927120405"))
    result_chntng = session.execute(s_chntng)
    result_ru = session.execute(s_ru)
    result_indon = session.execute(s_indon)

    self.assertEqual(str(result_chntng.fetchall()), "[(2, 'Chintang', 'Chintang', 'Chintang', 'CLDLCh1R01S01.002', 'MKR', None, 'theke hapamettukumcum hou', 'theke hapamettukumcum hou', 'None', 'question', None, None, '00:00:01.908', '00:00:03.348', 'theke hapamettukumcum hou', 'theke *** hou', 'why *** AFF', 'adv n gm', None, None)]")
    self.assertEqual(str(result_ru.fetchall()), "[(375, 'Russian', 'Russian', 'Russian', 'A00210817_3', 'LEN', None, 'Alja , ne trogaj kisu .', 'Alja  ne trogaj kisu ', None, 'default', None, None, None, None, None, 'alja , ne trogatq kisa .', None, 'NAME:M:SG:NOM:AN PUNCT PCL V-IMP:2:SG:IRREFL:IPFV NOUN:F:SG:ACC:INAN PUNCT ', None, None)]")
    self.assertEqual(str(result_indon.fetchall()), "[(1003, 'Indonesian', 'Indonesian', 'Indonesian', '447883094927120405', 'MOTHIZ', None, 'e, Ai mana Ai, Ai, eh?', 'e Ai mana Ai Ai eh', 'hey, where is Ai, Ai, hey?', 'question', None, None, '0:00:21', None, None, 'e Ai mana Ai Ai eh', 'EXCL Ai which Ai Ai huh', None, None, None)]")
    session.close()