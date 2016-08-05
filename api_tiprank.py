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
# from app.py import *

mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'mengjiao'
app.config['MYSQL_DATABASE_PASSWORD'] = '6GpNU4GfD434N5dj'
app.config['MYSQL_DATABASE_DB'] = 'mengjiao'
app.config['MYSQL_DATABASE_HOST'] = 'kibot-data.cgbzucciybhz.us-east-1.rds.amazonaws.com'


mysql.init_app(app)

cnx = mysql.connect()
cur = cnx.cursor()

api = Api(app)


picture_base_url = "https://trstorage1.blob.core.windows.net/expert-pictures/"


analysts = Blueprint('analysts',__name__)


@analysts.route('/analysts', methods = ['GET'])
# @require_app_key
def get_analysts():
	cur.execute("SELECT * FROM tr_Analyst LIMIT 1000")
	resultSet = cur.fetchall()
	empList = []
	for d in resultSet:
		dictionary = {}
		dictionary['duut_pk'] = d[0]
		dictionary['analystName'] = d[2]
		dictionary['firmName'] = d[3]
		dictionary['recommendation'] = d[4]
		dictionary['recommendationDate'] = d[5].strftime('%Y-%m-%d')
		dictionary['experUID'] = d[6]
		dictionary['url'] = d[7]
		dictionary['expertPictureURL'] = picture_base_url + str(d[8])
		dictionary['analystRank'] = d[9]
		dictionary['numberOfRankedExperts'] = d[10]
		dictionary['successRate'] = d[11]
		dictionary['excessReturn'] = d[12]
		dictionary['totalRecommendations'] = d[13]
		dictionary['goodRecommendations'] = d[14]
		dictionary['numOfStars'] = d[15]
		dictionary['stockSuccessRate'] = d[16]
		dictionary['stockAvgReturn'] = d[17]
		dictionary['articleTitle'] = d[18]
		dictionary['articleSite'] = d[19]
		dictionary['priceTarget'] = d[20]
		dictionary['ticker'] = d[21]
		dictionary['timestamp'] = d[22].strftime('%Y-%m-%d %H:%M:%S')
		dictionary['analystAction'] = d[23]
		empList.append(dictionary)
	data = json.dumps(empList)
	resp = Response(data, status=200, mimetype='application/json')
	return resp



# @app.route('/analysts/<string:ticker>', methods = ['GET'])
# @require_app_key
# def get_stock(ticker):
# 	parser = reqparse.RequestParser()
# 	parser.add_argument('sort', type=str)
# 	parser.add_argument('month', type=int)
# 	parser.add_argument('num', type=int)
# 	args = parser.parse_args()
# 	sort = args['sort']
# 	month = args['month']
# 	num = args['num']
# 	query = "SELECT * FROM tr_Analyst WHERE ticker = %s"
# 	param = [ticker]
# 	if month:
# 		today=time.strftime('%Y-%m-%d')
# 		x = datetime.strptime(today,'%Y-%m-%d').date()+relativedelta(months=-month)
# 		query = query + " " + "AND recommendationDate > %s"
# 		param.append(x)
# 	if sort == 'date':
# 		query = query + " " + "ORDER BY recommendationDate DESC"
# 	elif sort == 'rank':
# 		query = query + " " + "ORDER BY analystRank"
# 	if num:
# 		query = query + " " + "LIMIT %s"
# 		param.append(num)
# 	cur.execute(query, param)
# 	resultSet = cur.fetchall()
# 	empList = []
# 	for d in resultSet:
# 		dictionary = {}
# 		dictionary['duut_pk'] = d[0]
# 		dictionary['analystName'] = d[2]
# 		dictionary['firmName'] = d[3]
# 		dictionary['recommendation'] = d[4]
# 		dictionary['recommendationDate'] = d[5].strftime('%Y-%m-%d')
# 		dictionary['experUID'] = d[6]
# 		dictionary['url'] = d[7]
# 		dictionary['expertPictureURL'] = picture_base_url + str(d[8])
# 		dictionary['analystRank'] = d[9]
# 		dictionary['numberOfRankedExperts'] = d[10]
# 		dictionary['successRate'] = d[11]
# 		dictionary['excessReturn'] = d[12]
# 		dictionary['totalRecommendations'] = d[13]
# 		dictionary['goodRecommendations'] = d[14]
# 		dictionary['numOfStars'] = d[15]
# 		dictionary['stockSuccessRate'] = d[16]
# 		dictionary['stockAvgReturn'] = d[17]
# 		dictionary['articleTitle'] = d[18]
# 		dictionary['articleSite'] = d[19]
# 		dictionary['priceTarget'] = d[20]
# 		dictionary['ticker'] = d[21]
# 		dictionary['timestamp'] = d[22].strftime('%Y-%m-%d %H:%M:%S')
# 		dictionary['analystAction'] = d[23]
# 		empList.append(dictionary)
# 	data = json.dumps(empList)
# 	resp = Response(data, status=200, mimetype='application/json')
# 	return resp




