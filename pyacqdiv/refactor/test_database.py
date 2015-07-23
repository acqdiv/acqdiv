from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation, sessionmaker

Base = declarative_base()

class Movie(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    year = Column(Integer)
    directed_by = Column(Integer, ForeignKey('directors.id'))

    director = relation("Director", backref='movies', lazy=False)

    def __init__(self, title=None, year=None):
        self.title = title
        self.year = year

    def __repr__(self):
        return "Movie(%r, %r, %r)" % (self.title, self.year, self.director)

class Director(Base):
    __tablename__ = 'directors'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return "Director(%r)" % (self.name)



if __name__=="__main__":
    engine = create_engine('sqlite:///_movies.sqlite3', echo=False)
    # engine = create_engine('dbms://user:pwd@host/dbname')
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    # TODO: in these objects we could do our testing and corrections
    # from bugzilla party
    m1 = Movie("Robocop", 1987)
    m1.director = Director("Paul Verhoeven")

    d2 = Director("George Lucas")
    d2.movies = [Movie("Star Wars", 1977), Movie("THX 1138", 1971)]

    try:
        session.add(m1)
        session.add(d2)
        session.commit()
    except:
        session.rollback()

    # query database
    alldata = session.query(Movie).all()
    for somedata in alldata:
        print somedata