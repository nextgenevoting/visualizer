import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from flask_socketio import SocketIO, emit
from bson.json_util import dumps
from demonstrator.backend.database import db

def syncElections():
    res = db.elections.find()
    elections = dumps(res)
    emit('syncElections',elections , broadcast=True)

def createElection(data):
    db.elections.insert({'title': data["title"]})
    syncElections()