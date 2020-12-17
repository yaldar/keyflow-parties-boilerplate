"""
Created on Feb 2, 2014

@author: parallels
"""

import tornado

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
            return tornado.locale.get(self.current_user.language_selected)

        return None

    def set_default_headers(self):
        super().set_default_headers()
        # We need this not to mix languages in the reponse when Nginx caches pages.
        self.add_header("Vary", "Accept-Language")
