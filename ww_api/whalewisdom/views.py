from flask import Flask, request, jsonify, abort, Response, current_app, g, Blueprint
from flask_restful import Resource, Api, reqparse
from json import dumps
import json
from functools import wraps
from bson import json_util
from flask.json import JSONEncoder

from .models import Analysts, Pagination





analysts = Blueprint('analysts', __name__)

@analysts.route('/analysts', methods = ['GET'])
# @app.route('/analysts', methods = ['GET'])
# @require_app_key
def get_analysts():
	picture_base_url = "https://trstorage1.blob.core.windows.net/expert-pictures/"
	parser = reqparse.RequestParser()
	parser.add_argument('page', type=str)
	args = parser.parse_args()
	page = args['page']
	resultSet = Analysts.query.limit(1000).all().Pagination()
	# resultSet = Analysts.query.limit(1000).all()
	empList = []
	for d in resultSet:
		dictionary = {}
		dictionary['duut_pk'] = d.duut_pk
		dictionary['analystName'] = d.analystName
		dictionary['firmName'] = d.firmName
		# dictionary['recommendation'] = d[4]
		# dictionary['recommendationDate'] = d[5].strftime('%Y-%m-%d')
		# dictionary['experUID'] = d[6]
		# dictionary['url'] = d[7]
		# dictionary['expertPictureURL'] = picture_base_url + str(d[8])
		# dictionary['analystRank'] = d[9]
		# dictionary['numberOfRankedExperts'] = d[10]
		# dictionary['successRate'] = d[11]
		# dictionary['excessReturn'] = d[12]
		# dictionary['totalRecommendations'] = d[13]
		# dictionary['goodRecommendations'] = d[14]
		# dictionary['numOfStars'] = d[15]
		# dictionary['stockSuccessRate'] = d[16]
		# dictionary['stockAvgReturn'] = d[17]
		# dictionary['articleTitle'] = d[18]
		# dictionary['articleSite'] = d[19]
		# dictionary['priceTarget'] = d[20]
		# dictionary['ticker'] = d[21]
		# dictionary['timestamp'] = d[22].strftime('%Y-%m-%d %H:%M:%S')
		# dictionary['analystAction'] = d[23]
		empList.append(dictionary)
	data = json.dumps(empList)
	resp = Response(data, status=200, mimetype='application/json')
	return resp

