import os
import sys

import api
import storage


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
        sys.stderr.write('DB_NAME not set in environment')
        os.exit(1)


def initialize_app():
    if not os.environ.get('DB_USER', None):
        sys.stderr.write('DB_USER not set in environment')
        os.exit(1)
    if not os.environ.get('DB_PASS', None):
        sys.stderr.write('DB_PASS not set in environment')
        os.exit(1)
    if not os.environ.get('DB_HOST', None):
        sys.stderr.write('DB_HOST not set in environment')
        os.exit(1)
    if not os.environ.get('DB_NAME', None):
        sys.stderr.write('DB_NAME not set in environment')
        os.exit(1)

    db = storage.prepare_storage(database_connector())
    ensure_data(db())

    sessionManager = storage.DBSessionFactory(db)
    return api.create_api([sessionManager])

app = initialize_app()
