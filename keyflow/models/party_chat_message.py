from pymodm import fields

from keyflow.models.guest_account import GuestAccount
from keyflow.models.party import Party
from keyflow.models.pymodm_model import BasePyModelModel


class PartyChatMessage(BasePyModelModel):
    _COLLECTION_NAME = "party_chat_messages"

    class Meta:
        final = True
        collection_name = "party_chat_messages"

    id = fields.BigIntegerField(primary_key=True)
    from_ga = fields.ReferenceField(GuestAccount, required=True)
    party = fields.ReferenceField(Party, required=True)
    message = fields.CharField(blank=True)
    # This could be used when you have to introduce reply to message and so ?
    parent_chat_message = fields.ReferenceField(
        "PartyChatMessage", required=False, blank=True
    )
