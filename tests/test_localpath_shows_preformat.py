import pytest

from renamer.localpath import error
from renamer.localpath.shows import match


def test_serie_preformat_simple():
    name = 'Some Show - 01x25 - Full Name.ext'
    test = match(name)
    assert test.title == 'Some Show'
    assert test.season == '01'
    assert test.episodes == ['25']


def test_serie_preformat_numbers():
    name = '11.22.33 - 01x25 - Full Name.ext'
    test = match(name)
    assert test.title == '11.22.33'
    assert test.season == '01'
    assert test.episodes == ['25']


def test_serie_preformat_with_year():
    name = 'Some Show 2017 - 01x25 - Full Name.ext'
    test = match(name)
    assert test.title == 'Some Show 2017'
    assert test.season == '01'
    assert test.episodes == ['25']


def test_serie_preformat_with_country():
    name = 'Some Show US - 01x25 - Full Name.ext'
    test = match(name)
    assert test.title == 'Some Show US'
    assert test.season == '01'
    assert test.episodes == ['25']


def test_serie_preformat_multiple_eps():
    name = 'Some Show - 01x24-25 - Full Name.ext'
    test = match(name)
    assert test.title == 'Some Show'
    assert test.season == '01'
    assert test.episodes == ['24', '25']


def test_serie_preformat_full():
    name = 'Some Show US 2017 - 01x24-25 - Full Name.ext'
    test = match(name)
    assert test.title == 'Some Show US 2017'
    assert test.season == '01'
    assert test.episodes == ['24', '25']


def test_serie_preformat_error():
    name = '01x25 - Full Name.ext'
    with pytest.raises(error.MatchNotFoundError):
        match(name)
