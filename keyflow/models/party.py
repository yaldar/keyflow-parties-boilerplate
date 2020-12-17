from pymodm import fields

from keyflow.models.pymodm_model import BasePyModelModel


class Party(BasePyModelModel):
    _COLLECTION_NAME = "parties"

    class Meta:
        final = True
        collection_name = "parties"

    id = fields.BigIntegerField(primary_key=True)
    title = fields.CharField(required=True)
    address = fields.CharField(blank=True)
    start_time = fields.DateTimeField(blank=True)
    end_time = fields.DateTimeField(blank=True)

    # ... add other fields here to store people who are confirmed the party
    # using fields.ReferenceField to
