# By importing eventlet, flask will automatically use it instead of Werkzeug.

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from datetime import datetime
import pymongo
import json
from bson.json_util import dumps

app = Flask(__name__)
socketio = SocketIO(app, engineio_logger=True)

global counter
global db

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
    global db
    res = db.elections.find()
    elections = dumps(res)

    emit('getelections',elections , broadcast=True)

@socketio.on('createElection')
def createElection(dataJson):
    global db

    # todo: Id dynamisch generieren
    db.elections.insert({'id':4, 'title': dataJson["title"]})
    sendElections()

if __name__ == '__main__':
    global counter
    global db
    counter = 0

    client = pymongo.MongoClient('localhost', 27017)
    db = client.chvote
    elections = db.elections
    #elections.insert({'id': 1, 'title': 'Testelection 1'})
    #elections.insert({'id': 2, 'title': 'Testelection 2'})
    #elections.insert({'id': 3, 'title': 'Testelection 3'})

    socketio.run(app)
