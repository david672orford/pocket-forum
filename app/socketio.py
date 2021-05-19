from flask_socketio import SocketIO, send, emit
from . import app
from .components.users import current_user

socketio = SocketIO(app, logger=True, engineio_logger=True)

@socketio.on('connect')
def handle_connect():
	print('connect')
	send("User %s has just connected!" % current_user.handle, broadcast=True, include_self=False)

@socketio.on('disconnect')
def handle_disconnect():
	print('disconnect')
	send("User %s has just disconnected!" % current_user.handle, broadcast=True, include_self=False)

@socketio.on('message')
def handle_message(message):
	print('message ', message)
	send("%s: %s" % (current_user.handle, message.strip()), broadcast=True)

