import falcon
import pytest

from basil_refapi import api
from tests import *
from tests.basil_refapi import support


@pytest.fixture(scope="module")
def app():
    engine, sessions = support.session_maker()
    middleware = [db.SessionManager(sessions)]
    return api.create_api(middleware)

application = app()


def test_get_manufacturing_by_id(client):
    resp = client.get('/recipes/manufacturing/691')
    assert_that(resp, has_property('status'), falcon.HTTP_OK)

    assert_that(resp.json, has_entry('time', 6000))

    assert_that(resp.json, has_key('materials'))
    assert_that(resp.json['materials'], has_length(7))

    assert_that(resp.json, has_key('products'))
    assert_that(resp.json['products'], has_length(1))
    assert_that(resp.json['products'][0], has_entry('typeID', 587))
    assert_that(resp.json['products'][0], has_entry('quantity', 1))


def test_get_manufacturing_by_bad_id(client):
    resp = client.get('/recipes/manufacturing/1')
    assert_that(resp, has_property('status'), falcon.HTTP_NOT_FOUND)


def test_get_invention_by_id(client):
    resp = client.get('/recipes/invention/691')
    assert_that(resp, has_property('status'), falcon.HTTP_OK)

    assert_that(resp.json, has_entry('time', 63900))

    assert_that(resp.json, has_entry('materials', instance_of(list)))
    assert_that(resp.json['materials'], has_length(2))

    assert_that(resp.json, has_key('products'))
    prod = resp.json['products']
    assert_that(prod, has_length(2))
    assert_that(prod, has_item(has_entry('typeID', 11372)))
    assert_that(prod, has_item(has_entry('quantity', 1)))


def test_get_invention_by_bad_id(client):
    resp = client.get('/recipes/invention/1')
    assert_that(resp, has_property('status'), falcon.HTTP_NOT_FOUND)


def test_get_copying_by_id(client):
    resp = client.get('/recipes/copying/691')
    assert_that(resp, has_property('status'), falcon.HTTP_OK)
    assert_that(resp.json, has_entry('time', 4800))


def test_get_copying_by_bad_id(client):
    resp = client.get('/recipes/copying/1')
    assert_that(resp, has_property('status'), falcon.HTTP_NOT_FOUND)


def test_research_material_by_id(client):
    resp = client.get('/recipes/research_material/691')
    assert_that(resp, has_property('status'), falcon.HTTP_OK)
    assert_that(resp.json, has_entry('time', 2100))


def test_get_research_material_by_bad_id(client):
    resp = client.get('/recipes/research_material/1')
    assert_that(resp, has_property('status'), falcon.HTTP_NOT_FOUND)


def test_research_time_by_id(client):
    resp = client.get('/recipes/research_time/691')
    assert_that(resp, has_property('status'), falcon.HTTP_OK)
    assert_that(resp.json, has_entry('time', 2100))


def test_get_research_time_by_bad_id(client):
    resp = client.get('/recipes/research_time/1')
    assert_that(resp, has_property('status'), falcon.HTTP_NOT_FOUND)


def test_get_unknown_activity_by_id(client):
    resp = client.get('/recipes/unknown/1')
    assert_that(resp, has_property('status'), falcon.HTTP_NOT_FOUND)

# FUTURE more tests
