#! flask/bin/python
from flask import Flask, request, jsonify, abort, Response
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask_mysqldb import MySQL
from flaskext.mysql import MySQL


from functools import wraps
import hashlib
import bcrypt
from eve import Eve
from eve.auth import BasicAuth
from flask import current_app as app1





mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'mengjiao'
app.config['MYSQL_DATABASE_PASSWORD'] = '6GpNU4GfD434N5dj'
app.config['MYSQL_DATABASE_DB'] = 'mengjiao'
app.config['MYSQL_DATABASE_HOST'] = 'kibot-data.cgbzucciybhz.us-east-1.rds.amazonaws.com'
mysql.init_app(app)

cur = mysql.connect().cursor()

api = Api(app)


@app.route('/')
def index():
    return "Welcome!"


# API Key for anthenticate
# api_key = request.headers.get('APIKEY')


# 1
def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == 'admin' and password == 'secret'

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


# 2
def check_auth(api_key):
    """This function is called to check if a username /
    password combination is valid.
    """
    return api_key == 'zxcvbnm'

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get('X-APIKEY')
        if not auth or not check_auth(auth):
            return authenticate()
        return f(*args, **kwargs)
    return decorated




@app.route('/secret-page', methods = ['GET'])
@requires_auth
def secret_page():
    # return render_template('secret_page.html')
    cur.execute("SELECT * FROM tr_Analyst LIMIT 4")
    rv = cur.fetchall()
    return jsonify( { 'Analysts': [i[0] for i in rv] } )


# 3
# The actual decorator function
def require_appkey(view_function):
    @wraps(view_function)
    # the new, post-decoration function. Note *args and **kwargs here.
    def decorated_function(*args, **kwargs):
        if request.args.get('key') and request.args.get('key') == APPKEY_HERE:
            return view_function(*args, **kwargs)
        else:
            abort(401)
    return decorated_function



@route('/users/', methods=['PUT'])
@require_appkey
def put_user():
    ...




def checkAppKey(fn):
    def inner(*args, **kwargs): #appkey should be in kwargs
        try:
            AppKey.get(appkey)
        except KeyError:
            raise AuthenticationError("Invalid appkey")
            #Whatever other errors can raise up such as db inaccessible
        #We were able to access that API key, so pass onward.
        #If you know nothing else will use the appkey after this, you can unset it.
        return fn(*args, **kwargs)
    return inner





# GET
@app.route('/analysts', methods = ['GET'])
def analysts():
    cur.execute("SELECT * FROM tr_Analyst LIMIT 3000")
    rv = cur.fetchall()
    return jsonify( { 'Analysts': [i for i in rv] } )




class Departments_Meta(Resource):
	def get(self):
		#Connect to databse
		conn = e.connect()
		#Perform query and return JSON data
		query = conn.execute("select distinct DEPARTMENT from salaries")
		return {'departments': [i[0] for i in query.cursor.fetchall()]}

class Departmental_Salary(Resource):
    def get(self, department_name):
    	conn = e.connect()
    	query = conn.execute("select * from salaries where Department='%s'"%department_name.upper())
        #Query the result and get cursor.Dumping that data to a JSON is looked by extension
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return result
    #We can have PUT,DELETE,POST here. But in our API GET implementation is sufficient
       
api.add_resource(Departmental_Salary, '/dept/<string:department_name>')
api.add_resource(Departments_Meta, '/departments')



@app.route("/Authenticate")
def Authenticate():
    username = request.args.get('UserName')
    password = request.args.get('Password')
    cursor = mysql.connect().cursor()
    cursor.execute("SELECT * from User where Username='" + username + "' and Password='" + password + "'")
    data = cursor.fetchone()
    if data is None:
     return "Username or Password is wrong"
    else:
     return "Logged in successfully"



if __name__ == '__main__':
    app.run(debug=True)




