#!/bin/env python
import os

from app import create_app, socketio
from flask import jsonify

app = create_app(debug=True)

if __name__ == '__main__':
    socketio.run(app, host=os.environ['SOCKETIO_HOST'] if 'SOCKETIO_HOST' in os.environ else '127.0.0.1',
        port=int(os.environ['SOCKETIO_PORT']) if 'SOCKETIO_PORT' in os.environ else 5000)



