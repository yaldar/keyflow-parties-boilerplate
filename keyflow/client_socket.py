import logging

import socketio

from keyflow.models.guest_account import GuestAccount
from keyflow.models.party import Party


class ClientSocket(socketio.Client):

  def __init__(self, party: Party, ga: GuestAccount, url='http://localhost:5000/', **kwargs):
    super().__init__(**kwargs)
    self.url = url
    self.party = party
    self.ga = ga
    self.sio = socketio.Client()

    @self.sio.event
    def chat_message(data):
      print("message received: ", data)

    @self.sio.event
    def connect():
      while not self.sio.connected:
        self.sio.wait()
      if self.sio.connected:
        self.sio.emit('user_join', data={"party": self.party.id})
    self.sio.connect(url=url)

  def send_message_from_client(self, message, from_ga, room):
    data = {
      "message": message,
      "from_ga": from_ga,
      "room": room
    }

    self.sio.emit('broadcast_to_room', data=data)
