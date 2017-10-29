from flask import session, redirect, url_for, render_template, request
from . import main
from flask_socketio import emit
from bson.json_util import dumps
from app.database import db, serializeState, deserializeState
from app.models.bulletinBoardState import BulletinBoardState
from app.models.electionAuthorityState import ElectionAuthorityState
from app.models.printingAuthorityState import PrintingAuthorityState
from .. import socketio
from app.voteSimulator import VoteSimulator
from flask.ext.cors import CORS, cross_origin
from app.main.syncService import syncElections, syncBulletinBoard, SyncType, syncPrintingAuthority, syncElectionStatus, syncVoters, syncElectionAuthorities
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
    db.bulletinBoardStates.insert({'election':str(id), 'state' : serializeState(newBBState)})

    # create new electionAuthority states
    for j in range(3):
        newAuthState = ElectionAuthorityState(j)
        db.electionAuthorityStates.insert({'election': str(id), 'authorityID': j, 'state': serializeState(newAuthState)})


    printingAuthState =  PrintingAuthorityState()
    # create new printing authority state
    db.printingAuthorityStates.insert({'election':str(id), 'state' : serializeState(printingAuthState)})

    # update the election list on all clients
    syncElections(SyncType.BROADCAST)
    # return the new elections id to the client so it can load the overview directly
    return json.dumps({'id': str(id)})


@main.route('/setUpElection', methods=['POST'])
@cross_origin(origin='*')
def setUpElection():
    data = request.json
    electionId = data["election"]
    numberOfVoters = json.loads(data["numberOfVoters"])
    candidates = json.loads(data["candidates"])
    countingCircles = json.loads(data["countingCircles"])
    numberOfSelections = json.loads(data["numberOfSelections"])
    numberOfCandidates = json.loads(data["numberOfCandidates"])

    try:
        # validate vote parameters
        if len(candidates) != sum(numberOfCandidates):
            raise RuntimeError("The numberOfCandidates must match the number of candidates")
        if numberOfVoters != len(countingCircles):
            raise RuntimeError("The length of countingCircles must match the number of voters")
        if len(numberOfSelections) != len(numberOfCandidates):
            raise RuntimeError("The length of numberOfSelections must match the length of numberOfCandidates")

        # prepare voteSimulator
        sim = VoteSimulator(electionId)

        # perform action
        sim.setupElection(numberOfVoters, countingCircles, candidates, numberOfCandidates, numberOfSelections)

        # retrieve and persist modified state
        sim.persist()

        syncBulletinBoard(electionId, SyncType.ROOM)
        syncPrintingAuthority(electionId, SyncType.ROOM)

        # update election status
        sim.updateStatus(1)
    except Exception as ex:
        return json.dumps({'result': 'error', 'message': str(ex) })

    return json.dumps({'result': 'success'})


@main.route('/printVotingCards', methods=['POST'])
@cross_origin(origin='*')
def printVotingCards():
    electionId = request.json["election"]

    try:
        sim = VoteSimulator(electionId)             # prepare voteSimulator
        sim.printVotingCards()
        sim.persist()                               # persist the modified state

        syncPrintingAuthority(electionId, SyncType.ROOM)

        # update election status
        sim.updateStatus(2)


    except Exception as ex:
        return json.dumps({'result': 'error', })

    return json.dumps({'result': 'success'})


@main.route('/sendVotingCards', methods=['POST'])
@cross_origin(origin='*')
def sendVotingCards():
    electionId = request.json["election"]

    try:
        sim = VoteSimulator(electionId)             # prepare voteSimulator
        sim.sendVotingCards()
        sim.persist()                               # persist the modified state

        syncVoters(electionId, SyncType.ROOM)

        # update election status
        sim.updateStatus(3)


    except Exception as ex:
        return json.dumps({'result': 'error', })

    return json.dumps({'result': 'success'})

@main.route('/debugVotingSim', methods=['POST'])
@cross_origin(origin='*')
def debugVotingSim():
    electionId = request.json["election"]
    from gmpy2 import mpz
    try:
        sim = VoteSimulator(electionId)             # prepare voteSimulator
        sim.authorities[0].publicKey = mpz(33333)
        sim.persist()
        syncElectionAuthorities(electionId, SyncType.ROOM)
        print(sim)
    except Exception as ex:
        return json.dumps({'result': 'error', })

    return json.dumps({'result': 'success'})