from tornado.web import url

from keyflow.handlers.v1.parties_list_handler import PartiesListHandler
from keyflow.handlers.v1.party_chat_room_handler import PartyChatRoomHandler

urls = [
    url(
        r"/v1/parties/(?P<party_id>[0-9]+)/chats/",
        PartyChatRoomHandler,
        name="party_chats",
    ),
    url(r"/v1/parties/", PartiesListHandler, name="list_parties"),
]
