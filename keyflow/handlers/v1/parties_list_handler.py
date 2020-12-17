import http

from tornado import gen

from keyflow.services.parties_service_v1 import PartiesServiceV1
from keyflow.utils.keyflow_parties_app_handler_base import KeyflowPartiesAppHandlerBase


class PartiesListHandler(KeyflowPartiesAppHandlerBase):
    def get_worker(self, *args, **kwargs):
        parties_service = PartiesServiceV1()
        parties = parties_service.get_parties()
        return http.HTTPStatus.OK, parties_service.serialize_parties(parties)

    @gen.coroutine
    def get(self):
        try:
            search_args = self.get_argument("search", None, True)
            filter_args = self.get_argument("filter", None, True)
            success, result_data = yield self.application.threadPool.submit(
                self.get_worker, self.request, search_args, filter_args
            )
            self.write_success(output=result_data)
            self.finish()
        except Exception as e:
            self.write_error(http.HTTPStatus.BAD_REQUEST, detail=str(e))
