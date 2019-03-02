import pytest

from renamer.localpath.names import parse


def test_name_scene_simple():
    name = 'Some Show'
    test = parse(name)
    assert test.title == 'SOME SHOW'
    assert test.country == None
    assert test.year == None


def test_name_scene_numbers():
    name = '11.22.33'
    test = parse(name)
    assert test.title == '11 22 33'
    assert test.country == None
    assert test.year == None


def test_name_scene_with_country():
    name = 'Some Show.US'
    test = parse(name)
    assert test.title == 'SOME SHOW US'
    assert test.country == 'US'
    assert test.year == None


def test_name_scene_with_year():
    name = 'Some Show.2017'
    test = parse(name)
    assert test.title == 'SOME SHOW'
    assert test.country == None
    assert test.year == '2017'


def test_name_scene_full():
    name = 'Some Show.US.2017'
    test = parse(name)
    assert test.title == 'SOME SHOW US'
    assert test.country == 'US'
    assert test.year == '2017'
