import json

from keyflow.models.factories.guest_account_factory import GuestAccountFactory
from keyflow.models.factories.party_factory import PartyFactory
from keyflow.tests.keyflow_parties_test_base import KeyflowPartiesTestBase


class TestAPIReadOperations(KeyflowPartiesTestBase):
    """
    Will show you how to read write on teh API, use a factory method for
    creating parties later.
    """

    def test_read_op_over_api(self):
        party_owner = GuestAccountFactory().get_instance()
        party_a = PartyFactory(title="Party A", owner_ga=party_owner).get_instance()
        party_b = PartyFactory(title="Party B", owner_ga=party_owner).get_instance()
        party_c = PartyFactory(title="Party C", owner_ga=party_owner).get_instance()

        parties_response_raw = self.fetch(
            path=self.get_app().reverse_url("list_parties"), method="GET"
        )
        parties_response = json.loads(parties_response_raw.body)
        self.assertEqual(len(parties_response["data"]["parties"]), 3)
