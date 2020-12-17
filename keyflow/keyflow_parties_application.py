from concurrent.futures.thread import ThreadPoolExecutor

import tornado
from tornado.options import options

from keyflow.controller.urls import urls
from keyflow.models.pymodm_model import BasePyModelModel
from keyflow.utils.keyflow_web_application_handler import KeyflowWebApplicationHelper


class KeyflowPartiesApplication(tornado.web.Application):
    def __init__(self, database_name=None, debug=None, cookie_secret=None):
        settings = dict(debug=True)
        self.threadPool = ThreadPoolExecutor(4)

        handlers_with_parameters = KeyflowWebApplicationHelper.add_handler_regex_to_handler_parameters(
            urls
        )

        tornado.web.Application.__init__(self, handlers_with_parameters, **settings)
        options.mongodb_hosts = "127.0.0.1:27017"
        BasePyModelModel.initialize(
            database_name=database_name,
            host=options.mongodb_hosts,
            use_authentication=False,
            use_ssl=False,
        )
