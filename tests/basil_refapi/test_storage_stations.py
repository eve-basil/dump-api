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
    r = db.Station.get(session, 60012574)
    expected = u'P-VYVL VII - Moon 1 - Guristas Assembly Plant'
    assert_that(r, has_property('name', equal_to(expected)))


def test_get_by_invalid_id(session):
    r = db.Station.get(session, -4)
    assert_that(r, none())


def test_find_unique(session):
    matches = db.Station.find(session, 'ROIR-Y II - Sisters')
    assert_that(matches, instance_of(list))
    assert_that(matches, has_length(1))
    expected = u'ROIR-Y II - Sisters of EVE Bureau'
    assert_that(matches[0], has_property('name', equal_to(expected)))


def test_find_none(session):
    matches = db.Station.find(session, 'Alpha Centauri')
    assert_that(matches, instance_of(list))
    assert_that(matches, empty())


def test_find_many(session):
    matches = db.Station.find(session, 'Penirgman IX')
    assert_that(matches, instance_of(list))
    assert_that(matches, has_length(10))


def test_dict(session):
    instance = db.Station(id=12345, name="Some", constellation_id=42,
                          system_id=30004727, region_id=10000016,
                          owning_corp=18, office_rental=7654321,
                          reprocessing_efficiency=0.5)
    instance._session = session

    returned = instance.dict()
    assert_that(returned, has_entries({'id': 12345, 'region_id': 10000016,
                                       'name': 'Some', 'system_id': 30004727,
                                       'constellation_id': 42,
                                       'owning_corp': 18,
                                       'office_rental': 7654321,
                                       'reprocessing_efficiency': 0.5,
                                       'system_name': 'R5-MM8',
                                       'region_name': 'Lonetrek'}))


def test_json(session):
    instance = db.Station(id=12345, name="Some", constellation_id=42,
                          system_id=30004727, region_id=10000016,
                          owning_corp=18, office_rental=7654321,
                          reprocessing_efficiency=0.5)
    instance._session = session

    returned = instance.json()
    # no error by reloading from json string
    json.loads(returned)
