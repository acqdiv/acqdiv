import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker


session = None


def setup():
    global cfg, session
    engine = sa.create_engine('sqlite:///test.sqlite3')
    meta = sa.MetaData(engine, reflect=True)
    Session = sessionmaker(bind=engine)
    session = Session()


def tests():
    pass

"""
The idea would be to have shared test functions between the full and test databases.

"""