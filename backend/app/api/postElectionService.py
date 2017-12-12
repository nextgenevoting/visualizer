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

@main.route('/startMixingPhase', methods=['POST'])
@cross_origin(origin='*')
def startMixingPhase():
    data = request.json
    electionId = data["election"]
    try:
        # prepare voteService
        voteSvc = VoteService(electionId)

        # perform action
        voteSvc.startMixing()

        # retrieve and persist modified state
        patches = voteSvc.persist()
        syncPatches(electionId, SyncType.ROOM, patches)

        voteSvc.updateStatus(4)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        return make_error(500, '%s:%s: %s' % (fname, exc_tb.tb_lineno, e))

    return json.dumps({'id': str(id)})

@main.route('/mix', methods=['POST'])
@cross_origin(origin='*')
def mix():
    data = request.json
    electionId = data["election"]
    authorityId = data["authorityId"]
    try:
        # prepare voteService
        voteSvc = VoteService(electionId)

        # perform action
        voteSvc.mix(authorityId)

        # retrieve and persist modified state
        patches = voteSvc.persist()
        syncPatches(electionId, SyncType.ROOM, patches)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        return make_error(500, '%s:%s: %s' % (fname, exc_tb.tb_lineno, e))

    return json.dumps({'id': str(id)})

@main.route('/startDecryptionPhase', methods=['POST'])
@cross_origin(origin='*')
def startDecryptionPhase():
    data = request.json
    electionId = data["election"]
    try:
        # prepare voteService
        voteSvc = VoteService(electionId)

        voteSvc.startDecryption()

        # retrieve and persist modified state
        patches = voteSvc.persist()
        syncPatches(electionId, SyncType.ROOM, patches)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        return make_error(500, '%s:%s: %s' % (fname, exc_tb.tb_lineno, e))

    return json.dumps({'id': str(id)})

@main.route('/decrypt', methods=['POST'])
@cross_origin(origin='*')
def decrypt():
    data = request.json
    electionId = data["election"]
    authorityId = data["authorityId"]
    try:
        # prepare voteService
        voteSvc = VoteService(electionId)

        # perform action
        voteSvc.decrypt(authorityId)

        # retrieve and persist modified state
        patches = voteSvc.persist()
        syncPatches(electionId, SyncType.ROOM, patches)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        return make_error(500, '%s:%s: %s' % (fname, exc_tb.tb_lineno, e))

    return json.dumps({'id': str(id)})

@main.route('/tally', methods=['POST'])
@cross_origin(origin='*')
def tally():
    data = request.json
    electionId = data["election"]

    try:
        # prepare voteService
        voteSvc = VoteService(electionId)

        # perform action
        voteSvc.tally()

        # retrieve and persist modified state
        patches = voteSvc.persist()
        syncPatches(electionId, SyncType.ROOM, patches)

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        return make_error(500, '%s:%s: %s' % (fname, exc_tb.tb_lineno, e))

    return json.dumps({'id': str(id)})

@main.route('/publishResult', methods=['POST'])
@cross_origin(origin='*')
def publishResult():
    data = request.json
    electionId = data["election"]

    try:
        # prepare voteService
        voteSvc = VoteService(electionId)

        # perform action
        voteSvc.publishResult()

        # retrieve and persist modified state
        patches = voteSvc.persist()
        syncPatches(electionId, SyncType.ROOM, patches)

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        return make_error(500, '%s:%s: %s' % (fname, exc_tb.tb_lineno, e))

    return json.dumps({'id': str(id)})


@main.route('/verifyElection', methods=['POST'])
@cross_origin(origin='*')
def verifyElection():
    data = request.json
    electionId = data["election"]

    try:
        # prepare voteService
        voteSvc = VoteService(electionId)

        # perform action
        voteSvc.verifyElection()

        # retrieve and persist modified state
        patches = voteSvc.persist()
        syncPatches(electionId, SyncType.ROOM, patches)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        return make_error(500, '%s:%s: %s' % (fname, exc_tb.tb_lineno, e))

    return json.dumps({'id': str(id)})
