import logging
import typing

from keyflow.models.guest_account import GuestAccount
from keyflow.models.party_chat_message import PartyChatMessage
from keyflow.schemas.party_chat_schema_v1 import PartyChatSchemaV1


class PartyChatRoomServiceV1(object):
    party = None

    def __init__(self, party=None):
        self.party = party

    def add_message_to_chat_room(
        self,
        from_ga: GuestAccount = None,
        message: typing.Dict[typing.Any, typing.Any] = None,
    ):
        party_chat = PartyChatMessage(
            party=self.party,
            from_ga=from_ga,
            message=message.get("message", None),
            parent_chat_message=message.get("parent_chat_message", None),
        )
        party_chat.save()

        self.relay_message_to_consumers(party_chat=party_chat)
        return party_chat

    def get_messages_serialized(self):
        return_response = {"chats": []}
        party_chats = PartyChatMessage.objects.raw({"party": self.party.id})
        if not party_chats.count():
            return return_response

        return_response["chats"] = PartyChatSchemaV1().dump(party_chats, many=True)
        return return_response

    def relay_message_to_consumers(self, party_chat: PartyChatMessage):
        """
        Fill this function. This is where you should relay the message to
        your websocket. You can probably create a separate ID for the chat
        room or use the party ID itself as you only have one party chat room per party.
        """
        import socketio

        sio = socketio.Client()
        data = {"message": party_chat.message, "from": party_chat.from_ga.id, "room": party_chat.party.id}
        @sio.event
        def connect():
          logging.info("broadcasting to room", data)
          sio.emit("broadcast_to_room", data)
          sio.disconnect()

        sio.connect('http://localhost:5000/')

        pass
