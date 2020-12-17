from keyflow.models.guest_account import GuestAccount


class GuestAccountFactory:
    object = None

    def get_instance(self):
        return self.object

    def __init__(
        self, first_name="First", last_name="last_name", email="tester@keyflow.se"
    ):
        guest_account = GuestAccount(
            first_name=first_name, last_name=last_name, email=email
        )
        guest_account.save()
        self.object = guest_account
