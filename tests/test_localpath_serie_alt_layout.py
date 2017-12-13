import pytest

from renamer.localpath import types, error


def test_serie_alt_simple():
    name = 'some.show.125.foo.bar.ext'
    test = types.SerieFile(name)
    assert test.title == 'Some Show'
    assert test.country is None
    assert test.year is None
    assert test.season == '01'
    assert test.episodes == ['25']


def test_serie_alt_numbers():
    name = '11.22.33.125.foo.bar.ext'
    test = types.SerieFile(name)
    assert test.title == '11 22 33'
    assert test.country is None
    assert test.year is None
    assert test.season == '01'
    assert test.episodes == ['25']


def broken_test_serie_alt_with_year():
    name = 'some.show.2017.125.foo.bar.ext'
    test = types.SerieFile(name)
    assert test.title == 'Some Show'
    assert test.country is None
    assert test.year == '2017'
    assert test.season == '01'
    assert test.episodes == ['25']


def broken_test_serie_alt_with_country():
    name = 'some.show.us.125.foo.bar.ext'
    test = types.SerieFile(name)
    assert test.title == 'Some Show'
    assert test.country == 'US'
    assert test.year is None
    assert test.season == '01'
    assert test.episodes == ['25']


def test_serie_alt_multiple_eps():
    name = 'some.show.12425.foo.bar.ext'
    test = types.SerieFile(name)
    assert test.title == 'Some Show'
    assert test.country is None
    assert test.year is None
    assert test.season == '01'
    assert test.episodes == ['24', '25']


def broken_test_serie_alt_full():
    name = 'some.show.us.2017.12425.foo.bar.ext'
    test = types.SerieFile(name)
    assert test.title == 'Some Show'
    assert test.country == 'US'
    assert test.year == '2017'
    assert test.season == '01'
    assert test.episodes == ['24', '25']


def test_serie_alt_error():
    name = '125.foo.bar.ext'
    with pytest.raises(error.MatchNotFoundError):
        types.SerieFile(name)
