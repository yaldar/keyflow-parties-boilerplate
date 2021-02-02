import logging

import socketio

from keyflow.models.party import Party

class ClientSocket:

  def __init__(self, ga, party: Party, url='http://localhost:5000/'):
    self.ga = ga
    self.party = party
    self.sio = socketio.Client()
    @self.sio.event
    def chat_message(sid, data):
      logging.info("message received: ", data)
    @self.sio.event
    def request_data():
      while not self.sio.connected:
        self.sio.wait()
      if self.sio.connected:
        self.sio.emit('user_join', data={"party": self.party.id})
    self.sio.connect(url='http://localhost:5000/')
