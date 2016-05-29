import logging
import os

from basil_common import configurables, db
from basil_common import falcon_support

import api
import recipes as rec
import storage

LOG = logging.getLogger(__name__)


def ensure_cache(store):
    pong = store.ping()
    if not pong:
        raise SystemExit('Could not connect to Blueprint Cache')
    LOG.info('Cache Connected')


def prepare_data_conn(engine):
    try:
        storage.Type.initialize(engine)
        if not storage.Type.meta_level:
            raise SystemExit('Cannot connect to Eve SDK Static Reference DB')
    except ImportError as ex:
        LOG.fatal(ex.message)
        raise
    else:
        LOG.info('DB Connected')


def initialize_app():
    required_options = ['DB_USER', 'DB_PASS', 'DB_HOST', 'DB_NAME',
                        'REDIS_HOST', 'REDIS_PASSWORD']
    configurables.verify(required_options)

    recipe_store = rec.bootstrap_store(os.environ['REDIS_HOST'],
                                       os.environ['REDIS_PASSWORD'])
    ensure_cache(recipe_store)

    db_connector = configurables.database_connector()
    db_engine = db.prepare_storage_engine(db_connector, 5200)
    db_store = db.prepare_storage_for_engine(db_engine)
    prepare_data_conn(db_engine())

    injector = falcon_support.InjectorMiddleware(
        {'recipes': rec.Recipes(recipe_store)})
    session_manager = db.SessionManager(db_store)
    middleware = [session_manager, injector]
    app = api.create_api(middleware)

    # Add a different root error handler based on: are we in production or not
    error_handler = configurables.root_error_handler()
    app.add_error_handler(Exception, error_handler)

    # TODO investigate falcon.set_error_serializer, just cause
    return app


application = initialize_app()
