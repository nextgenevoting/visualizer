from flask import Flask, request
from flask_socketio import SocketIO, leave_room, join_room, rooms
from flask_cors import CORS, cross_origin

socketio = SocketIO(engineio_logger=True)

def create_app(debug=False):
    app = Flask(__name__)
    cors = CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.debug = debug
    app.config['SECRET_KEY'] = 'gjr39dkjn344_!67#'

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    socketio.init_app(app)
    return app

@socketio.on('connect')
def handle_connection():
    from app.main.preElectionService import syncElections
    syncElections(False)

# on_join is called whenever a client selects an election. Election specific messages will only be sent to clients that have joined the room
@socketio.on('join')
def on_join(data):
    electionID = data['election']
    for room in rooms():
        if room != request.sid:
            leave_room(room)
    join_room(electionID)
    from app.main.preElectionService import syncElectionData
    from app.main.incrementService import syncCounter
    syncElectionData(electionID)
    syncCounter(electionID)