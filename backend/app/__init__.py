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

    from .api import main as main_blueprint
    app.register_blueprint(main_blueprint)

    socketio.init_app(app)
    return app


@socketio.on('connect')
def handle_connection():
    from app.api.preElectionService import syncElections
    from app.api.syncService import SyncType

    syncElections(SyncType.SENDER_ONLY)

# on_join is called whenever a client selects an election. Election specific messages will only be sent to clients that have joined the room
@socketio.on('join')
def on_join(data):
    from app.api.syncService import SyncType, fullSync

    electionID = data['election']
    for room in rooms():
        if room != request.sid:
            leave_room(room)
    join_room(electionID)

    from app.api.syncService import emitToClient, SyncType

    fullSync(electionID, SyncType.SENDER_ONLY)

    emitToClient('joinAck', electionID, SyncType.SENDER_ONLY)
