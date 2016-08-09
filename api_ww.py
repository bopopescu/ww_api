#!flask/bin/python
from flask import Flask, request, jsonify, abort, Response, current_app, g, Blueprint
from flask_restful import Resource, Api, reqparse
from json import dumps
from flask_mysqldb import MySQL
from flaskext.mysql import MySQL
from functools import wraps
import hashlib
from flask_httpauth import HTTPDigestAuth
from bson import json_util
import json
from flask.json import JSONEncoder
from datetime import date, datetime, timedelta
import time
from dateutil.relativedelta import relativedelta
from api_tiprank import analysts



mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'Classify_Prod'
app.config['MYSQL_DATABASE_PASSWORD'] = 'f8WhcpDVMEv5LYEZ'
app.config['MYSQL_DATABASE_DB'] = 'Classify_Prod'
app.config['MYSQL_DATABASE_HOST'] = 'kibot-data.cgbzucciybhz.us-east-1.rds.amazonaws.com'


mysql.init_app(app)

cnx = mysql.connect()
cur = cnx.cursor()

api = Api(app)




# -------------------------------------------Authentication---------------------------------------------------------

def calculate_hash(api_key):
    """
    @return: A hashkey for use to authenticate agains the API.
    """
    salt = "jdalakh2"
    return hashlib.md5(salt + api_key).hexdigest()


def get_apiauth_object_by_key(key):
	"""
	Query the datastorage for an API key.
	@return: apiauth sqlachemy object.
	"""
	hash_key = calculate_hash(key)
	cur.execute("SELECT pass FROM api_user WHERE pass = %s", [hash_key])
	r = cur.fetchone()
	return r

def match_api_keys(key):
	"""
	Match API keys and discard ip
	@param key: API key from request
	@param ip: remote host IP to match the key.
	@return: boolean
	"""
	if key is None:
		return False
	api_key = get_apiauth_object_by_key(key)
	if api_key is None:
		return False
	else:
		return True


def require_app_key(f):
	"""
	@param f: flask function
	@return: decorator, return the wrapped function or abort json object.
	"""
	@wraps(f)
	def decorated(*args, **kwargs):
		if match_api_keys(request.headers.get('X-APIKEY')):
			return f(*args, **kwargs)
		else:
			return "Could not verify your access level for that URL.\n You have to login with proper credentials."
			abort(401)
	return decorated



# -------------------------------------------Mysql---------------------------------------------------------
# app.register_blueprint(analysts)


@app.route('/')
def index():
    return "Welcome!"


class DecimalEncoder(json.JSONEncoder):
    def _iterencode(self, o, markers=None):
        if isinstance(o, decimal.Decimal):
            # wanted a simple yield str(o) in the next line,
            # but that would mean a yield on the line with super(...),
            # which wouldn't work (see my comment below), so...
            return (str(o) for o in [o])
        return super(DecimalEncoder, self)._iterencode(o, markers)




@app.route('/ww/filingStockRecords/<int:stock_id>', methods = ['GET'])
@require_app_key
def get_filingStockRecords(stock_id):
	cur.execute("SELECT * FROM ww_filing_stock_records WHERE stock_id = %s LIMIT 20 OFFSET 100", [stock_id])
	resultSet = cur.fetchall()
	empList = []
	for d in resultSet:
		dictionary = {}
		dictionary['filing_id'] = d[1]
		dictionary['stock_id'] = d[2]
		dictionary['name'] = d[3]
		dictionary['alt_name'] = d[4]
		dictionary['title'] = d[5]
		dictionary['cusip_number'] = d[6]
		dictionary['alt_cusip'] = d[7]
		dictionary['market_value'] = float(d[8])
		dictionary['shares'] = d[9]
		dictionary['security_type'] = d[10]
		dictionary['manager_number'] = d[11]
		dictionary['quarter_date'] = d[12]
		dictionary['quarter_id'] = d[13]
		empList.append(dictionary)
	data = json.dumps(empList, cls=DecimalEncoder)
	resp = Response(data, status=200, mimetype='application/json')
	return resp



@app.route('/ww/filerSummary/<int:filer_id>', methods = ['GET'])
@require_app_key
def get_filerSummary():
	cur.execute("SELECT * FROM ww_filing_stock_records WHERE stock_id = %s LIMIT 20 OFFSET 100", [stock_id])
	resultSet = cur.fetchall()
	empList = []
	for d in resultSet:
		dictionary = {}
		dictionary['filing_id'] = d[1]
		dictionary['stock_id'] = d[2]
		dictionary['name'] = d[3]
		dictionary['alt_name'] = d[4]
		dictionary['title'] = d[5]
		dictionary['cusip_number'] = d[6]
		dictionary['alt_cusip'] = d[7]
		dictionary['market_value'] = float(d[8])
		dictionary['shares'] = d[9]
		dictionary['security_type'] = d[10]
		dictionary['manager_number'] = d[11]
		dictionary['quarter_date'] = d[12]
		dictionary['quarter_id'] = d[13]
		empList.append(dictionary)
	data = json.dumps(empList, cls=DecimalEncoder)
	resp = Response(data, status=200, mimetype='application/json')
	return resp




@app.route('/ww/filerSummary/<int:filer_id>', methods = ['GET'])
@require_app_key
def get_filerSummary():
	cur.execute("SELECT * FROM ww_filing_stock_records WHERE stock_id = %s LIMIT 20 OFFSET 100", [stock_id])
	resultSet = cur.fetchall()
	empList = []
	for d in resultSet:
		dictionary = {}
		dictionary['filing_id'] = d[1]
		dictionary['stock_id'] = d[2]
		dictionary['name'] = d[3]
		dictionary['alt_name'] = d[4]
		dictionary['title'] = d[5]
		dictionary['cusip_number'] = d[6]
		dictionary['alt_cusip'] = d[7]
		dictionary['market_value'] = float(d[8])
		dictionary['shares'] = d[9]
		dictionary['security_type'] = d[10]
		dictionary['manager_number'] = d[11]
		dictionary['quarter_date'] = d[12]
		dictionary['quarter_id'] = d[13]
		empList.append(dictionary)
	data = json.dumps(empList, cls=DecimalEncoder)
	resp = Response(data, status=200, mimetype='application/json')
	return resp






# --------------------------------------------------Log-------------------------------------------------------
@app.before_request
def api_log():
	uri = request.url
	method = request.method
	api_key = request.headers.get('X-APIKEY')
	# ip_address = request.remote_addr
	ip_address = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
	timestamp=time.strftime('%Y-%m-%d %H:%M:%S')
	if match_api_keys(api_key):
		authorized = 1
	else:
		authorized = 0
	api_key = calculate_hash(api_key)
	cur.execute("INSERT INTO api_log(uri, method, api_key, ip_address, time, authorized) \
		VALUES(%s, %s, %s, %s, %s, %s)", [uri, method, api_key, ip_address, timestamp, authorized])
	cnx.commit()



if __name__ == '__main__':
    app.run(debug=True)


