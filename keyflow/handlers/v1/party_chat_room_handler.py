import http
import json

from marshmallow import EXCLUDE, ValidationError
from tornado import gen

from keyflow.models.party import Party
from keyflow.schemas.party_chat_schema_v1 import PartyChatSchemaV1
from keyflow.services.party_chat_room_service_v1 import PartyChatRoomServiceV1
from keyflow.utils import decorators
from keyflow.utils.keyflow_parties_app_handler_base import KeyflowPartiesAppHandlerBase


class PartyChatRoomHandler(KeyflowPartiesAppHandlerBase):
    """
    You can post a message to the chat room here. Will be provided later to
    the party websocket for listeneres to listen to. POST Body should be {
    "message": "Message"
    }
    """

    def post_worker(self, party: Party = None, post_body="", *args, **kwargs):
        party_chat_service_v1 = PartyChatRoomServiceV1(party=party)
        party_chat_message_schema = PartyChatSchemaV1()
        try:
            party_chat_message = party_chat_message_schema.load(
                post_body, unknown=EXCLUDE
            )
        except ValidationError as ex:
            return False, str(ex)
        party_chat_service_v1.add_message_to_chat_room(
            from_ga=self.get_current_user(), message=party_chat_message
        )
        party_chat_messages_serialized = party_chat_service_v1.get_messages_serialized()
        return http.HTTPStatus.OK, party_chat_messages_serialized

    @gen.coroutine
    @decorators.authenticated
    def post(self, party_id=None, *args, **kwargs):
        try:
            party = Party.objects.get({"_id": int(party_id)})
            if not party:
                raise Exception("Party not found")

            # TODO: Check if the POSTer has right to create messages on this
            #  party.
            post_body = json.loads(self.request.body)
            success, result_data = yield self.application.threadPool.submit(
                self.post_worker, party=party, post_body=post_body
            )
            self.write_success(output=result_data)
            self.finish()
        except Exception as e:
            self.write_error(http.HTTPStatus.BAD_REQUEST, detail=str(e))
