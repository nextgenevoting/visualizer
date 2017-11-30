import json
from enum import Enum
from flask import Flask, request

import pymongo
from app.database import db, deserializeState
from app.utils.JsonParser import mpzconverter
from bson.json_util import dumps
from bson.objectid import ObjectId

from .. import socketio


class SyncType(Enum):
   SENDER_ONLY = 1
   ROOM = 2
   BROADCAST = 3

def emitToClient(messageName, payload, syncType, room = None):
    if syncType == SyncType.ROOM:
        socketio.emit(messageName, payload , room=room)
    elif syncType == SyncType.BROADCAST:
        socketio.emit(messageName, payload, broadcast=True)
    else:
        socketio.emit(messageName, payload, room=request.sid)

# EMITTERS
def syncElections(syncType):
    assert syncType != SyncType.ROOM, "SyncType of syncElections must be SENDER_ONLY or BROADCAST"
    res = db.elections.find()
    elections = dumps(res)
    emitToClient('syncElections', elections, syncType)

def syncPatches(electionID, syncType, patches):
    emitToClient('patchState', json.dumps(patches, default=mpzconverter), syncType, electionID)

def fullSync(electionID, syncType):
    syncBulletinBoard(electionID, syncType)
    syncPrintingAuthority(electionID, syncType)
    syncVoters(electionID, syncType)
    syncElectionAuthorities(electionID, syncType)
    syncElectionAdministrator(electionID, syncType)
    syncElectionStatus(electionID, syncType)

def syncElectionStatus(electionID, syncType):
    election = db.elections.find_one({'_id': ObjectId(electionID)})
    if election != None:
        emitToClient('syncElection', {'electionID':electionID, 'status': election["status"]}, syncType, electionID)
    else:
        raise RuntimeError("No Election entry for election {}!".format(electionID))

# ************************
# VoteService State Syncs
# ************************

def syncBulletinBoard(electionID, syncType):
    bbState = db.bulletinBoardStates.find_one({'election':electionID})
    if bbState != None:
        bbState = deserializeState(bbState["state"])
        emitToClient('syncElectionData', bbState.toJSON(), syncType, electionID)
    else:
        raise RuntimeError("No BulletinBoardState for election {}!".format(electionID))


def syncPrintingAuthority(electionID, syncType):
    paState = db.printingAuthorityStates.find_one({'election':electionID})
    if paState != None:
        paState = deserializeState(paState["state"])
        emitToClient('syncPrintingAuthority', paState.toJSON(), syncType, electionID)
    else:
        raise RuntimeError("No PrintingAuthorityState for election {}!".format(electionID))


def syncElectionAdministrator(electionID, syncType):
    eaState = db.electionAdministratorStates.find_one({'election':electionID})
    if eaState != None:
        eaState = deserializeState(eaState["state"])
        emitToClient('syncElectionAdministrator', eaState.toJSON(), syncType, electionID)
    else:
        raise RuntimeError("No ElectionAdministrator.py for election {}!".format(electionID))

def syncVoters(electionID, syncType):
    voters = []
    try:
        for voterState in db.voterStates.find({'election':electionID}).sort([("voterID", pymongo.ASCENDING)]):
            state = deserializeState(voterState["state"])
            voters.append(state)
        emitToClient('syncVoters', json.dumps(voters, default=mpzconverter), syncType, electionID)
    except Exception as ex:
        raise RuntimeError("No VoterStates for election {}!".format(electionID))

def syncElectionAuthorities(electionID, syncType):
    electionAuthorities = []
    try:
        for authorityState in db.electionAuthorityStates.find({'election':electionID}).sort([("authorityID", pymongo.ASCENDING)]):
            state = deserializeState(authorityState["state"])
            electionAuthorities.append(state)
        emitToClient('syncElectionAuthorities', json.dumps(electionAuthorities, default=mpzconverter), syncType, electionID)
    except Exception as ex:
        raise RuntimeError("No ElectionAuthorityStates for election {}!".format(electionID))
