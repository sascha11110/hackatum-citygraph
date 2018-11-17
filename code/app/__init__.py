import os
from flask import Flask
from flask_pymongo import PyMongo

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
APP_STATIC = os.path.join(APP_ROOT, 'static')
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://mongo:27017/hackatumdb"

mongo = PyMongo(app)

from app import routes
