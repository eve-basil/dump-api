import json

import pytest

import basil_refapi.storage as db
import support
from tests import *


@pytest.fixture(scope="module")
def session():
    engine, sessions = support.session_maker()
    return sessions()


def test_get_by_id(session):
    r = db.SolarSystem.get(session, 30004712)
    assert_that(r, has_property('name', equal_to('NOL-M9')))


def test_get_by_invalid_id(session):
    r = db.SolarSystem.get(session, -4)
    assert_that(r, none())


def test_find_unique(session):
    matches = db.SolarSystem.find(session, 'Utop')
    assert_that(matches, instance_of(list))
    assert_that(matches, has_length(1))
    assert_that(matches[0], has_property('name', equal_to('Utopia')))


def test_find_none(session):
    matches = db.SolarSystem.find(session, 'Alpha Centauri')
    assert_that(matches, instance_of(list))
    assert_that(matches, empty())


def test_find_many(session):
    matches = db.SolarSystem.find(session, 'G-')
    assert_that(matches, instance_of(list))
    assert_that(matches, has_length(34))


def test_dict():
    instance = db.SolarSystem(id=12345, name="Sol", security=1.0,
                              constellation_id=42, region_id=9,
                              faction_id=18)
    returned = instance.dict()
    assert_that(returned, has_entries({'id': 12345, 'name': 'Sol',
                                       'security': 1.0, 'region_id': 9,
                                       'constellation_id': 42,
                                       'faction_id': 18}))


def test_json():
    instance = db.SolarSystem(id=12345, name="Sol", security=1.0,
                              constellation_id=42, region_id=9,
                              faction_id=18)
    returned = instance.json()

    # no error by reloading from json string
    json.loads(returned)
