from flask import session, redirect, url_for, render_template, request
from . import main
from .. import socketio
from app.voteSimulator import VoteSimulator
from flask.ext.cors import CORS, cross_origin
from app.main.syncService import syncElections, syncBulletinBoard, SyncType, syncPrintingAuthority, syncElectionStatus, syncVoters, syncElectionAuthorities, fullSync
from app.utils.errorhandling import make_error

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

    if len(selection) == 0:
        return make_error(400, "Empty selection")

    try:
        # prepare voteSimulator
        sim = VoteSimulator(electionId)

        # perform action
        sim.castVote(voterId, selection, votingCode)

        # retrieve and persist modified state
        sim.persist()

        syncElectionAuthorities(electionId, SyncType.ROOM)
        syncBulletinBoard(electionId, SyncType.ROOM)
        syncVoters(electionId, SyncType.ROOM)

    except Exception as ex:
        return make_error(500, str(ex))

    return json.dumps({'result': 'success'})


@main.route('/checkVote', methods=['POST'])
@cross_origin(origin='*')
def checkVote():
    data = request.json
    electionId = data["election"]
    authorityId = data["authorityId"]
    ballotId = data["ballotId"]

    try:
        # prepare voteSimulator
        sim = VoteSimulator(electionId)

        # perform action
        sim.checkVote(ballotId, authorityId)

        # retrieve and persist modified state
        sim.persist()

        syncElectionAuthorities(electionId, SyncType.ROOM)
        syncBulletinBoard(electionId, SyncType.ROOM)
        syncVoters(electionId, SyncType.ROOM)
    except Exception as ex:
        return make_error(500, str(ex))

    return json.dumps({'id': str(id)})

@main.route('/respond', methods=['POST'])
@cross_origin(origin='*')
def respond():
    data = request.json
    electionId = data["election"]
    ballotId = data["ballotId"]
    authorityId = data["authorityId"]

    try:
        # prepare voteSimulator
        sim = VoteSimulator(electionId)

        # perform action
        sim.respond(ballotId, authorityId)

        # retrieve and persist modified state
        sim.persist()

        syncBulletinBoard(electionId, SyncType.ROOM)
        syncElectionAuthorities(electionId, SyncType.ROOM)
        syncVoters(electionId, SyncType.ROOM)
    except Exception as ex:
        return make_error(500, str(ex))

    return json.dumps({'id': str(id)})

@main.route('/discardBallot', methods=['POST'])
@cross_origin(origin='*')
def discardBallot():
    data = request.json
    electionId = data["election"]
    ballotId = data["ballotId"]
    authorityId = data["authorityId"]

    try:
        # prepare voteSimulator
        sim = VoteSimulator(electionId)

        # perform action
        sim.discardBallot(ballotId, authorityId)

        # retrieve and persist modified state
        sim.persist()

        syncElectionAuthorities(electionId, SyncType.ROOM)
    except Exception as ex:
        return make_error(500, str(ex))

    return json.dumps({'id': str(id)})



@main.route('/confirmVote', methods=['POST'])
@cross_origin(origin='*')
def confirmVote():
    data = request.json
    electionId = data["election"]
    voterId = data["voterId"]
    ballotId = data["ballotId"]
    confirmationCode = data["confirmationCode"]

    try:
        # prepare voteSimulator
        sim = VoteSimulator(electionId)

        # perform action
        sim.confirmVote(voterId, ballotId, confirmationCode)

        # retrieve and persist modified state
        sim.persist()

        syncBulletinBoard(electionId, SyncType.ROOM)
        syncElectionAuthorities(electionId, SyncType.ROOM)
        syncVoters(electionId, SyncType.ROOM)
    except Exception as ex:
        return make_error(500, str(ex))

    return json.dumps({'id': str(id)})



@main.route('/checkConfirmation', methods=['POST'])
@cross_origin(origin='*')
def checkConfirmation():
    data = request.json
    electionId = data["election"]
    confirmationId = data["confirmationId"]
    authorityId = data["authorityId"]

    try:
        # prepare voteSimulator
        sim = VoteSimulator(electionId)

        # perform action
        sim.checkConfirmation(confirmationId, authorityId)

        # retrieve and persist modified state
        sim.persist()

        syncBulletinBoard(electionId, SyncType.ROOM)
        syncElectionAuthorities(electionId, SyncType.ROOM)
        syncVoters(electionId, SyncType.ROOM)
    except Exception as ex:
        return make_error(500, str(ex))

    return json.dumps({'id': str(id)})

@main.route('/finalize', methods=['POST'])
@cross_origin(origin='*')
def finalize():
    data = request.json
    electionId = data["election"]
    confirmationId = data["confirmationId"]
    authorityId = data["authorityId"]

    try:
        # prepare voteSimulator
        sim = VoteSimulator(electionId)

        # perform action
        sim.finalize(confirmationId, authorityId)

        # retrieve and persist modified state
        sim.persist()

        syncBulletinBoard(electionId, SyncType.ROOM)
        syncElectionAuthorities(electionId, SyncType.ROOM)
        syncVoters(electionId, SyncType.ROOM)
    except Exception as ex:
        return make_error(500, str(ex))

    return json.dumps({'id': str(id)})

@main.route('/discardConfirmation', methods=['POST'])
@cross_origin(origin='*')
def discardConfirmation():
    data = request.json
    electionId = data["election"]
    confirmationId = data["confirmationId"]
    authorityId = data["authorityId"]

    try:
        # prepare voteSimulator
        sim = VoteSimulator(electionId)

        # perform action
        sim.discardConfirmation(confirmationId, authorityId)

        # retrieve and persist modified state
        sim.persist()

        syncElectionAuthorities(electionId, SyncType.ROOM)
    except Exception as ex:
        return make_error(500, str(ex))

    return json.dumps({'id': str(id)})



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
        return make_error(500, str(ex))

    return json.dumps({'id': str(id)})
