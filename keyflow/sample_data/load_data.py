import logging
from datetime import datetime

from tornado.options import options

from keyflow.main import setup_defines
from keyflow.models.factories.guest_account_factory import GuestAccountFactory
from keyflow.models.factories.party_factory import PartyFactory
from keyflow.models.guest_account import GuestAccount
from keyflow.models.party import Party
from keyflow.models.party_requests import PartyRequest
from keyflow.models.pymodm_model import BasePyModelModel


def create_sample_guest_accounts():
    guest_accounts_created = []
    for i in range(10):
        first_name = f"User_{i}"
        last_name = f"Last Name_{i}"
        email = f"guest-account-{i}@keyflow.se"
        guest_account = GuestAccountFactory(
            first_name=first_name, last_name=last_name, email=email
        )
        guest_accounts_created.append(guest_account.get_instance())

    return guest_accounts_created


def create_sample_party(party_owner: GuestAccount):
    party = PartyFactory(owner_ga=party_owner)
    return party.get_instance()


def add_confirmed_guests_to_a_party(guest_accounts, number_of_guests,
                                    party: Party):
    for i in range(number_of_guests):
        guest_account = guest_accounts[i]
        party_request = PartyRequest(
            party=party, from_ga=guest_account,
            status=PartyRequest.STATUS_ACCEPTED,
            accepted_ts=datetime.now(),
        )
        party_request.save()
        logging.info(f"Accepted guest, {guest_account.first_name} to Party: "
                     f"{party.title}")
    return True

def main():
    """
    Create 10 guest accounts. Create 1 party. 8 others are confirmed guests
    to the party.
    """
    guest_accounts = create_sample_guest_accounts()
    party = create_sample_party(guest_accounts[0])
    add_confirmed_guests_to_a_party(guest_accounts=guest_accounts[1:],
                                    number_of_guests=8, party=party)


if __name__ == "__main__":
    setup_defines()
    options.mongodb_hosts = "127.0.0.1:27017"
    BasePyModelModel.initialize(
        database_name="keyflow_parties",
        host=options.mongodb_hosts,
        use_authentication=False,
        use_ssl=False,
    )
    main()
