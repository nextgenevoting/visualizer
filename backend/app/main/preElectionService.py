from flask import session, redirect, url_for, render_template, request
from . import main
from flask_socketio import emit
from bson.json_util import dumps
from app.database import db, saveComplex, loadComplex
from app.models.bulletinBoardState import BulletinBoardState
from app.models.electionAuthorityState import ElectionAuthorityState
from .. import socketio
from app.voteSimulator import VoteSimulator
from flask.ext.cors import CORS, cross_origin
from app.main.syncService import syncElections, syncElectionData
from bson.objectid import ObjectId

import json

# LISTENERS

@main.route('/createElection', methods=['POST'])
@cross_origin(origin='*')
def createElection():
    data = request.json

    # Create a new election
    id = db.elections.insert({'title': data["title"], 'status': 0})

    # create a new (empty) BulletinBoardState
    newBBState =  BulletinBoardState(str(id))
    db.bulletinBoardStates.insert({'election':str(id), 'state' : saveComplex(newBBState)})

    # create new electionAuthority states
    for j in range(3):
        newAuthState = ElectionAuthorityState(j)
        db.electionAuthorityStates.insert({'election': str(id), 'authorityID': j, 'state': saveComplex(newAuthState)})

    # Create a new counter state (for testing purposes only)
    db.counter.insert({'election': str(id), 'counter': 0})

    # update the election list on all clients
    syncElections(True)
    # return the new elections id to the client so it can load the overview directly
    return json.dumps({'id': str(id)})


@socketio.on('setUpElection')
def setUpElection(data):
    electionId = data["election"]

    # prepare voteSimulator
    sim = VoteSimulator(electionId)

    # perform action
    sim.setupElection(["Voter1", "Voter 2"], [1], ["Clinton", "Trump"], [1], [1])

    # retrieve and persist modified state
    sim.persist()

    db.elections.update_one({'_id': ObjectId(electionId)}, {"$set": {"status" : 1}}, upsert=False)

    syncElectionData(electionId)


