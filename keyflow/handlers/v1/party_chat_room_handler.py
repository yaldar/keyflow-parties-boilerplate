import http
import json

from tornado import gen

from keyflow.models.party import Party
from keyflow.services.parties_service_v1 import PartiesServiceV1
from keyflow.services.party_chat_room_service_v1 import PartyChatRoomServiceV1
from keyflow.utils.keyflow_parties_app_handler_base import KeyflowPartiesAppHandlerBase


class PartyChatRoomHandler(KeyflowPartiesAppHandlerBase):
    """
    You can post a message to the chat room here. Will be provided later to
    the party websocket for listeneres to listen to. POST Body should be {
    "message": "Message"
    }
    """

    def post_worker(self, party: Party = None, message="", *args, **kwargs):
        party_chat_service_v1 = PartyChatRoomServiceV1(party=party)
        party_chat_service_v1.add_message_to_chat_room(
            from_ga=self.get_current_user(), message=message
        )
        return http.HTTPStatus.OK, None

    @gen.coroutine
    def post(self, party_id=None):
        try:
            party = Party.get(party_id=party_id)
            if not party:
                raise Exception("Party not found")

            # TODO: Check if the POSTer has right to create messages on this
            #  party.
            message = json.loads(self.request.body)["message"]
            success, result_data = yield self.application.threadPool.submit(
                self.post_worker, party=party
            )
            self.write_success(output=result_data)
            self.finish()
        except Exception as e:
            self.write_error(http.HTTPStatus.BAD_REQUEST, detail=str(e))
