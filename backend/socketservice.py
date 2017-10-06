# By importing eventlet, flask will automatically use it instead of Werkzeug.
import eventlet

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from datetime import datetime

app = Flask(__name__)
socketio = SocketIO(app, engineio_logger=True)

global counter

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

if __name__ == '__main__':
    global counter
    counter = 0
    socketio.run(app)
