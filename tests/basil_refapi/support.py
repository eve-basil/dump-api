import os

from basil_common import db
from basil_common.falcon_support import InjectorMiddleware
from basil_refapi import recipes
import tests.basil_refapi


def test_db_conn():
    data_path = os.path.normpath(tests.basil_refapi.__path__[0] + '/../..')
    return "sqlite:///%s/data/eve.db" % data_path


def session_maker():
    conn_str = test_db_conn()
    engine = db.prepare_storage_engine(connect_str=conn_str, conn_timeout=120)
    return engine, db.prepare_storage_for_engine(engine)


def test_cache_conn():
    return recipes.bootstrap_store(os.environ['REDIS_HOST'],
                                   os.environ.get('REDIS_PASSWORD', ''))


def cache_middleware():
    recipe_proxy = recipes.Recipes(test_cache_conn())
    return InjectorMiddleware({'recipes': recipe_proxy})
