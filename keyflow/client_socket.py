import logging

import socketio

from keyflow.models.guest_account import GuestAccount
from keyflow.models.party import Party


class ClientSocket:

  def __init__(self, ga: GuestAccount, party: Party, url='http://localhost:5000/'):
    self.ga = ga
    self.party = party
    self.sio = socketio.Client()

    @self.sio.event
    def chat_message(sid, data):
      logging.info("message received: ", data)

    @self.sio.event
    def connect(sid):
      while not self.sio.connected:
        self.sio.wait()
      if self.sio.connected:
        self.sio.emit('user_join', data={"party": self.party.id})

    self.sio.connect(url='http://localhost:5000/')
