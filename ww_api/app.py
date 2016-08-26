from .database import db
from flask import Flask
from flask_restful import Resource, Api, reqparse
from sqlalchemy import create_engine, MetaData


def create_app():
	app = Flask(__name__)
	app.config.from_object('config')
	db.init_app(app)
	app.app_context().push()
	db.Model.metadata.reflect(db.engine)
	api = Api(app)
	return app


app = create_app()