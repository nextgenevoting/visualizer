import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from flask_socketio import emit
from bson.json_util import dumps
from backend.app.database import db, saveComplex, loadComplex
from backend.app.models.electionParams import ElectionParams
from .. import socketio

# OBSERVERS

@socketio.on('createElection')
def createElection(data):
    id = db.elections.insert({'title': data["title"]})
    db.counter.insert({'election': str(id), 'counter': 0})
    syncElections(True)

@socketio.on('setUpElection')
def setUpElection(data):
    electionParams = ElectionParams(data["election"], ["Voter1", "Voter 2"], [1], ["Clinton", "Trump"], [1], [1])
    db.electorateData.insert({'election':data["election"], 'data' : saveComplex(electionParams)})
    syncElectorateData(data["election"])


# EMITTERS
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
