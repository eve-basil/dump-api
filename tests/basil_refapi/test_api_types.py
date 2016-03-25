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
    resp = client.get('/types?name:starts=Tritan')
    assert_that(resp, has_property('status'), falcon.HTTP_OK)
    assert_that(resp.json, has_length(2))
    assert_that(resp.json[0], has_entry('name', 'Tritanium'))
    assert_that(resp.json[1], has_entry('id', 17916))


def test_get_by_id(client):
    resp = client.get('/types/34')
    assert_that(resp, has_property('status'), falcon.HTTP_OK)
    assert_that(resp.json, has_entry('name', 'Tritanium'))


def test_get_by_str_id(client):
    resp = client.get('/types/thirtyfour')
    assert_that(resp, has_property('status'), falcon.HTTP_BAD_REQUEST)


def test_get_by_unknown_id(client):
    resp = client.get('/types/99999999')
    assert_that(resp, has_property('status'), falcon.HTTP_NOT_FOUND)


def test_put_by_str_id(client):
    resp = client.put('/types/thirtyfour', None)
    assert_that(resp, has_property('status'), falcon.HTTP_METHOD_NOT_ALLOWED)
