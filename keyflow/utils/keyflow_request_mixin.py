import http
import logging


class KeyflowRequestMixin(object):
    def write_error(self, status_code, **kwargs):
        # We return all error messages using UTF-8
        self.set_header("Content-Type", "text/plain; charset=UTF-8")
        _ = self.locale.translate

        if "status" not in kwargs:
            kwargs["status"] = status_code

        if "error" not in kwargs:
            kwargs["error"] = True

        # Try to translate detail if passed along.
        if "detail" in kwargs:
            # Translator: this string does not need to be translated. But it needs to be here.
            keyword = kwargs["detail"]
            kwargs["detail"] = str(_(keyword))

        self.response = kwargs

        if not status_code >= 500:
            logging.info(self.response)
        else:
            logging.error(self.response)

        reason = None
        if "detail" in kwargs and isinstance(kwargs["detail"], str):
            reason = kwargs["detail"].replace("\n", " ")
        self.set_status(status_code, reason=reason)
        self.write(self.response)

    def write_success(
        self, output=None, status_code=http.HTTPStatus.OK, pagination_properties=None
    ):
        # We return all error messages using UTF-8
        self.set_header("Content-Type", "text/plain; charset=UTF-8")
        _ = self.locale.translate

        if output is None:
            output = self.response

        assert isinstance(status_code, int)

        # If the return data is a string, we try to translate it. This is a bit questionable. Should should really
        # differ between return data (which is what we have now) and return messages (that can be easily identified
        # and translated). Currently we return both in the key "data" depending on context.
        if isinstance(output, str):
            output = str(_(output))

        import pytz
        from datetime import datetime

        tz = datetime.utcnow().replace(tzinfo=pytz.utc)

        response_data = {
            "status": status_code,
            "data": output,
            "serverTime": tz.isoformat(),
        }

        if pagination_properties is not None:
            response_data["pagination"] = pagination_properties

        self.set_status(status_code)
        self.write(response_data)
