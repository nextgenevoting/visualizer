from flask import session, redirect, url_for, render_template, request
from . import main
from flask_socketio import emit
from bson.objectid import ObjectId
from bson.json_util import dumps
from app.database import db, saveComplex, loadComplex
from app.models.bulletinBoardState import BulletinBoardState
from .. import socketio
import json

# EMITTERS
def syncElections(broadcast):
    res = db.elections.find()
    elections = dumps(res)
    socketio.emit('syncElections',elections , broadcast=broadcast)

def syncElectionData(electionID):
    election = db.elections.find_one({'_id': ObjectId(electionID)})

    bbState = db.bulletinBoardStates.find_one({'election':electionID})
    if bbState != None:
        bbState = loadComplex(bbState["state"])
        socketio.emit('syncElectionData', {'election':electionID, 'status': election["status"], 'bulletinBoard': bbState.toJSON()}, room=electionID)
    else:
        raise RuntimeError("No BulletinBoardState for this election!")
