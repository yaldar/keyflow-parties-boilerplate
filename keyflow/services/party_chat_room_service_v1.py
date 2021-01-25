from keyflow.models.guest_account import GuestAccount
from keyflow.models.party_chat import PartyChat


class PartyChatRoomServiceV1(object):
    party = None

    def __init__(self, party=None):
        self.party = party

    def add_message_to_chat_room(self, from_ga: GuestAccount = None, message=""):
        party_chat = PartyChat(party=self.party, from_ga=from_ga, message=message)
        party_chat.save()

        return party_chat
