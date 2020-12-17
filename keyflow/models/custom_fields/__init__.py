from datetime import datetime

from pymodm import DateTimeField


class DefaultDateTimeField(DateTimeField):
    def get_default(self):
        return datetime.datetime.utcnow()
