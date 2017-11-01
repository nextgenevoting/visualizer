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