from flask import Flask
from flask_restful import Resource, Api, reqparse

from .data import db
from .views import analysts

app = Flask(__name__)


app.config.from_object('config')


db.init_app(app)
api = Api(app)


app.register_blueprint(analysts)