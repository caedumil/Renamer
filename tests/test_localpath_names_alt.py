import pytest

from renamer.localpath.names import parse


def test_name_scene_simple():
    name = 'some.show'
    test = parse(name)
    assert test.title == 'Some Show'
    assert test.country == None
    assert test.year == None


def test_name_scene_numbers():
    name = '11.22.33'
    test = parse(name)
    assert test.title == '11 22 33'
    assert test.country == None
    assert test.year == None


def broken_test_name_scene_with_country():
    name = 'some.show.us'
    test = parse(name)
    assert test.title == 'Some Show'
    assert test.country == 'US'
    assert test.year == None


def test_name_scene_with_year():
    name = 'some.show.2017'
    test = parse(name)
    assert test.title == 'Some Show'
    assert test.country == None
    assert test.year == '2017'


def broken_test_name_scene_full():
    name = 'some.show.us.2017'
    test = parse(name)
    assert test.title == 'Some Show'
    assert test.country == 'US'
    assert test.year == '2017'