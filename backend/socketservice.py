import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, send, rooms
from datetime import datetime
from demonstrator.backend.database import db
from flask_socketio import join_room, leave_room

app = Flask(__name__)
socketio = SocketIO(app, engineio_logger=True)

@socketio.on('connect')
def handle_connection():
    from demonstrator.backend.electionAdministration import syncElections
    syncElections(False)

# on_join is called whenever a client selects an election. Election specific messages will only be sent to clients that have joined the room
@socketio.on('join')
def on_join(data):
    global rooms
    from demonstrator.backend.electionAdministration import syncElectionData
    for room in rooms():
        if room != request.sid:
            leave_room(room)
    join_room(data['election'])
    syncElectionData(data['election'], data['election'])
    #emit('getupdate', {'data': {'counter' : counter}}, broadcast=False)

@socketio.on('createElection')
def createElection(data):
    from demonstrator.backend.electionAdministration import createElection
    createElection(data)

@socketio.on('increment')
def increment(data):
    print("Data in increment:")
    print(data["election"])
    electionData = db.electorateData.find_one({'election':data["election"]})
    replaceElectionData = electionData.copy()
    replaceElectionData["counter"] = replaceElectionData["counter"] + 1
    db.electorateData.replace_one(electionData, replaceElectionData)
    from demonstrator.backend.electionAdministration import syncElectionData
    syncElectionData(data['election'], data['election'])


if __name__ == '__main__':
    print("run")

    socketio.run(app)
