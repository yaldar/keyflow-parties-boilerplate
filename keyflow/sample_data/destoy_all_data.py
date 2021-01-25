import logging

from tornado.options import options

from keyflow.main import setup_defines
from keyflow.models.pymodm_model import BasePyModelModel


def main():
    confirmation = input(
        f"This would destroy all data from your database: "
        f"keyflow_parties. Type YES to continue: "
    )
    if not str(confirmation).strip() == "YES":
        return

    BasePyModelModel.remove_all_data_from_collections(database_name="keyflow_parties")


if __name__ == "__main__":
    setup_defines()
    options.mongodb_hosts = "127.0.0.1:27017"
    BasePyModelModel.initialize(
        database_name="keyflow_parties",
        host=options.mongodb_hosts,
        use_authentication=False,
        use_ssl=False,
    )
    main()
