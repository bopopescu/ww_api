"""Example for reflecting database tables to ORM objects

This script creates classes for each table reflected
from the database.

Note: The class names are imported to the global namespace using
the same name as the tables. This is useful for quick utility scripts.
A better solution for production code would be to return a dict
of reflected ORM objects.
"""

from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


def reflect_all_tables_to_declarative(uri):
"""Reflects all tables to declaratives

Given a valid engine URI and declarative_base base class
reflects all tables and imports them to the global namespace.

Returns a session object bound to the engine created.
"""

# create an unbound base our objects will inherit from
	Base = declarative_base()

	engine = create_engine(uri)
	metadata = MetaData(bind=engine)
	Base.metadata = metadata

	g = globals()

	metadata.reflect()

	for tablename, tableobj in metadata.tables.items():
	    g[tablename] = type(str(tablename), (Base,), {'__table__' : tableobj })
	    print("Reflecting {0}".format(tablename))

	Session = sessionmaker(bind=engine)
	return Session()


# set to database credentials/host
CONNECTION_URI = "postgres://..."

session = reflect_all_tables_to_declarative(CONNECTION_URI)

# do something with the session and the orm objects
results = session.query(some_table_name).all()




# 2
app.config['SQLALCHEMY_DATABASE_URI'] = \
	"mysql://mengjiao:6GpNU4GfD434N5dj@kibot-data.cgbzucciybhz.us-east-1.rds.amazonaws.com/mengjiao"
db = SQLAlchemy(app)
class User(db.Model):
	id = db.Column(db.Integer, primary_key = True)



# 3
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///webmgmt.db', convert_unicode=True, echo=False)
Base = declarative_base()
Base.metadata.reflect(engine)


from sqlalchemy.orm import relationship, backref

class Users(Base):
    __table__ = Base.metadata.tables['users']


if __name__ == '__main__':
    from sqlalchemy.orm import scoped_session, sessionmaker, Query
    db_session = scoped_session(sessionmaker(bind=engine))
    for item in db_session.query(Users.id, Users.name):
        print item


# 4
class Buildings(db.Model):
    __table__ = db.Model.metadata.tables['BUILDING']

    def __repr__(self):
        return self.DISTRICT