# @app.route('/analysts/Overview', methods = ['GET'])
# @require_app_key
# def get_analyst():
# 	parser = reqparse.RequestParser()
# 	parser.add_argument('id', type=str)
# 	parser.add_argument('name', type=str)
# 	args = parser.parse_args()
# 	expertUID = args['id']
# 	analystName = args['name']
# 	if expertUID:
# 		cur.execute("SELECT * FROM tr_Analyst WHERE expertUID = %s LIMIT 1", [expertUID])
# 		resultSet = cur.fetchall()
# 	elif analystName:
# 		cur.execute("SELECT * FROM tr_Analyst WHERE analystName LIKE %s GROUP BY expertUID ", [analystName])
# 		resultSet = cur.fetchall()
# 	else:
# 		cur.execute("SELECT * FROM tr_Analyst GROUP BY expertUID ORDER BY analystRank")
# 		resultSet = cur.fetchall()
# 	empList = []
# 	for d in resultSet:
# 		dictionary = {}
# 		dictionary['analystName'] = d[2]
# 		dictionary['firmName'] = d[3]
# 		dictionary['experUID'] = d[6]
# 		dictionary['expertPictureURL'] = picture_base_url + str(d[8])
# 		dictionary['analystRank'] = d[9]
# 		dictionary['numberOfRankedExperts'] = d[10]
# 		dictionary['successRate'] = d[11]
# 		dictionary['excessReturn'] = d[12]
# 		dictionary['totalRecommendations'] = d[13]
# 		dictionary['goodRecommendations'] = d[14]
# 		dictionary['numOfStars'] = d[15]
# 		empList.append(dictionary)
# 	data = json.dumps(empList)
# 	resp = Response(data, status=200, mimetype='application/json')
# 	return resp


# @app.route('/rating', methods = ['GET'])
# @require_app_key
# def get_rating():
# 	parser = reqparse.RequestParser()
# 	parser.add_argument('id', type=str)
# 	parser.add_argument('name', type=str)
# 	parser.add_argument('sort', type=str)
# 	parser.add_argument('num', type=int)
# 	args = parser.parse_args()
# 	sort = args['sort']
# 	num = args['num']
# 	expertUID = args['id']
# 	analystName = args['name']
# 	query = "SELECT * FROM tr_Analyst"
# 	param = []
# 	flag = False
# 	if expertUID:
# 		query = query + " " + "WHERE expertUID = %s"
# 		param.append(expertUID)
# 		flag = True
# 	elif analystName:
# 		query = query + " " + "WHERE analystName LIKE %s"
# 		param.append(analystName)
# 		flag = True
# 	if flag:
# 		if sort == 'date':
# 			query = query + " " + "ORDER BY recommendationDate DESC"
# 		elif sort == 'rank':
# 			query = query + " " + "ORDER BY analystRank"
# 		if num:
# 			query = query + " " + "LIMIT %s"
# 			param.append(num)
# 	else:
# 		query = "SELECT * FROM tr_Analyst ORDER BY analystRank LIMIT 1000"
# 	cur.execute(query, param)
# 	resultSet = cur.fetchall()
# 	empList = []
# 	for d in resultSet:
# 		dictionary = {}
# 		dictionary['analystName'] = d[2]
# 		dictionary['firmName'] = d[3]
# 		dictionary['recommendation'] = d[4]
# 		dictionary['recommendationDate'] = d[5].strftime('%Y-%m-%d')
# 		dictionary['experUID'] = d[6]
# 		dictionary['url'] = d[7]
# 		dictionary['analystRank'] = d[9]
# 		dictionary['numberOfRankedExperts'] = d[10]
# 		dictionary['successRate'] = d[11]
# 		dictionary['excessReturn'] = d[12]
# 		dictionary['stockSuccessRate'] = d[16]
# 		dictionary['stockAvgReturn'] = d[17]
# 		dictionary['articleTitle'] = d[18]
# 		dictionary['articleSite'] = d[19]
# 		dictionary['priceTarget'] = d[20]
# 		dictionary['ticker'] = d[21]
# 		dictionary['timestamp'] = d[22].strftime('%Y-%m-%d %H:%M:%S')
# 		dictionary['analystAction'] = d[23] 
# 		empList.append(dictionary)
# 	data = json.dumps(empList)
# 	resp = Response(data, status=200, mimetype='application/json')
# 	return resp

