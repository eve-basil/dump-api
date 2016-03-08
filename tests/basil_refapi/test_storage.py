import json

import pytest
import hamcrest as _

import basil_refapi.storage as db
import support


@pytest.fixture(scope="module")
def session():
    return support.session_maker()()


def test_get_by_id(session):
    r = db.Type.get(session, 34)
    _.assert_that(r, _.has_property('name', _.equal_to('Tritanium')))


def test_get_by_invalid_id(session):
    r = db.Type.get(session, -4)
    _.assert_that(r, _.is_(_.none()))


def test_find_unique(session):
    matches = db.Type.find(session, 'Tritani')
    _.assert_that(matches, _.instance_of(list))
    _.assert_that(matches, _.has_length(1))
    _.assert_that(matches[0], _.has_property('name', _.equal_to('Tritanium')))


def test_find_none(session):
    matches = db.Type.find(session, 'Gandalf')
    _.assert_that(matches, _.instance_of(list))
    _.assert_that(matches, _.is_(_.empty()))


def test_find_many(session):
    matches = db.Type.find(session, 'Prototype')
    _.assert_that(matches, _.instance_of(list))
    _.assert_that(matches, _.has_length(33))


def test_dict():
    name = unicode('a\xac\u1234\u20ac\U00008000', 'utf-8', 'ignore')
    instance = db.Type(id=12345, group_id=4545, name=name, volume=1.2,
                       capacity=0, base_price=12500000, market_group_id=3232,
                       portion_size=1, published=False)
    returned = instance.dict()
    _.assert_that(returned, _.has_entries({'id': 12345, 'name': name,
                                           'volume': 1.2, 'capacity': 0,
                                           'portion_size': 1}))


def test_json():
    name = unicode('a\xac\u1234\u20ac\U00008000', 'utf-8', 'ignore')
    type = db.Type(id=12345, group_id=4545, name=name, volume=1.2, capacity=0,
                   base_price=12500000, market_group_id=3232, portion_size=1,
                   published=False)
    returned = type.json()

    # no error by reloading from json string
    json.loads(returned)

    _.assert_that(returned, _.contains_string('"id": 12345'))
    _.assert_that(returned, _.contains_string('"volume": 1.2'))
    _.assert_that(returned, _.contains_string('"capacity": 0'))
    _.assert_that(returned, _.contains_string('"portion_size": 1'))
