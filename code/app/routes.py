import os
import json
from flask import render_template
from flask import request
from app import app
from app import mongo
from app import APP_STATIC
from app.logic.waypoints import assemble_waypoints
from app.logic.waypoints import status_color
from app.logic.waypoints import type_info
from pymongo import TEXT
from bson.objectid import ObjectId


@app.route('/')
@app.route('/index')
def index():
    proposals = []
    search = ''
    searched = False

    if request.args.get('search'):
        searched = True
        search = request.args.get('search')
        proposals = list(mongo.db.proposals.find(
            {'$text': {'$search': search}}
        ))

    return render_template('index.html',
                           proposals=proposals,
                           search=search,
                           searched=searched)


@app.route('/proposal/<page_id>')
def proposal(page_id):
    proposal = mongo.db.proposals.find_one({'_id': ObjectId(page_id)})
    waypoints = assemble_waypoints(proposal)
    sc = status_color(proposal)

    return render_template('timeline.html',
                           proposal=proposal,
                           sc=sc,
                           ti=type_info(proposal),
                           waypoints=waypoints)


@app.route('/import_data')
def import_data():
    with open(os.path.join(APP_STATIC, 'data/proposals.json')) as f:
        data = json.loads(f.read())
        mongo.db.proposals.remove()
        i = 0
        for p in data:
            subject = p['subject']
            subject = subject.replace('<br />', '')
            mongo.db.proposals.insert({
                'ris_id': p['id'],
                'initiator': p['application_by'],
                'date': p['application_date'],
                'department': p['department'],
                'done_date': p['done_date'],
                'editing': p['editing'],
                'legislative_period': p['legislative_period'],
                'processing_period': p['processing_period'],
                'status': p['status'],
                'subject': subject,
                'type': p['type'],
                'results': p['results'],
            })
            i += 1
            if i > 100:
                pass

        num_proposals = mongo.db.proposals.count()
        out = 'Es gibt jetzt ' + \
              str(num_proposals) + ' Anträge im System.'

        # mongo.db.proposals.create_index('subject')
        mongo.db.proposals.create_index(
            [('subject', TEXT)])

        return out
    return 'nicht importiert'
