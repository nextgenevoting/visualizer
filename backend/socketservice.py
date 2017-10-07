import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from datetime import datetime
from demonstrator.backend.database import db

app = Flask(__name__)
socketio = SocketIO(app, engineio_logger=True)

global counter

@socketio.on('increment')
def increment():
    global counter
    counter += 1
    print(counter)
    emit('getupdate', {'data': {'message': 'Hello from websocket', 'counter' : counter}}, broadcast=True)

@socketio.on('connect')
def handle_connection():
    from demonstrator.backend.electionAdministration import syncElections
    emit('getupdate', {'data': {'message': 'Hello from websocket', 'counter' : counter}}, broadcast=True)
    syncElections()

@socketio.on('createElection')
def createElection(data):
    from demonstrator.backend.electionAdministration import createElection
    createElection(data)

if __name__ == '__main__':
    global counter
    counter = 0
    print("run")

    socketio.run(app)
