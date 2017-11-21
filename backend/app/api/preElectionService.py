from flask import session, redirect, url_for, render_template, request
from . import main
from flask_socketio import emit
from bson.json_util import dumps
from app.database import db, serializeState, deserializeState
from app.states.bulletinBoardState import BulletinBoardState
from app.states.electionAuthorityState import ElectionAuthorityState
from app.states.printingAuthorityState import PrintingAuthorityState
from app.states.electionAdministratorState import ElectionAdministratorState
from .. import socketio
from app.voteSimulator import VoteSimulator
from flask.ext.cors import CORS, cross_origin
from app.api.syncService import *
from bson.objectid import ObjectId
from app.utils.errorhandling import make_error
import json
import pprint


# LISTENERS

@main.route('/createElection', methods=['POST'])
@cross_origin(origin='*')
def createElection():
    data = request.json

    try:
        # Create a new election
        id = db.elections.insert({'title': data["title"], 'status': 0})

        # create a new (empty) BulletinBoardState
        newBBState =  BulletinBoardState(str(id))
        db.bulletinBoardStates.insert({'election':str(id), 'state' : serializeState(newBBState)})

        # create new electionAuthority states
        for j in range(3):
            newAuthState = ElectionAuthorityState(j)
            db.electionAuthorityStates.insert({'election': str(id), 'authorityID': j, 'state': serializeState(newAuthState)})

        # create new printing authority state
        printingAuthState =  PrintingAuthorityState()
        db.printingAuthorityStates.insert({'election':str(id), 'state' : serializeState(printingAuthState)})

        # create new election administrator state
        electionAdminState =  ElectionAdministratorState()
        db.electionAdministratorStates.insert({'election':str(id), 'state' : serializeState(electionAdminState)})

        # update the election list on all clients
        syncElections(SyncType.BROADCAST)
        # return the new elections id to the client so it can load the overview directly
    except Exception as ex:
        return make_error(500, str(ex))

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

        #patches = sim.getJSONPatches()
        # retrieve and persist modified state
        patches = sim.persist()
        syncPatches(electionId, SyncType.ROOM, patches)

        # update election status
        sim.updateStatus(1)
    except Exception as ex:
        raise ex
        return make_error(500, str(ex))

    return json.dumps({'result': 'success'})


@main.route('/printVotingCards', methods=['POST'])
@cross_origin(origin='*')
def printVotingCards():
    electionId = request.json["election"]

    try:
        sim = VoteSimulator(electionId)             # prepare voteSimulator
        sim.printVotingCards()

        patches = sim.persist()
        syncPatches(electionId, SyncType.ROOM, patches)

        # update election status
        sim.updateStatus(2)

    except Exception as ex:
        return make_error(500, str(ex))

    return json.dumps({'result': 'success'})


@main.route('/sendVotingCards', methods=['POST'])
@cross_origin(origin='*')
def sendVotingCards():
    electionId = request.json["election"]

    try:
        sim = VoteSimulator(electionId)             # prepare voteSimulator
        sim.sendVotingCards()
        patches = sim.persist()
        syncPatches(electionId, SyncType.ROOM, patches)

        # update election status
        sim.updateStatus(3)

    except Exception as ex:
        return make_error(500, str(ex))

    return json.dumps({'result': 'success'})

@main.route('/debugVotingSim', methods=['POST'])
@cross_origin(origin='*')
def debugVotingSim():
    electionId = request.json["election"]
    from gmpy2 import mpz
    try:
        #sim = VoteSimulator(electionId)             # prepare voteSimulator
        #from chvote.Types import Ballot
        #sim.bulletinBoard.confirmations[0].finalizations.append(1)
        #patches = sim.persist()
        #syncPatches(electionId, SyncType.ROOM, patches)
        import jsonpatch
        import copy
        from chvote.Types import VoterConfirmation
        from app.utils.JsonParser import mpzconverter

        #class MyObject(object):
        #    def __init__(self):
        #       self.someList = [VoterConfirmation(1,2,3)]


        #new = MyObject()
        #old = copy.deepcopy(new)

        #new.someList[0].finalizations.append(1)
        #oldNormalized = json.loads(json.dumps(old, default=mpzconverter))
        #newNormalized = json.loads(json.dumps(new, default=mpzconverter))
        #patches = jsonpatch.make_patch(json.loads(json.dumps(old, default=mpzconverter)), json.loads(json.dumps(new, default=mpzconverter))).patch

        old = {'someDict': [{'someNumber': 0, 'someArray': [1, 2, 3]}]}

        new = {'someDict': [{'someNumber': 0, 'someArray': [1, 2, 3, 4]}]}

        patches = jsonpatch.make_patch(old,new)

    except Exception as ex:
        return make_error(500, str(ex))

    return json.dumps({'result': 'success'})
