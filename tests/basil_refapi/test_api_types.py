import basil_common.db as db
import falcon
import pytest
import hamcrest as _

import basil_refapi.api
import support


@pytest.fixture(scope="module")
def app():
    middleware = [db.SessionManager(support.session_maker())]
    return basil_refapi.api.create_api(middleware)

application = app()


def test_get_by_prefix(client):
    resp = client.get('/types?name:starts=Tritan')
    _.assert_that(resp, _.has_property('status'), falcon.HTTP_OK)
    _.assert_that(resp.json, _.has_length(2))
    _.assert_that(resp.json[0], _.has_entry('name', 'Tritanium'))
    _.assert_that(resp.json[1], _.has_entry('id', 17916))


def test_get_by_id(client):
    resp = client.get('/types/34')
    _.assert_that(resp, _.has_property('status'), falcon.HTTP_OK)
    _.assert_that(resp.json, _.has_entry('name', 'Tritanium'))


def test_get_by_str_id(client):
    resp = client.get('/types/thirtyfour')
    _.assert_that(resp, _.has_property('status'), falcon.HTTP_BAD_REQUEST)


def test_get_by_unknown_id(client):
    resp = client.get('/types/99999999')
    _.assert_that(resp, _.has_property('status'), falcon.HTTP_NOT_FOUND)


def test_put_by_str_id(client):
    resp = client.put('/types/thirtyfour', None)
    _.assert_that(resp, _.has_property('status'),
                  falcon.HTTP_METHOD_NOT_ALLOWED)
