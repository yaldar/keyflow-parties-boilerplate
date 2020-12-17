import http


class KeyflowRequestMixin(object):
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
