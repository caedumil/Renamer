import pytest

from renamer import localpath


def test_serie_scene_simple():
    name = 'Some.Show.S01E25.FOO.BAR.ext'
    test = localpath.SerieFile(name)
    assert test.title == 'Some Show'
    assert test.country is None
    assert test.year is None
    assert test.season == '01'
    assert test.episodes == ['25']


def test_serie_scene_numbers():
    name = '11.22.33.S01E25.FOO.BAR.ext'
    test = localpath.SerieFile(name)
    assert test.title == '11 22 33'
    assert test.country is None
    assert test.year is None
    assert test.season == '01'
    assert test.episodes == ['25']


def test_serie_scene_with_year():
    name = 'Some.Show.2017.S01E25.FOO.BAR.ext'
    test = localpath.SerieFile(name)
    assert test.title == 'Some Show'
    assert test.country is None
    assert test.year == '2017'
    assert test.season == '01'
    assert test.episodes == ['25']


def test_serie_scene_with_country():
    name = 'Some.Show.US.S01E25.FOO.BAR.ext'
    test = localpath.SerieFile(name)
    assert test.title == 'Some Show'
    assert test.country == 'US'
    assert test.year is None
    assert test.season == '01'
    assert test.episodes == ['25']


def test_serie_scene_multiple_eps():
    name = 'Some.Show.S01E24-E25.FOO.BAR.ext'
    test = localpath.SerieFile(name)
    assert test.title == 'Some Show'
    assert test.country is None
    assert test.year is None
    assert test.season == '01'
    assert test.episodes == ['24', '25']


def test_serie_scene_full():
    name = 'Some.Show.US.2017.S01E24-E25.FOO.BAR.ext'
    test = localpath.SerieFile(name)
    assert test.title == 'Some Show'
    assert test.country == 'US'
    assert test.year == '2017'
    assert test.season == '01'
    assert test.episodes == ['24', '25']


def test_serie_scene_error():
    name = 'S01E25.FOO.BAR.ext'
    with pytest.raises(localpath.error.MatchNotFoundError):
        localpath.SerieFile(name)
