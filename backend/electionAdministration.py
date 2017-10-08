import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from flask_socketio import SocketIO, emit
from bson.json_util import dumps
from demonstrator.backend.database import db
import json

def syncElections():
    res = db.elections.find()
    elections = dumps(res)
    emit('syncElections',elections , broadcast=True)

def createElection(data):
    id = db.elections.insert({'title': data["title"]})
    db.electorateData.insert({'election':str(id), 'counter' : 0})
    syncElections()

def syncElectionData(election, room):
    data = db.electorateData.find_one({'election':election})
    jsonRes = json.dumps({'election': data['election'], 'counter': data['counter']})
    emit('syncElectionData', jsonRes, room=room)
