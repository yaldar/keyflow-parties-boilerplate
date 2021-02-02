from keyflow.client_socket import socket_maker, ClientSocket
from keyflow.models.factories.guest_account_factory import GuestAccountFactory
from keyflow.models.factories.party_factory import PartyFactory
from keyflow.models.guest_account import GuestAccount
from keyflow.models.party import Party


p2 = Party()
p1 = Party()

u = GuestAccount()
u2 = GuestAccount()

p1.id=1
p2.id=2

s1 = ClientSocket(u, p1)
s2 = ClientSocket(u2, p2)
