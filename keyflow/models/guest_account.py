from pymodm import fields

from keyflow.models.pymodm_model import BasePyModelModel


class GuestAccount(BasePyModelModel):
    _COLLECTION_NAME = "guest_accounts"

    class Meta:
        final = True
        collection_name = "guest_accounts"

    id = fields.BigIntegerField(primary_key=True)
    first_name = fields.CharField(required=True)
    last_name = fields.CharField(required=True)
    email = fields.EmailField(required=True)
    # ... add other fields here
