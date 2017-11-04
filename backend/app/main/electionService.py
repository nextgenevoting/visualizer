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
from app.main.syncService import syncElections, syncBulletinBoard, SyncType, syncPrintingAuthority, syncElectionStatus, syncVoters, syncElectionAuthorities, fullSync
from bson.objectid import ObjectId

import json

# LISTENERS

@main.route('/castVote', methods=['POST'])
@cross_origin(origin='*')
def castVote():
    data = request.json
    electionId = data["election"]
    selection = data["selection"]
    voterId = data["voterId"]
    votingCode = data["votingCode"]

    try:
        # prepare voteSimulator
        sim = VoteSimulator(electionId)

        # perform action
        sim.castVote(voterId, selection, votingCode)

        # retrieve and persist modified state
        sim.persist()

        syncElectionAuthorities(electionId, SyncType.ROOM)
        syncVoters(electionId, SyncType.ROOM)

    except Exception as ex:
        return json.dumps({'result': 'error', 'message': str(ex)})

    return json.dumps({'result': 'success'})


@main.route('/checkVote', methods=['POST'])
@cross_origin(origin='*')
def checkVote():
    data = request.json
    electionId = data["election"]
    voterId = data["voterId"]
    authorityId = data["authorityId"]

    try:
        # prepare voteSimulator
        sim = VoteSimulator(electionId)

        # perform action
        sim.checkVote(voterId, authorityId)

        # retrieve and persist modified state
        sim.persist()

        syncElectionAuthorities(electionId, SyncType.ROOM)
        syncVoters(electionId, SyncType.ROOM)
    except Exception as ex:
        return json.dumps({'result': 'error', 'message': str(ex)})

    return json.dumps({'result': 'success'})

@main.route('/respond', methods=['POST'])
@cross_origin(origin='*')
def respond():
    data = request.json
    electionId = data["election"]
    voterId = data["voterId"]
    authorityId = data["authorityId"]

    try:
        # prepare voteSimulator
        sim = VoteSimulator(electionId)

        # perform action
        sim.respond(voterId, authorityId)

        # retrieve and persist modified state
        sim.persist()

        syncElectionAuthorities(electionId, SyncType.ROOM)
        syncVoters(electionId, SyncType.ROOM)
    except Exception as ex:
        return json.dumps({'result': 'error', 'message': str(ex)})

    return json.dumps({'result': 'success'})

@main.route('/discardBallot', methods=['POST'])
@cross_origin(origin='*')
def discardBallot():
    data = request.json
    electionId = data["election"]
    voterId = data["voterId"]
    authorityId = data["authorityId"]

    try:
        # prepare voteSimulator
        sim = VoteSimulator(electionId)

        # perform action
        sim.discardBallot(voterId, authorityId)

        # retrieve and persist modified state
        sim.persist()

        syncElectionAuthorities(electionId, SyncType.ROOM)
        syncVoters(electionId, SyncType.ROOM)
    except Exception as ex:
        return json.dumps({'result': 'error', 'message': str(ex)})

    return json.dumps({'result': 'success'})



@main.route('/confirmVote', methods=['POST'])
@cross_origin(origin='*')
def confirmVote():
    data = request.json
    electionId = data["election"]
    voterId = data["voterId"]
    confirmationCode = data["confirmationCode"]

    try:
        # prepare voteSimulator
        sim = VoteSimulator(electionId)

        # perform action
        sim.confirmVote(voterId, confirmationCode)

        # retrieve and persist modified state
        sim.persist()

        syncElectionAuthorities(electionId, SyncType.ROOM)
        syncVoters(electionId, SyncType.ROOM)
    except Exception as ex:
        return json.dumps({'result': 'error', 'message': str(ex)})

    return json.dumps({'result': 'success'})



@main.route('/checkConfirmation', methods=['POST'])
@cross_origin(origin='*')
def checkConfirmation():
    data = request.json
    electionId = data["election"]
    voterId = data["voterId"]
    authorityId = data["authorityId"]

    try:
        # prepare voteSimulator
        sim = VoteSimulator(electionId)

        # perform action
        sim.checkConfirmation(voterId, authorityId)

        # retrieve and persist modified state
        sim.persist()

        syncElectionAuthorities(electionId, SyncType.ROOM)
        syncVoters(electionId, SyncType.ROOM)
    except Exception as ex:
        return json.dumps({'result': 'error', 'message': str(ex)})

    return json.dumps({'result': 'success'})

@main.route('/finalize', methods=['POST'])
@cross_origin(origin='*')
def finalize():
    data = request.json
    electionId = data["election"]
    voterId = data["voterId"]
    authorityId = data["authorityId"]

    try:
        # prepare voteSimulator
        sim = VoteSimulator(electionId)

        # perform action
        sim.finalize(voterId, authorityId)

        # retrieve and persist modified state
        sim.persist()

        syncElectionAuthorities(electionId, SyncType.ROOM)
        syncVoters(electionId, SyncType.ROOM)
    except Exception as ex:
        return json.dumps({'result': 'error', 'message': str(ex)})

    return json.dumps({'result': 'success'})

@main.route('/setAutoMode', methods=['POST'])
@cross_origin(origin='*')
def setAutoMode():
    data = request.json
    electionId = data["election"]
    authorityId = data["authorityId"]
    value = data["value"]

    try:
        # prepare voteSimulator
        sim = VoteSimulator(electionId)

        # perform action
        sim.authorities[authorityId].autoCheck = value

        # retrieve and persist modified state
        sim.persist()

        syncElectionAuthorities(electionId, SyncType.ROOM)
    except Exception as ex:
        return json.dumps({'result': 'error', 'message': str(ex)})

    return json.dumps({'result': 'success'})
