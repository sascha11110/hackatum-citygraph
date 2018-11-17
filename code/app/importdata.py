import os
import json

from app import app
from app import mongo
from app import APP_STATIC


def importdocument():
    with open(os.path.join(APP_STATIC, 'data/documents.json')) as f:
        data = json.loads(f.read())
        mongo.db.documents.remove()
        i = 0
        for p in data:
            mongo.db.documents.insert({
                'ris_id': p['id'],
                'documents': p['documents'],
            })
            
            
            num_documents = mongo.db.documents.count()
            out = 'Es gibt jetzt ' + \
                str(num_documents) + ' Anträge im System.'
            
        return out
    return 'nicht importiert'
