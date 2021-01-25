from pymodm import fields

from keyflow.models.guest_account import GuestAccount
from keyflow.models.party import Party
from keyflow.models.pymodm_model import BasePyModelModel


class PartyChat(BasePyModelModel):
    _COLLECTION_NAME = "party_chats"

    class Meta:
        final = True
        collection_name = "party_chats"

    from_ga = fields.ReferenceField(GuestAccount, required=True)
    party = fields.ReferenceField(Party, required=True)
    message = fields.CharField(blank=True)
