import os

from . import logger
import api
import recipes
import storage


LOG = logger()
REQUIRED_OPTS = ['DB_USER', 'DB_PASS', 'DB_HOST', 'DB_NAME', 'REDIS_HOST',
                 'REDIS_PASSWORD']


def verify_parameters():
    missing = [n for n in REQUIRED_OPTS if not os.environ.get(n, None)]
    if len(missing) > 0:
        LOG.critical('Missing options in environment: %s' % missing)
        exit(1)


def database_connector():
    # in debug mode you might use mysql+pymysql for pure python solution
    db_proto = os.environ.get('DB_PROTO', 'mysql')
    db_user = os.environ['DB_USER']
    db_pass = os.environ['DB_PASS']
    db_host = os.environ['DB_HOST']
    db_name = os.environ['DB_NAME']
    return '%s://%s:%s@%s/%s' % (db_proto, db_user, db_pass, db_host, db_name)


def ensure_data(session):
    first = session.query(storage.Type).first()
    session.close()
    if not first:
        LOG.critical('Could not connect to SDK dump DB')
        exit(1)


def ensure_cache(store):
    pong = store.ping()
    if not pong:
        LOG.critical('Could not connect to Blueprint Cache')
        exit(1)


def initialize_app():
    verify_parameters()

    store = recipes.bootstrap_store(os.environ['REDIS_HOST'],
                                    os.environ['REDIS_PASSWORD'])
    ensure_cache(store)
    LOG.info('Cache Connected')

    db = storage.prepare_storage(database_connector())
    ensure_data(db())
    LOG.info('DB Connected')

    session_manager = storage.DBSessionFactory(db)
    return api.create_api([session_manager])


application = initialize_app()
