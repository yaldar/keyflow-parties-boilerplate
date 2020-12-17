import typing

from keyflow.models.party import Party
from keyflow.services.schemas.party_schema_v1 import PartySchemaV1


class PartiesServiceV1(object):
    def get_parties(self):
        return Party.objects

    def serialize_parties(self, parties):
        return_dict = {"parties": []}
        party_serializer = PartySchemaV1()
        return_dict["parties"] = party_serializer.dump(parties, many=True)
        return return_dict
