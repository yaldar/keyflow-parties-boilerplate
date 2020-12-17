import logging

import tornado
from tornado.options import options

from keyflow.keyflow_parties_application import KeyflowPartiesApplication
from keyflow.utils.safe_defines import safe_define


def setup_defines():
    safe_define("port", default=8000, help="run on the given port", type=int)
    safe_define(
        "enable_xheaders",
        default=1,
        help="enable support for X-Real-Ip and X-Scheme headers",
        type=int,
    )
    safe_define(
        "child_processes",
        default=1,
        help="fork the given number of child processes",
        type=int,
    )
    safe_define(
        "mongodb_database", default="keyflow", help="Mongodb " "database name", type=str
    )
    safe_define(
        "mongodb-hosts", default="127.0.0.1:27017", help="Mongodb " "host", type=str
    )


def start():
    setup_defines()
    http_server = tornado.httpserver.HTTPServer(
        KeyflowPartiesApplication(debug=True, database_name=options.mongodb_hosts),
        xheaders=bool(options.enable_xheaders),
    )
    http_server.bind(8080)

    try:
        http_server.start(options.child_processes)
        logging.info("Server started")
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        logging.info("Server loop interrupted. Exiting.")


if __name__ == "__main__":
    start()
