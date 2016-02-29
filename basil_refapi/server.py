import os

from basil_common import configurables, db, logger
from basil_common import falcon_support

import api
import recipes as rec
import storage

LOG = logger()


def ensure_cache(store):
    pong = store.ping()
    if not pong:
        raise SystemExit('Could not connect to Blueprint Cache')


def ensure_data(session):
    first = session.query(storage.Type).first()
    session.close()
    if not first:
        raise SystemExit('Could not connect to Eve SDK Static Reference DB')


def initialize_app():
    required_options = ['DB_USER', 'DB_PASS', 'DB_HOST', 'DB_NAME',
                        'REDIS_HOST', 'REDIS_PASSWORD']
    configurables.verify(required_options)

    recipe_store = rec.bootstrap_store(os.environ['REDIS_HOST'],
                                       os.environ['REDIS_PASSWORD'])
    ensure_cache(recipe_store)
    LOG.info('Cache Connected')

    db_store = db.prepare_storage(configurables.database_connector(), 7200)
    ensure_data(db_store())
    LOG.info('DB Connected')

    injector = falcon_support.InjectorMiddleware(
        {'recipes': rec.Recipes(recipe_store)})
    session_manager = db.SessionManager(db_store)
    app = api.create_api([session_manager, injector])

    # Add a different root error handler based on: are we in production or not
    error_handler = configurables.root_error_handler()
    app.add_error_handler(Exception, error_handler)

    # TODO investigate falcon.set_error_serializer, just cause
    return app


application = initialize_app()
