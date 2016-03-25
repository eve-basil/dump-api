import os

import basil_common.db as db
import tests.basil_refapi

from basil_common.falcon_support import InjectorMiddleware
from basil_refapi import recipes


def test_db_conn():
    data_path = os.path.normpath(tests.basil_refapi.__path__[0] + '/../..')
    return "sqlite:///%s/data/eve.db" % data_path


def session_maker():
    conn_str = test_db_conn()
    return db.prepare_storage(connect_str=conn_str, conn_timeout=600)


def test_cache_conn():
    return recipes.bootstrap_store(os.environ['REDIS_HOST'],
                                   os.environ['REDIS_PASSWORD'])


def cache_middleware():
    recipe_proxy = recipes.Recipes(test_cache_conn())
    return InjectorMiddleware({'recipes': recipe_proxy})
