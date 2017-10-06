# By importing eventlet, flask will automatically use it instead of Werkzeug.

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from datetime import datetime

app = Flask(__name__)
socketio = SocketIO(app, engineio_logger=True)

global counter
global elections

@socketio.on('increment')
def increment():
    global counter
    counter += 1
    print(counter)
    emit('getupdate', {'data': {'message': 'Hello from websocket', 'counter' : counter}}, broadcast=True)
    emit('usermessage', 'Hello from server {}'.format(datetime.now().strftime('%H:%M:%S')), broadcast=True)

@socketio.on('connect')
def handle_connection():
    print("connected!")
    emit('getupdate', {'data': {'message': 'Hello from websocket', 'counter' : counter}}, broadcast=True)
    sendElections()


def sendElections():
    global elections
    emit('getelections', elections, broadcast=True)

@socketio.on('createElection')
def createElection(electionTitle):
    global elections
    print(electionTitle)
    sendElections()

if __name__ == '__main__':
    global counter
    global elections
    counter = 0
    elections = {'elections': [{'id': 1, 'title': 'Testelection 1'}, {'id': 2, 'title': 'Testelection 2'}]}
    socketio.run(app)
