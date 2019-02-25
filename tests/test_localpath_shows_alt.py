import pytest

from renamer.localpath import error
from renamer.localpath.shows import match


def test_serie_alt_simple():
    name = 'some.show.125.foo.bar.ext'
    test = match(name)
    assert test.title == 'some.show'
    assert test.season == '01'
    assert test.episodes == ['25']


def test_serie_alt_numbers():
    name = '11.22.33.125.foo.bar.ext'
    test = match(name)
    assert test.title == '11.22.33'
    assert test.season == '01'
    assert test.episodes == ['25']


def test_serie_alt_with_year():
    name = 'some.show.2017.125.foo.bar.ext'
    test = match(name)
    assert test.title == 'some.show.2017'
    assert test.season == '01'
    assert test.episodes == ['25']


def test_serie_alt_with_country():
    name = 'some.show.us.125.foo.bar.ext'
    test = match(name)
    assert test.title == 'some.show.us'
    assert test.season == '01'
    assert test.episodes == ['25']


def test_serie_alt_multiple_eps():
    name = 'some.show.12425.foo.bar.ext'
    test = match(name)
    assert test.title == 'some.show'
    assert test.season == '01'
    assert test.episodes == ['24', '25']


def test_serie_alt_full():
    name = 'some.show.us.2017.12425.foo.bar.ext'
    test = match(name)
    assert test.title == 'some.show.us.2017'
    assert test.season == '01'
    assert test.episodes == ['24', '25']


def test_serie_alt_error():
    name = '125.foo.bar.ext'
    with pytest.raises(error.MatchNotFoundError):
        match(name)
