from flask import render_template
from app import app
from app import mongo


@app.route('/')
@app.route('/index')
def index():
    online_users = mongo.db.users.find({"online": True})
    return render_template('index.html')


@app.route('/proposal')
def proposal():
    return render_template('timeline.html')
