import json

import pytest

import basil_refapi.storage as db
import support
from tests import *


@pytest.fixture(scope="module")
def session():
    return support.session_maker()()


def test_get_by_id(session):
    r = db.Region.get(session, 10000010)
    assert_that(r, has_property('name', equal_to('Tribute')))


def test_get_by_invalid_id(session):
    r = db.Region.get(session, -4)
    assert_that(r, none())


def test_find_unique(session):
    matches = db.Region.find(session, 'Vale')
    assert_that(matches, instance_of(list))
    assert_that(matches, has_length(1))
    assert_that(matches[0], has_property('name',
                                         equal_to('Vale of the Silent')))


def test_find_none(session):
    matches = db.Region.find(session, 'Proxima')
    assert_that(matches, instance_of(list))
    assert_that(matches, empty())


def test_find_many(session):
    matches = db.Region.find(session, 'The')
    assert_that(matches, instance_of(list))
    assert_that(matches, has_length(5))


def test_dict():
    instance = db.Region(id=12345, name="Proxima", faction_id=18)
    returned = instance.dict()
    assert_that(returned, has_entries({'id': 12345, 'name': 'Proxima',
                                       'faction_id': 18}))


def test_json():
    instance = db.Region(id=12345, name="Proxima", faction_id=18)
    returned = instance.json()

    # no error by reloading from json string
    json.loads(returned)
