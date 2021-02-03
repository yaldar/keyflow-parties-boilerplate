import logging

import eventlet
import socketio

sio = socketio.Server(cors_allowed_origins="*")
app = socketio.WSGIApp(sio)


@sio.event
def connect(sid, environ):
  logging.info('connect ', sid)


@sio.event
def message(sid, data):
  logging.info('message ', data)

@sio.event
def disconnect(sid):
  logging.info('disconnect ', sid)

@sio.event
def user_join(sid, data):
  print(f"user with id: {sid} has joined the room for the party: {data['party']}")
  sio.enter_room(sid, room=data["party"])


@sio.event
def broadcast_to_room(sid, data):
  sio.emit("chat_message", data={"message": data["message"], "from_ga": data["from_ga"]}, room=data["room"], skip_sid=sid)
  print("broadcasting message from server to room", data)


if __name__ == '__main__':
  eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
