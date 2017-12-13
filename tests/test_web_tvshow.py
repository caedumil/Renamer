import pytest

from renamer.web import types, error


def test_tvshow_simple():
    name = 'Wanted'
    test = types.TvShow(name)
    assert test.title == 'Wanted'
    assert test.thetvdb == 78809


def broken_test_tvshow_numbers():
    name = '11 22 63'
    test = types.TvShow(name)
    assert test.title == '11.22.63'
    assert test.thetvdb == 301824


def test_tvshow_with_year():
    name = 'The Goldbergs'
    year = '2013'
    test = types.TvShow(name, year=year)
    assert test.title == 'The Goldbergs'
    assert test.thetvdb == 269653


def test_tvshow_with_country():
    name = 'Wanted'
    country = 'AU'
    test = types.TvShow(name, country=country)
    assert test.title == 'Wanted'
    assert test.thetvdb == 271360


def test_tvshow_full():
    name = 'Wanted'
    country = 'AU'
    year = '2016'
    test = types.TvShow(name, country=country, year=year)
    assert test.title == 'Wanted'
    assert test.thetvdb == 304591


def test_tvshow_error():
    name = 'Wrong Name'
    with pytest.raises(error.NotFoundError):
        types.TvShow(name)
