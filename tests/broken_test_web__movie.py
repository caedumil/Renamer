import pytest

from renamer import web


def test_movie_simple():
    name = 'Starship Troopers'
    year = '1997'
    test = web.Movie(name, year)
    assert test.title == 'Some Blockbuster Title'
    assert test.year == '2017'
    assert test.IMDB == 'tt0120201'


def test_movie_error():
    name = 'Wrong Name'
    year = '2999'
    with pytest.raises(web.NotFoundError):
        web.Movie(name, year)
