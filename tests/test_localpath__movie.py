import pytest

from renamer import localpath


def test_movie_simple():
    name = 'Some.Blockbuster.Title.2017.FOO.BAR.ext'
    test = localpath.MovieFile(name)
    assert test.title == 'Some Blockbuster Title'
    assert test.year == '2017'


def test_movie_simple_spaces():
    name = 'Some Blockbuster Title 2017 FOO BAR.ext'
    with pytest.raises(localpath.MatchNotFoundError):
        localpath.MovieFile(name)


def test_movie_error():
    name = 'Some.Blockbuster.Title.FOO.BAR.ext'
    with pytest.raises(localpath.MatchNotFoundError):
        localpath.MovieFile(name)
