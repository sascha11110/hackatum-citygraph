import os
import json
from flask import render_template
from flask import request
from app import app
from app import mongo
from app import APP_STATIC


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    proposals = mongo.db.proposals.find()

    if request.method == 'POST':
        pass

    return render_template('index.html',
                           proposals=proposals)


@app.route('/proposal')
def proposal():
    return render_template('timeline.html')


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
                break

            num_proposals = mongo.db.proposals.count()
            out = 'Es gibt jetzt ' + \
                str(num_proposals) + ' Anträge im System.'

        return out
    return 'nicht importiert'
