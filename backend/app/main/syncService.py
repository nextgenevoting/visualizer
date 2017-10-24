from flask import session, redirect, url_for, render_template, request
from . import main
from flask_socketio import emit
from bson.objectid import ObjectId
from bson.json_util import dumps
from app.database import db, saveComplex, loadComplex
from app.models.bulletinBoardState import BulletinBoardState
from .. import socketio
import json
from enum import Enum
from chvote.Utils.JsonParser import mpzconverter

class SyncType(Enum):
   SENDER_ONLY = 1
   ROOM = 2
   BROADCAST = 3

def emitToClient(messageName, payload, syncType, room = None):
    if syncType == SyncType.ROOM:
        socketio.emit(messageName, payload , room=room)
    else:
        socketio.emit(messageName, payload, broadcast=True if syncType == SyncType.BROADCAST else False)

# EMITTERS
def syncElections(syncType):
    assert syncType != SyncType.ROOM, "SyncType of syncElections must be SENDER_ONLY or BROADCAST"
    res = db.elections.find()
    elections = dumps(res)
    emitToClient('syncElections', elections, syncType)

def fullSync(electionID, syncType):
    syncElectionStatus(electionID, syncType)
    syncBulletinBoard(electionID, syncType)
    syncPrintingAuthority(electionID, syncType)

def syncBulletinBoard(electionID, syncType):
    bbState = db.bulletinBoardStates.find_one({'election':electionID})
    if bbState != None:
        bbState = loadComplex(bbState["state"])
        emitToClient('syncElectionData', bbState.toJSON(), syncType, electionID)
    else:
        raise RuntimeError("No BulletinBoardState for election {}!".format(electionID))


def syncPrintingAuthority(electionID, syncType):
    paState = db.printingAuthorityStates.find_one({'election':electionID})
    if paState != None:
        paState = loadComplex(paState["state"])
        emitToClient('syncPrintingAuthority', paState.toJSON(), syncType, electionID)
    else:
        raise RuntimeError("No PrintingAuthorityState for this election {}!".format(electionID))

def syncVoters(electionID, syncType):
    voters = []
    try:
        for voterState in db.voterStates.find({'election':electionID}):
            state = loadComplex(voterState["state"])
            voters.append(state)
        emitToClient('syncVoters', json.dumps(voters, default=mpzconverter), syncType, electionID)
    except Exception as ex:
        raise RuntimeError("No PrintingAuthorityState for this election {}!".format(electionID))


def syncElectionStatus(electionID, syncType):
    election = db.elections.find_one({'_id': ObjectId(electionID)})
    if election != None:
        emitToClient('syncElection', {'electionID':electionID, 'status': election["status"]}, syncType, electionID)
    else:
        raise RuntimeError("No Election entry for this election {}!".format(electionID))