import basil_common.db as db
import falcon
import pytest

from basil_refapi import api
import support
from tests import *


@pytest.fixture(scope="module")
def app():
    middleware = [db.SessionManager(support.session_maker())]
    return api.create_api(middleware)

application = app()


def test_get_by_prefix(client):
    resp = client.get('/systems?name:starts=G-')
    assert_that(resp, has_property('status', equal_to(falcon.HTTP_OK)))
    assert_that(resp.json, has_length(34))
    assert_that(resp.json[0], has_entry('id', 30001041))
    assert_that(resp.json, has_item({u'region_id': 10000014,
                                     u'faction_id': None,
                                     u'constellation_id': 20000179,
                                     u'security': -0.1357720952711935,
                                     u'id': 30001227,
                                     u'name': u'G-AOTH'}))


def test_get_by_id(client):
    resp = client.get('/systems/30001213')
    assert_that(resp, has_property('status', equal_to(falcon.HTTP_OK)))
    assert_that(resp.json, has_entry('name', 'MUXX-4'))


def test_get_by_str_id(client):
    resp = client.get('/systems/thirtyfour')
    assert_that(resp, has_property('status',
                                   equal_to(falcon.HTTP_BAD_REQUEST)))


def test_get_by_unknown_id(client):
    resp = client.get('/systems/99999999')
    assert_that(resp, has_property('status',
                                   equal_to(falcon.HTTP_NOT_FOUND)))


def test_put_by_str_id(client):
    resp = client.put('/systems/thirtyfour', None)
    assert_that(resp, has_property('status',
                                   equal_to(falcon.HTTP_METHOD_NOT_ALLOWED)))
