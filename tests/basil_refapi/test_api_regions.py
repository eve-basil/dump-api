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
    resp = client.get('/regions?name:starts=The')
    assert_that(resp, has_property('status'), falcon.HTTP_OK)
    assert_that(resp.json, has_length(5))
    assert_that(resp.json[0], has_entry('name', 'The Bleak Lands'))
    assert_that(resp.json, has_item({u'faction_id': 500001, u'id': 10000033,
                                     u'name': u'The Citadel'}))


def test_get_by_id(client):
    resp = client.get('/regions/10000036')
    assert_that(resp, has_property('status'), falcon.HTTP_OK)
    assert_that(resp.json, has_entry('name', 'Devoid'))


def test_get_by_str_id(client):
    resp = client.get('/regions/thirtyfour')
    assert_that(resp, has_property('status'), falcon.HTTP_BAD_REQUEST)


def test_get_by_unknown_id(client):
    resp = client.get('/regions/99999999')
    assert_that(resp, has_property('status'), falcon.HTTP_NOT_FOUND)


def test_put_by_str_id(client):
    resp = client.put('/regions/thirtyfour', None)
    assert_that(resp, has_property('status'), falcon.HTTP_METHOD_NOT_ALLOWED)
