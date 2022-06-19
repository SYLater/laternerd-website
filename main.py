from flask import Flask, render_template
from flask_socketio import SocketIO

from website import create_app, socketio

app = create_app()


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')
