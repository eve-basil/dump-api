import os

import basil_common.db as db
import tests.basil_refapi


def test_db_conn():
    data_path = os.path.normpath(tests.basil_refapi.__path__[0] + '/../..')
    return "sqlite:///%s/data/eve.db" % data_path


def session_maker():
    conn_str = test_db_conn()
    return db.prepare_storage(connect_str=conn_str, conn_timeout=600)
