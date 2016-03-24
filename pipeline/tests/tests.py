import configparser

from nose.tools import assert_equal
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker

session = None


def setup():
    global cfg, session
    engine = sa.create_engine('sqlite:///test.sqlite3')
    meta = sa.MetaData(engine, reflect=True)
    Session = sessionmaker(bind=engine)
    session = Session()

def test_counts():
    cfg = configparser.ConfigParser()
    cfg.read("counts.ini")
    for section in cfg:
        # skip default section in default python config
        if section == "DEFAULT":
            continue
        for option in cfg[section]:
            if option == 'utterances':
                yield check, section, option, int(cfg[section][option])
            if option == 'words':
                yield check, section, option, int(cfg[section][option])
            if option == 'morphemes':
                yield check, section, option, int(cfg[section][option])
            if option == 'glosses':
                yield check, section, option, int(cfg[section][option])
            if option == 'pos':
                yield check, section, option, int(cfg[section][option])

def check(corpus, attr, target):
    res = session.execute("select count(*) from %s where corpus = '%s'" % (attr, corpus))
    actual = res.fetchone()[0]
    assert_equal(actual, target, msg='%s %s: expected %s, got %s' % (corpus, attr, target, actual))

