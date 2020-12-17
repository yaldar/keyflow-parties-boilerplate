from typing import Set, Any

from keyflow.models.party import Party
from keyflow.schemas.party_schema_v1 import PartySchemaV1


class PartiesServiceV1(object):
    def get_parties(self):
        return Party.objects

    def serialize_parties(self, parties):
        return_dict = {"parties": [], "guestAccounts": []}
        party_serializer = PartySchemaV1()
        owner_ga_ids_set: Set[int] = set()
        for party in parties:
            owner_ga_ids_set.add(party.owner_ga.id)

        # @TODO: Query the GuestAccount model for owner_ga_ids_set and then
        #  send it in the response after serializing it.
        return_dict["parties"] = party_serializer.dump(parties, many=True)
        return return_dict
