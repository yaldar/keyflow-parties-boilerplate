from keyflow.client_socket import ClientSocket
from keyflow.models.factories.party_factory import PartyFactory
from keyflow.models.guest_account import GuestAccount
from keyflow.models.party import Party

party = Party()
ga = GuestAccount()

party.id = 2
ga.id = 15

soc = ClientSocket(party=party, ga=ga)
soc.connect('http://localhost:5000/')
