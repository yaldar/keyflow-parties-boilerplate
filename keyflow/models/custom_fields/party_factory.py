from datetime import datetime, timedelta

from keyflow.models.party import Party


class PartyFactory:
    object = None

    def get_instance(self):
        return self.object

    def __init__(
        self,
        title="New Party",
        address="Epicenter, Stockholm",
        start_time=None,
        end_time=None,
    ):
        if not start_time:
            start_time = datetime.utcnow()

        if not end_time:
            end_time = start_time + timedelta(hours=5)
        party = Party(
            title=title, address=address, start_time=start_time, end_time=end_time
        )
        party.save()
        self.object = party
