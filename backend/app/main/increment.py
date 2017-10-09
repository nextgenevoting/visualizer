import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from flask_socketio import SocketIO, emit
from bson.json_util import dumps
from backend.app.main.database import db, saveComplex, loadComplex
from backend.app.main.models.electionParams import ElectionParams
import json
from .. import socketio

# EVENTS
@socketio.on('increment')
def increment(data):
    print("INCREMENT:")
    print(data["election"])
    counterRecord = db.counter.find_one({'election':data["election"]})
    replaceCounter = counterRecord.copy()
    replaceCounter["counter"] = replaceCounter["counter"] + 1
    db.counter.replace_one(counterRecord, replaceCounter)
    syncCounter(data['election'])


def syncCounter(election):
    data = db.counter.find_one({'election':election})
    jsonRes = json.dumps({'election': data['election'], 'counter': data['counter']})
    emit('syncCounter', jsonRes, room=election)
