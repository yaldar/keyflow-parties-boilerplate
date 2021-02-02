import http

from keyflow.models.guest_account import GuestAccount
from keyflow.models.party import Party
from keyflow.models.party_requests import PartyRequest


def is_attending(party: Party, from_ga: GuestAccount, write_error):
  requests_from_ga = PartyRequest.objects.raw({"from_ga": from_ga.id})
  requests_from_ga_to_party = requests_from_ga.raw({"party": party.id})
  count = requests_from_ga_to_party.count()
  try:
    if count < 1:
      raise Exception('Guest account has not requested access to this party')
    elif count > 1:
      # @TODO send this error to support. Database should not contain duplicate requests
      raise Exception('Duplicate requests detected')
    else:
      return requests_from_ga_to_party.first().status == "a"
  except Exception as e:
    write_error(http.HTTPStatus.UNAUTHORIZED, detail=str(e))
