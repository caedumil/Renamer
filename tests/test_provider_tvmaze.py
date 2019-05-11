import pytest

from renamer.provider import tvmaze, error


def test_search_simple():
    name = 'The Goldbergs'
    result = tvmaze.search(name)
    test = [x.thetvdb for x in result]
    assert 269653 in test                       # 'The Goldbergs 2013'


def test_search_multiple():
    name = 'Wanted'
    result = tvmaze.search(name, limit=10)
    test = [x.thetvdb for x in result]
    assert 78809 in test                        # 'Wanted'
    assert 271360 in test                       # 'Wanted AU'
    assert 304591 in test                       # 'Wanted AU 2016'


def test_search_numbers():
    name = '11 22 63'
    result = tvmaze.search(name)
    test = [x.thetvdb for x in result]
    assert 301824 in test                       # '11.22.63'


def test_search_with_symbol():
    name = 'Marvels Cloak and Dagger'
    result = tvmaze.search(name)
    test = [x.thetvdb for x in result]
    assert 341455 in test                       # 'Marvels Cloak and Dagger'


def test_search_with_ambiguity():
    name = 'The Gifted'
    result = tvmaze.search(name)
    test = [x.thetvdb for x in result]
    assert 328552 in test                       # 'The Gifted'


def test_search_error():
    name = 'Wrong Name'
    with pytest.raises(error.NotFoundError):
        tvmaze.search(name)
