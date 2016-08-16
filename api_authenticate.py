import hashlib
from functools import wraps

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