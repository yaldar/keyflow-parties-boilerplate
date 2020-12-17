import pymongo
from tornado import testing
from tornado.options import options
from tornado.web import Application

from keyflow.keyflow_parties_application import KeyflowPartiesApplication
from keyflow.main import setup_defines
from keyflow.models.party import Party
from keyflow.models.pymodm_model import BasePyModelModel


class TestModelReadWrite(testing.AsyncHTTPTestCase):
    database_name = "keyflow_tests"

    def get_app(self) -> Application:

        return KeyflowPartiesApplication(database_name="keyflow_tests")

    @classmethod
    def setUpClass(cls) -> None:
        setup_defines()
        if BasePyModelModel._db:
            BasePyModelModel.remove_all_data_from_collections(cls.database_name())
        else:
            pymongo.MongoClient(options.mongodb_hosts).drop_database(cls.database_name)
            BasePyModelModel.initialize(
                database_name=cls.database_name,
                host=options.mongodb_hosts,
                use_ssl=False,
                use_authentication=False,
            )
            BasePyModelModel.create_collections()
            BasePyModelModel.reload_mappings()
            BasePyModelModel.create_indexes()

    def setUp(self):
        BasePyModelModel.remove_all_data_from_collections(self.database_name)
        BasePyModelModel.create_collections()
        super().setUp()

    def test_create_list_on_models(self):
        party_a = Party()
        party_a.title = "New Party"
        party_a.save()

        self.assertEqual(Party.objects.count(), 1)
