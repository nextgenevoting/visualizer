import os
import sys

from flask_socketio import emit
from bson.json_util import dumps
from app.database import db, saveComplex, loadComplex
from app.models.bulletinBoardState import BulletinBoardState
from .. import socketio
from app.voteSimulator import VoteSimulator
import json

# LISTENERS

@socketio.on('createElection')
def createElection(data):
    id = db.elections.insert({'title': data["title"]})
    db.counter.insert({'election': str(id), 'counter': 0})
    syncElections(True)
    emit('createdElection',str(id) , broadcast=False)


@socketio.on('setUpElection')
def setUpElection(data):
    electionId = data["election"]

    # load states
    bbState = BulletinBoardState(electionId, ["Voter1", "Voter 2"], [1], ["Clinton", "Trump"], [1], [1])
    electionAuthorityStates = []

    # prepare voteSimulator
    sim = VoteSimulator(bbState, electionAuthorityStates)

    # perform action
    sim.genElectorateData()

    # retrieve and persist modified state
    newBBState = sim.bulletinBoardState
    db.bulletinBoardStates.insert({'election':electionId, 'state' : saveComplex(newBBState)})

    syncElectorateData(electionId)


# EMITTERS
def syncElections(broadcast):
    res = db.elections.find()
    elections = dumps(res)
    emit('syncElections',elections , broadcast=broadcast)

def syncElectorateData(electionID):
    bbState = db.bulletinBoardStates.find_one({'election':electionID})
    if bbState != None:
        bbState = loadComplex(bbState["state"])

        print(bbState.toJSON())
    else:
        raise RuntimeError("No BulletinBoardState for this election!")
    emit('syncElectionData', bbState.toJSON(), room=electionID)
