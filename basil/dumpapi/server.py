import logging
import os

import api
import storage

logging = logging.getLogger(__name__)

_REQUIRED_OPTS = ['DB_USER', 'DB_PASS', 'DB_HOST', 'DB_NAME']


def verify_parameters():
    missing = [n for n in _REQUIRED_OPTS if not os.environ.get(n, None)]
    if len(missing) > 0:
        logging.critical('Missing options in environment: %s' % missing)
        exit(1)


def database_connector():
    db_user = os.environ['DB_USER']
    db_pass = os.environ['DB_PASS']
    db_host = os.environ['DB_HOST']
    db_name = os.environ['DB_NAME']
    return 'mysql://%s:%s@%s/%s' % (db_user, db_pass, db_host, db_name)


def ensure_data(session):
    first = session.query(storage.Type).first()
    session.close()
    if not first:
        logging.critical('Could not connect to SDK dump DB')
        exit(1)


def initialize_app():
    verify_parameters()

    db = storage.prepare_storage(database_connector())
    ensure_data(db())

    session_manager = storage.DBSessionFactory(db)
    return api.create_api([session_manager])

application = initialize_app()
