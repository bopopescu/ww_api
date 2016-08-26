from flask import Flask
from flask_restful import Resource, Api, reqparse
from sqlalchemy import create_engine, MetaData


from .whalewisdom.views import analysts
from .app import app






app.register_blueprint(analysts)