from tornado.web import url

from keyflow.handlers.v1.parties_list_handler import PartiesListHandler

urls = [url(r"/v1/parties/", PartiesListHandler, name="list_parties")]
