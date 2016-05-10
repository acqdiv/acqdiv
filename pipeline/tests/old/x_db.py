import unittest
import configparser
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker


class TestCounts(unittest.TestCase):
    def setUp(self):
        engine = sa.create_engine('sqlite:///test.sqlite3')
        meta = sa.MetaData(engine, reflect=True)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        # reflecting tables:
        # utterances = sa.Table('utterances', meta, autoload=True, autoload_with=engine)

        # config setup
        self.cfg = configparser.ConfigParser()
        self.cfg.read("counts.ini")

    def test_evens():
        for i in range(0, 5):
            yield check_even, i, i*3

    def check_even(n, nn):
        assert n % 2 == 0 or nn % 2 == 0

    def test_counts(self):
        # self.assertTrue(1==1)
        # print(self.session.query(self.utterances).filter(self.utterances.c.corpus=="Cree"))
        # print(self.session.query(utterances).filter(utterances.corpus=="Cree"))

        # for c in self.utterances.c: print(c)

        for k in self.cfg:
            print(k)
            # skip default section in default python config
            if k == "DEFAULT":
                continue
            # returns <class 'sqlalchemy.engine.result.RowProxy'>
            utterances = self.session.execute('select count(*) from utterances where corpus = "'+k+'"')
            # get at int and compare with hand-vetted counts
            actual = utterances.fetchone()[0]
            target = int(self.cfg[k]['Utterances'])

            with self.subTest(actual=target):
                self.assertEqual(actual, target)

#            self._test_count(actual, target)
            # self.assertTrue(utterances.fetchone()[0] == int(self.cfg[k]['Utterances']))

#    def _get_count(self, actual, target):
#            self.assertEqual(actual, target)


            #print(utterances.fetchone()[0], int(self.cfg[k]['Utterances']))
            # print(type(n.fetchone()[0]))

#            print(x.fetchone()[0])
#            utterances = self.c.execute("select count(*) from utterances where corpus = '"+k+"'")
#            count = utterances.fetchall()[0]
#            print(count[0])
        # print(utterances.fetchall())
        # print(utterances.fetchone())
        # self.assertTrue(utterances==10)
#        c.execute(query_string)
#    return c.fetchall()

"""
class TestDB(unittest.TestCase):
    def setUp(self):
       url = os.getenv("../acqdiv.sqlite3")
       if not url:
           self.skipTest("No database URL set")
       self.engine = sqlalchemy.create_engine(url)

    def full_match(self):
        # test whether the whole database matches? this would break though on sessions database creation date, if added
        pass

class TestCounts(unittest.TestCase):
    pass


class TestQueries(unittest.TestCase):
    pass
"""

# https://www.jeffknupp.com/blog/2013/12/09/improve-your-python-understanding-unit-testing/
# https://wiki.python.org/moin/PythonTestingToolsTaxonomy
# http://intermediate-and-advanced-software-carpentry.readthedocs.org/en/latest/nose-intro.html
# http://alextechrants.blogspot.ch/2013/08/unit-testing-sqlalchemy-apps.html
# https://julien.danjou.info/blog/2014/db-integration-testing-strategies-python
# http://ivory.idyll.org/articles/nose-intro.html
# http://pythontesting.net/framework/nose/nose-introduction/
# https://cgoldberg.github.io/python-unittest-tutorial/
# http://docs.python-guide.org/en/latest/writing/tests/


# df = pd.read_sql(query.statement, query.session.bind)