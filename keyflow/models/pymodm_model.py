import logging
import time
from datetime import datetime

import pymodm
import pymongo
from pymodm import MongoModel, connect, errors, fields
from pymongo.errors import AutoReconnect, OperationFailure, CollectionInvalid
from tornado.options import options

from keyflow.models.custom_fields import DefaultDateTimeField


class BasePyModelModel(MongoModel):
    _phantom = False
    _db = None

    DB_RECONNECT_ATTEMPTS = 5
    deleted = fields.BooleanField(default=False)
    delete_stamp = fields.UUIDField(blank=True)
    created_at = DefaultDateTimeField()
    modified_at = fields.DateTimeField()

    @classmethod
    def reload_mappings(cls):
        logging.info("Reloading collections.")
        for clazz in cls._lazy_get_classes():
            if hasattr(clazz, "_reload_mapping"):
                clazz._reload_mapping()

    @classmethod
    def create_indexes(cls, database_name=None):
        logging.info("Creating indexes for model objects..")

        for clazz in cls._lazy_get_classes():
            if hasattr(clazz, "_ensure_indexes"):
                clazz._ensure_indexes()

            if hasattr(clazz, "_ensure_index"):
                clazz._ensure_index(clazz.F_DELETED, name=clazz.F_DELETED, sparse=True)

    @classmethod
    def _create_collection(cls):
        """
        This method provides a default implementation. It is called when the model is initialized.
        To provide a specialized implementation (such as for the activity model), this method is overridden in
        the derived class.
        """
        try:
            cls._db.validate_collection(cls._COLLECTION_NAME)
        except pymongo.errors.OperationFailure as e:
            # Create only when the collection do not exist.
            try:
                cls._db.create_collection(cls._COLLECTION_NAME)
            except CollectionInvalid as e:
                # the collection already exists
                logging.debug(
                    'Collection "%s" was not created. Reason: %s'
                    % (cls._COLLECTION_NAME, str(e))
                )

    @classmethod
    def create_collections(cls):
        logging.info("Creating collections.")
        for clazz in cls._lazy_get_classes():
            if hasattr(clazz, "_create_collection"):
                clazz._create_collection()

    @classmethod
    def remove_all_data_from_collections(cls, database_name="keyflow_tests"):
        """
        This method removes all documents from all collections.
        Should normally not be used but can come
        in handy in order to speed up tests for instance.
        """
        for collection in cls._db.list_collection_names():
            try:
                if collection == "activities" or collection == "keyflow_rules_log":
                    cls._db[collection].drop()
                else:
                    cls._db[collection].delete_many({})
            except OperationFailure:
                pass

    @classmethod
    def _lazy_get_classes(cls):
        from keyflow.models.party import Party
        from keyflow.models.guest_account import GuestAccount
        from keyflow.models.party_requests import PartyRequest
        from keyflow.models.party_chat_message import PartyChatMessage

        all_classes = (Party, GuestAccount, PartyRequest, PartyChatMessage)

        return all_classes

    @classmethod
    def initialize(
        cls,
        host=None,
        database_name=None,
        ssl=None,
        ssl_cert=None,
        use_ssl=True,
        use_authentication=True,
        user=None,
        password=None,
    ):
        from urllib.parse import quote_plus

        logging.info("Initializing database")
        hosts_string = host
        connect_string = "mongodb://"
        if not hosts_string:
            # This could be like =["db-01:27017", "db-02:27017","db-03:27017"]
            hosts_string = ",".join(options.mongodb_hosts)

        if not database_name:
            database_name = options.mongodb_database

        if use_authentication:
            # Could still be unset for development
            username = user or options.mongodb_user
            password = password or options.mongodb_password
            if username and password:
                connect_string = (
                    f"{connect_string}"
                    f"{quote_plus(username)}:"
                    f"{quote_plus(password)}@"
                )

        connect_string = f"{connect_string}{hosts_string}/{database_name}?"

        if use_ssl:
            if options.mongodb_ca_cert:
                ssl_string = (
                    f"ssl={str(options.mongodb_ssl).lower()}&tlsCAFile="
                    f"{quote_plus(options.mongodb_ca_cert)}"
                )
                connect_string = f"{connect_string}{ssl_string}"

        connect(connect_string)
        cls._db = pymodm.connection._get_db()
        for clazz in cls._lazy_get_classes():
            if hasattr(clazz, "_store_db_functions"):
                clazz._store_db_functions()

    @classmethod
    def _generate_id(cls):
        for _ in range(cls.DB_RECONNECT_ATTEMPTS):
            try:
                result = cls._db.command(
                    "findandmodify",
                    "seq",
                    query={"_id": cls._COLLECTION_NAME},
                    update={"$inc": {"seq": int(1)}},
                    new=True,
                    upsert=True,
                )
                return result["value"]["seq"]
                break
            except AutoReconnect as e:
                logging.warning("Reconnecting to DB: %s", str(e))
                time.sleep(1)

    def _prepare_phantom(self, data=None):
        self.id = self._generate_id()
        self.created_at = datetime.utcnow()
        self.modified_at = self.created_at
        # Adding the deleted flag to be false by default
        self.deleted = False

    def prepare_for_insert(self, prepare_phantom=True):
        if prepare_phantom:
            self._prepare_phantom()
        return

    def save(
        self,
        validate=True,
        cascade=None,
        full_clean=True,
        force_insert=False,
        *args,
        **kwargs,
    ):
        if self._phantom or not self.id:
            self._prepare_phantom()
            for _ in range(self.DB_RECONNECT_ATTEMPTS):
                try:
                    super(MongoModel, self).save(
                        cascade=None, full_clean=True, force_insert=False
                    )
                    break
                except errors.ValidationError as ex:
                    raise ex
                    break
                except AutoReconnect as e:
                    logging.warning("Reconnecting to DB: %s", str(e))
                    time.sleep(1)
        else:
            return False
        self._phantom = False
        return True
