import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from flask_socketio import SocketIO, emit
from bson.json_util import dumps
from backend.app.main.database import db, saveComplex, loadComplex
from backend.app.main.models.electionParams import ElectionParams
import json
from .. import socketio

# EVENTS

@socketio.on('createElection')
def createElection(data):
    print("CREATE ELECTION!!!")
    id = db.elections.insert({'title': data["title"]})
    db.counter.insert({'election': str(id), 'counter': 0})
    syncElections(True)

@socketio.on('setUpElection')
def setUpElection(data):
    electionParams = ElectionParams(data["election"], ["Voter1", "Voter 2"], [1], ["Clinton", "Trump"], [1], [1], [[1],[1]])
    db.electorateData.insert({'election':data["election"], 'data' : saveComplex(electionParams)})
    syncElectorateData(data["election"])


# FUNCTIONS

def syncElections(broadcast):
    res = db.elections.find()
    elections = dumps(res)
    emit('syncElections',elections , broadcast=broadcast)

def syncElectorateData(electionID):
    electorateData = db.electorateData.find_one({'election':electionID})
    if electorateData != None:
        electionParams = loadComplex(electorateData["data"])
        jsonRes = dumps({"election": electionID, "v": electionParams.voters, "c" : electionParams.candidates})
    else:
        jsonRes = dumps({"election": electionID, "v": [], "c": []})
    emit('syncElectionData', jsonRes, room=electionID)
