import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from flask_socketio import emit
from backend.app.database import db
import json
from .. import socketio

# OBSERVERS

@socketio.on('increment')
def increment(data):
    counterRecord = db.counter.find_one({'election':data["election"]})
    replaceCounter = counterRecord.copy()
    replaceCounter["counter"] = replaceCounter["counter"] + 1
    db.counter.replace_one(counterRecord, replaceCounter)
    syncCounter(data['election'])


# EMITTERS

def syncCounter(election):
    data = db.counter.find_one({'election':election})
    jsonRes = json.dumps({'election': data['election'], 'counter': data['counter']})
    emit('syncCounter', jsonRes, room=election)
