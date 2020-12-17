import http

from tornado import gen
from tornado.web import RequestHandler

from keyflow.utils.keyflow_request_mixin import KeyflowRequestMixin


class PartiesListHandler(RequestHandler, KeyflowRequestMixin):
    def get_worker(self):
        return "Success"

    @gen.coroutine
    def get(self):
        try:
            search_args = self.get_argument("search", None, True)
            filter_args = self.get_argument("filter", None, True)
            success, result_data, paging = yield self.application.threadPool.submit(
                self.get_worker, self.request, search_args, filter_args
            )
            self.write_success(output=result_data, pagination_properties=paging)
            self.finish()
        except Exception as e:
            self.write_error(http.HTTPStatus.BAD_REQUEST, detail=str(e))
