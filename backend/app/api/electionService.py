import sys, os, traceback
from flask import session, redirect, url_for, render_template, request
from . import main
from .. import socketio
from app.voteService import VoteService
from flask_cors import CORS, cross_origin
from app.api.syncService import syncPatches, SyncType
from app.utils.errorhandling import make_error

import json

# LISTENERS

@main.route('/castVote', methods=['POST'])
@cross_origin(origin='*')
def castVote():
    data = request.json
    print(data)
    electionId = data["election"]
    selection = data["selection"]
    selection = [int(x) for x in selection]
    selection.sort()
    voterId = data["voterId"]
    votingCode = data["votingCode"]
    manipulatedPublicCredential = data["manipulatedPublicCredential"]
    manipulatedPublicKey = data["manipulatedPublicKey"]


    if len(selection) == 0:
        return make_error(400, "Empty selection")

    try:
        # prepare voteService
        voteSvc = VoteService(electionId)

        # perform action
        voteSvc.castVote(voterId, selection, votingCode, manipulatedPublicCredential, manipulatedPublicKey)

        # retrieve and persist modified state
        patches = voteSvc.persist()
        syncPatches(electionId, SyncType.ROOM, patches)

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        return make_error(500, '%s:%s: %s. %s' % (fname, exc_tb.tb_lineno, e, traceback.format_exc()))

    return json.dumps({'result': 'success'})



@main.route('/abortVote', methods=['POST'])
@cross_origin(origin='*')
def abortVote():
    data = request.json
    electionId = data["election"]
    voterId = data["voterId"]

    try:
        # prepare voteService
        voteSvc = VoteService(electionId)

        # perform action
        voteSvc.abortVote(voterId)

        # retrieve and persist modified state
        patches = voteSvc.persist()
        syncPatches(electionId, SyncType.ROOM, patches)

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        return make_error(500, '%s:%s: %s. %s' % (fname, exc_tb.tb_lineno, e, traceback.format_exc()))

    return json.dumps({'result': 'success'})



@main.route('/checkVote', methods=['POST'])
@cross_origin(origin='*')
def checkVote():
    data = request.json
    electionId = data["election"]
    authorityId = data["authorityId"]
    ballotId = data["ballotId"]

    try:
        # prepare voteService
        voteSvc = VoteService(electionId)

        # perform action
        voteSvc.checkVote(ballotId, authorityId)

        # retrieve and persist modified state
        patches = voteSvc.persist()
        syncPatches(electionId, SyncType.ROOM, patches)

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        return make_error(500, '%s:%s: %s' % (fname, exc_tb.tb_lineno, e))

    return json.dumps({'id': str(id)})

@main.route('/respond', methods=['POST'])
@cross_origin(origin='*')
def respond():
    data = request.json
    electionId = data["election"]
    ballotId = data["ballotId"]
    authorityId = data["authorityId"]

    try:
        # prepare voteService
        voteSvc = VoteService(electionId)

        # perform action
        voteSvc.respond(ballotId, authorityId)

        # retrieve and persist modified state
        patches = voteSvc.persist()
        syncPatches(electionId, SyncType.ROOM, patches)

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        return make_error(500, '%s:%s: %s' % (fname, exc_tb.tb_lineno, e))

    return json.dumps({'id': str(id)})

@main.route('/discardBallot', methods=['POST'])
@cross_origin(origin='*')
def discardBallot():
    data = request.json
    electionId = data["election"]
    ballotId = data["ballotId"]
    authorityId = data["authorityId"]

    try:
        # prepare voteService
        voteSvc = VoteService(electionId)

        # perform action
        voteSvc.discardBallot(ballotId, authorityId)

        # retrieve and persist modified state
        patches = voteSvc.persist()
        syncPatches(electionId, SyncType.ROOM, patches)

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        return make_error(500, '%s:%s: %s' % (fname, exc_tb.tb_lineno, e))

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
        # prepare voteService
        voteSvc = VoteService(electionId)

        # perform action
        voteSvc.confirmVote(voterId, ballotId, confirmationCode)

        # retrieve and persist modified state
        patches = voteSvc.persist()
        syncPatches(electionId, SyncType.ROOM, patches)

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        return make_error(500, '%s:%s: %s' % (fname, exc_tb.tb_lineno, e))

    return json.dumps({'id': str(id)})

@main.route('/checkConfirmation', methods=['POST'])
@cross_origin(origin='*')
def checkConfirmation():
    data = request.json
    electionId = data["election"]
    confirmationId = data["confirmationId"]
    authorityId = data["authorityId"]

    try:
        # prepare voteService
        voteSvc = VoteService(electionId)

        # perform action
        voteSvc.checkConfirmation(confirmationId, authorityId)

        # retrieve and persist modified state
        patches = voteSvc.persist()
        syncPatches(electionId, SyncType.ROOM, patches)

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        return make_error(500, '%s:%s: %s' % (fname, exc_tb.tb_lineno, e))

    return json.dumps({'id': str(id)})

@main.route('/finalize', methods=['POST'])
@cross_origin(origin='*')
def finalize():
    data = request.json
    electionId = data["election"]
    confirmationId = data["confirmationId"]
    authorityId = data["authorityId"]

    try:
        # prepare voteService
        voteSvc = VoteService(electionId)

        # perform action
        voteSvc.finalize(confirmationId, authorityId)

        # retrieve and persist modified state
        patches = voteSvc.persist()
        syncPatches(electionId, SyncType.ROOM, patches)

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        return make_error(500, '%s:%s: %s' % (fname, exc_tb.tb_lineno, e))

    return json.dumps({'id': str(id)})

@main.route('/discardConfirmation', methods=['POST'])
@cross_origin(origin='*')
def discardConfirmation():
    data = request.json
    electionId = data["election"]
    confirmationId = data["confirmationId"]
    authorityId = data["authorityId"]

    try:
        # prepare voteService
        voteSvc = VoteService(electionId)

        # perform action
        voteSvc.discardConfirmation(confirmationId, authorityId)

        # retrieve and persist modified state
        patches = voteSvc.persist()
        syncPatches(electionId, SyncType.ROOM, patches)

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        return make_error(500, '%s:%s: %s' % (fname, exc_tb.tb_lineno, e))

    return json.dumps({'id': str(id)})

@main.route('/setAutoMode', methods=['POST'])
@cross_origin(origin='*')
def setAutoMode():
    data = request.json
    electionId = data["election"]
    authorityId = data["authorityId"]
    value = data["value"]

    try:
        # prepare voteService
        voteSvc = VoteService(electionId)

        # perform action
        voteSvc.authorities[authorityId].autoCheck = value

        # retrieve and persist modified state
        patches = voteSvc.persist()
        syncPatches(electionId, SyncType.ROOM, patches)

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        return make_error(500, '%s:%s: %s' % (fname, exc_tb.tb_lineno, e))

    return json.dumps({'id': str(id)})


@main.route('/revealCode', methods=['POST'])
@cross_origin(origin='*')
def revealCode():
    data = request.json
    electionId = data["election"]
    voterId = int(data["voterId"])
    codeIndex = int(data["codeIndex"])

    try:
        # prepare voteService
        voteSvc = VoteService(electionId)

        # perform action
        voteSvc.revealCode(voterId, codeIndex)

        # retrieve and persist modified state
        patches = voteSvc.persist()
        syncPatches(electionId, SyncType.ROOM, patches)

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        return make_error(500, '%s:%s: %s' % (fname, exc_tb.tb_lineno, e))

    return json.dumps({'id': str(id)})


