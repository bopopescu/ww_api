from flask import Flask
from flask_sqlalchemy import SQLALchemy


db = SQLALchemy()


def create_app():
	app = Flask(__name__)
	db.init_app(app)
	return app


def create_app():
	app = Flask(__name__)
	app.config['SQLALCHEMY_DATABASE_URI'] = \
	"mysql://mengjiao:6GpNU4GfD434N5dj@kibot-data.cgbzucciybhz.us-east-1.rds.amazonaws.com/mengjiao"
	db = SQLAlchemy(app)
	return app



def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()




engine = create_engine("mysql://Classify_Prod:f8WhcpDVMEv5LYEZ@kibot-data.cgbzucciybhz.us-east-1.rds.amazonaws.com/Classify_Prod", encoding = 'utf-8', echo = Ture)


mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'Classify_Prod'
app.config['MYSQL_DATABASE_PASSWORD'] = 'f8WhcpDVMEv5LYEZ'
app.config['MYSQL_DATABASE_DB'] = 'Classify_Prod'
app.config['MYSQL_DATABASE_HOST'] = 'kibot-data.cgbzucciybhz.us-east-1.rds.amazonaws.com'





class User(db.Model):
	id = db.Column(db.Integer, primary_key = True)
