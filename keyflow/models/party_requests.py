from pymodm import fields

from keyflow.models.guest_account import GuestAccount
from keyflow.models.party import Party
from keyflow.models.pymodm_model import BasePyModelModel


class PartyRequest(BasePyModelModel):
    _COLLECTION_NAME = "party_requests"

    class Meta:
        final = True
        collection_name = "party_requests"

    STATUS_PENDING = "p"
    STATUS_DECLINED = "d"
    STATUS_ACCEPTED = "a"
    STATUS_CANCELLED = "c"

    PARTY_STATUSES = (
        STATUS_PENDING,
        STATUS_DECLINED,
        STATUS_CANCELLED,
        STATUS_ACCEPTED,
    )

    id = fields.BigIntegerField(primary_key=True)
    from_ga = fields.ReferenceField(GuestAccount, required=True)
    party = fields.ReferenceField(Party, required=True)
    status = fields.CharField(
        choices=PARTY_STATUSES, required=True, default=STATUS_PENDING
    )
    accepted_ts = fields.DateTimeField(blank=True)
