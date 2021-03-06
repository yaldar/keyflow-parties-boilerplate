from keyflow.models.factories.guest_account_factory import GuestAccountFactory
from keyflow.models.party import Party
from keyflow.tests.keyflow_parties_test_base import KeyflowPartiesTestBase


class TestModelReadWrite(KeyflowPartiesTestBase):
    def test_create_list_on_models(self):
        party_a = Party()
        party_a.title = "New Party"
        party_a.owner_ga = GuestAccountFactory().get_instance()
        party_a.save()

        self.assertEqual(Party.objects.count(), 1)
