from flaskext.mysql import MySQL
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import scoped_session, sessionmaker, Query
from flask import Flask
# mysql = MySQL()



# engine = create_engine('mysql://mengjiao:6GpNU4GfD434N5dj@kibot-data.cgbzucciybhz.us-east-1.rds.amazonaws.com/mengjiao', convert_unicode=True, echo=False)
# Base = declarative_base()
# Base.metadata.reflect(engine)


# db_session = scoped_session(sessionmaker(autocommit=False,autoflush=False,bind=engine))



# class Stock(Base):
#     __table__ = Base.metadata.tables['tr_Stock']


# for item in db_session.query(Stock.id, Stock.ticker):
# 	print item


# ---------------------------

db = SQLAlchemy()
# app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = \
# 	"mysql://mengjiao:6GpNU4GfD434N5dj@kibot-data.cgbzucciybhz.us-east-1.rds.amazonaws.com/mengjiao"

# app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True



# db.init_app(app)
# app.app_context().push()



# db.Model.metadata.reflect(db.engine)


# class Stock(db.Model):
#     __table__ = db.Model.metadata.tables['tr_Stock']


# db_session = scoped_session(sessionmaker(autocommit=False,autoflush=False,bind=db.engine))




# class Bar(Base):
#     __table__ = Base.metadata.tables['bars']

# class Foo(Base):
#     __table__ = Base.metadata.tables['foos']

#     bar = relationship(Bar, primaryjoin='Foo.bar_id == Bar.bar_id')


# # Example usage (assuming foo has a column named foo_column1)

# foo = db.query(Foo).filter(Foo.foo_id = 1).one()
# print foo.foo_column1 = 1
# foo.foo_string_column = "foo"
# foo.bar.bar_column1 = 1



