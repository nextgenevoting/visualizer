from flask import session, redirect, url_for, render_template, request
from . import main
from .. import socketio
from app.voteSimulator import VoteSimulator
from flask.ext.cors import CORS, cross_origin
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
        # prepare voteSimulator
        sim = VoteSimulator(electionId)

        # perform action
        sim.startMixing()

        # retrieve and persist modified state
        patches = sim.persist()
        syncPatches(electionId, SyncType.ROOM, patches)

        sim.updateStatus(4)
    except Exception as ex:
        return make_error(500, str(ex))

    return json.dumps({'id': str(id)})



@main.route('/mix', methods=['POST'])
@cross_origin(origin='*')
def mix():
    data = request.json
    electionId = data["election"]
    authorityId = data["authorityId"]
    try:
        # prepare voteSimulator
        sim = VoteSimulator(electionId)

        # perform action
        sim.mix(authorityId)

        # retrieve and persist modified state
        patches = sim.persist()
        syncPatches(electionId, SyncType.ROOM, patches)
    except Exception as ex:
        return make_error(500, str(ex))

    return json.dumps({'id': str(id)})

@main.route('/startDecryptionPhase', methods=['POST'])
@cross_origin(origin='*')
def startDecryptionPhase():
    data = request.json
    electionId = data["election"]
    try:
        # prepare voteSimulator
        sim = VoteSimulator(electionId)

        sim.updateStatus(5)
    except Exception as ex:
        return make_error(500, str(ex))

    return json.dumps({'id': str(id)})



@main.route('/decrypt', methods=['POST'])
@cross_origin(origin='*')
def decrypt():
    data = request.json
    electionId = data["election"]
    authorityId = data["authorityId"]
    try:
        # prepare voteSimulator
        sim = VoteSimulator(electionId)

        # perform action
        sim.decrypt(authorityId)

        # retrieve and persist modified state
        patches = sim.persist()
        syncPatches(electionId, SyncType.ROOM, patches)
    except Exception as ex:
        return make_error(500, str(ex))

    return json.dumps({'id': str(id)})

@main.route('/tally', methods=['POST'])
@cross_origin(origin='*')
def tally():
    data = request.json
    electionId = data["election"]

    try:
        # prepare voteSimulator
        sim = VoteSimulator(electionId)

        # perform action
        sim.tally()

        # retrieve and persist modified state
        patches = sim.persist()
        syncPatches(electionId, SyncType.ROOM, patches)
    except Exception as ex:
        return make_error(500, str(ex))

    return json.dumps({'id': str(id)})
