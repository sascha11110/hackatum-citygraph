import os
from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://monogo:27017/hackatumdb"

mongo = PyMongo(app)

from app import routes
