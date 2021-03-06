"""
Created on Feb 2, 2014

@author: parallels
"""

import tornado

from keyflow.models.guest_account import GuestAccount
from keyflow.utils.keyflow_request_mixin import KeyflowRequestMixin
from keyflow.utils.loggin_request_handler import LoggingRequestHandler


class KeyflowPartiesAppHandlerBase(KeyflowRequestMixin, LoggingRequestHandler):
    """
    The purpose of this base handler is to provide the get_current_user method
    which is mandatory when we use the @tornado.web.authenticated decorator.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.response = dict()

    def get_current_user(self) -> GuestAccount:
        # Fake authentication for fancy sake.
        guest_account_id = self.request.headers.get("Authorization")
        if not guest_account_id:
            return None
        try:
            guest_account = GuestAccount.objects.get({"_id": int(guest_account_id)})
        except GuestAccount.DoesNotExist:
            return None
        return guest_account

    def get_user_locale(self):
        """
        Tornado will call this method to determine whether the user has some
        specific language preference. We will try to determine it from an
        optional cookie that can be sent  from the client. If this method
        returns None, Tornado will fallback
        to get_browser_locale() which is determined by the Accept-Language
        header
        """
        language_code = self.get_cookie("AcceptLanguage", None)
        if language_code:
            return tornado.locale.get(language_code)

        # If the user has a saved setting - go for that.
        if self.current_user:
            return tornado.locale.get("en-US")

        return None

    def set_default_headers(self):
        super().set_default_headers()
        # We need this not to mix languages in the reponse when Nginx caches pages.
        self.add_header("Vary", "Accept-Language")
