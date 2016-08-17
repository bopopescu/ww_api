

def generate_hash_key():
    """
    @return: A hashkey for use to authenticate agains the API.
    """
    return base64.b64encode(hashlib.sha256(str(random.getrandbits(256))).digest(),
                            random.choice(['rA', 'aZ', 'gQ', 'hH', 'hG', 'aR', 'DD'])).rstrip('==')



def get_apiauth_object_by_key(key):
    """
    Query the datastorage for an API key.
    @param ip: ip address
    @return: apiauth sqlachemy object.
    """
    return model.APIAuth.query.filter_by(key=key).first()

def match_api_keys(key, ip):
    """
   Match API keys and discard ip
   @param key: API key from request
   @param ip: remote host IP to match the key.
   @return: boolean
   """
   if key is None or ip is None:
      return False
   api_key = get_apiauth_object_by_key(key)
   if api_key is None:
      return False
   elif api_key.ip == "0.0.0.0":   # 0.0.0.0 means all IPs.
      return True
   elif api_key.key == key and api_key.ip == ip:
      return True
   return False

def require_app_key(f):
   """
   @param f: flask function
   @return: decorator, return the wrapped function or abort json object.
   """

   @wraps(f)
   def decorated(*args, **kwargs):
      if match_api_keys(request.args.get('key'), request.remote_addr):
         return f(*args, **kwargs)
      else:
         with log_to_file:
            log.warning("Unauthorized address trying to use API: " + request.remote_addr)
         abort(401)
      return decorated




#-------------------------------------------handle-json-format------------------------------------------------------
# 1
def date_handler(obj):
	return obj.isoformat
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    else:
        raise TypeError

print json.dumps(data, default=date_handler)
app.json_encoder = date_handler


# 2
class DatetimeEncoder(json.JSONEncoder):
    def default(obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%dT%H:%M:%SZ')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(obj)

json.dumps(dict,cls=DatetimeEncoder)


# 3
class SpecializedJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, date):
            return date.strftime("%Y-%m-%d")
        else:
        	return json.JSONEncoder.default(self, o)
            # super(SpecializedJSONEncoder, self).default()


app.json_encoder = DatetimeEncoder


#-------------------------------------------example------------------------------------------------------

from flask import Flask
from flask import g
from flask import Response
from flask import request
import json
import MySQLdb

app = Flask(__name__)

@app.before_request
def db_connect():
  g.conn = MySQLdb.connect(host='192.168.33.10',
                              user='test',
                              passwd='password',
                              db='test')
  g.cursor = g.conn.cursor()

@app.after_request
def db_disconnect(response):
  g.cursor.close()
  g.conn.close()
  return response

def query_db(query, args=(), one=False):
  g.cursor.execute(query, args)
  rv = [dict((g.cursor.description[idx][0], value)
  for idx, value in enumerate(row)) for row in g.cursor.fetchall()]
  return (rv[0] if rv else None) if one else rv

@app.route("/")
def hello():
  return "Hello World!"

@app.route("/names", methods=['GET'])
def names():
  result = query_db("SELECT firstname,lastname FROM test.name")
  data = json.dumps(result)
  resp = Response(data, status=200, mimetype='application/json')
  return resp

@app.route("/add", methods=['POST'])
def add():
  req_json = request.get_json()
  g.cursor.execute("INSERT INTO test.name (firstname, lastname) VALUES (%s,%s)", (req_json['firstname'], req_json['lastname']))
  g.conn.commit()
  resp = Response("Updated", status=201, mimetype='application/json')
  return resp

if __name__ == "__main__":
  app.run()




