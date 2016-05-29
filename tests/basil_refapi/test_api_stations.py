import falcon
import pytest

import basil_common.db as db
from basil_refapi import api
import support
from tests import *


@pytest.fixture(scope="module")
def app():
    engine, sessions = support.session_maker()
    middleware = [db.SessionManager(sessions)]
    return api.create_api(middleware)

application = app()


def test_get_by_prefix(client):
    resp = client.get('/stations?name:starts=Penirgman+IX')
    assert_that(resp, has_property('status', equal_to(falcon.HTTP_OK)))
    assert_that(resp.json, has_length(10))
    assert_that(resp.json[0], has_entry('id', 60002179))
    expected = {u'system_name': u'Penirgman', u'region_name': u'Domain',
                u'office_rental': 10000, u'constellation_id': 20000509,
                u'system_id': 30003488, u'region_id': 10000043,
                u'owning_corp': 1000019, u'id': 60002179, u'name':
                    u'Penirgman IX - Moon 11 - Ishukone Corporation Factory',
                u'reprocessing_efficiency': 0.3}
    assert_that(resp.json, has_item(expected))


def test_get_by_id(client):
    resp = client.get('/stations/60012574')
    assert_that(resp, has_property('status', equal_to(falcon.HTTP_OK)))
    expected = 'P-VYVL VII - Moon 1 - Guristas Assembly Plant'
    assert_that(resp.json, has_entry('name', expected))


def test_get_by_str_id(client):
    resp = client.get('/stations/thirtyfour')
    assert_that(resp, has_property('status',
                                   equal_to(falcon.HTTP_BAD_REQUEST)))


def test_get_by_unknown_id(client):
    resp = client.get('/stations/99999999')
    assert_that(resp, has_property('status',
                                   equal_to(falcon.HTTP_NOT_FOUND)))


def test_put_by_str_id(client):
    resp = client.put('/stations/thirtyfour', None)
    assert_that(resp, has_property('status',
                                   equal_to(falcon.HTTP_METHOD_NOT_ALLOWED)))
