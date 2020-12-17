import http.client
import json
import logging

from tornado import locale
from tornado.web import RequestHandler

from keyflow.utils.safe_decode import safe_decode


class LoggingRequestHandler(RequestHandler):
    """
    The purpose of this request handler is to catch any uncaught exceptions
    in a request. When an exception occurs we ensure it is logged and that
    a tech mail is sent.
    """

    # Fields to hide in the log, replaced with __HIDDEN__
    HIDDEN_FIELDS = ["password", "newPassword", "userPassword"]

    def get_browser_locale(self, default="en_US"):
        """Determines the user's locale from ``Accept-Language`` header.
        See http://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html#sec14.4

        This code is copied from web.py in Tornado. Regardless of what the link above says, Tornado
        does not parse the Accept-Language string properly. zh-hans-SE for instance is ditched. So, we're creating
        our own flavour here where. Not the coolest thing, but necessary in this case I think.
        """
        if "Accept-Language" in self.request.headers:
            languages = self.request.headers["Accept-Language"].split(",")
            locales = []
            for language in languages:
                parts = language.strip().split(";")
                if len(parts) > 1 and parts[1].startswith("q="):
                    try:
                        score = float(parts[1][2:])
                    except (ValueError, TypeError):
                        score = 0.0
                else:
                    score = 1.0

                # <Keyflow magic here!>
                if len(parts[0].split("-")) > 1:
                    last_dash = parts[0].rfind("-")
                    parts[0] = parts[0][:last_dash]
                # </Keyflow magic here!>
                locales.append((parts[0], score))
            if locales:
                locales.sort(key=lambda pair: pair[1], reverse=True)
                codes = [l[0] for l in locales]
                return locale.get(*codes)

        return locale.get(default)

    def __init__(self, *args, **kwargs):
        if "handler_regex" in kwargs:
            self.regex_handler = kwargs.get("handler_regex", None)
            del kwargs["handler_regex"]
        super(LoggingRequestHandler, self).__init__(*args, **kwargs)

        self._ = self.locale.translate

    # This handler is called when we trap an uncaught exception.
    def _handle_request_exception(self, e):
        logging.exception(e)

        # Return server internal error
        self.set_header("Content-Type", "application/json")
        self.write(
            json.dumps(
                {"status": http.HTTPStatus.BAD_REQUEST, "detail": str(e), "error": True}
            )
        )
        self.set_status(http.HTTPStatus.BAD_REQUEST)
        self.finish()

    def __request_data_dict(self):
        result = {
            "method": safe_decode(self.request.method),
            "uri": safe_decode(self.request.uri),
            "remote_ip": safe_decode(self.request.remote_ip),
            "body": safe_decode(self.request.body),
            "user_agent": safe_decode(self.request.headers.get("User-Agent")),
        }
        try:
            json_body = json.loads(self.request.body)
            for field in self.HIDDEN_FIELDS:
                if field in json_body:
                    json_body[field] = "__HIDDEN__"
            result["body"] = json.dumps(json_body)
        except ValueError:
            # Unparsable body is used as is
            pass
        if result.get("bearer_header", None):
            result["bearer_header"] = f"Authorization: {result['bearer_header']}"
        return result

    # Called before each request is handled
    def prepare(self):
        request_data = self.__request_data_dict()
        logging.info(
            '%(method)s %(uri)s (%(remote_ip)s) " "%('
            'user_agent)s" %(body)s' % request_data
        )
