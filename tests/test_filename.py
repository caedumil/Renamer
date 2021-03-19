import pytest

from renamer import filename


class TestBase:
    def test_instantiation(self):
        with pytest.raises(TypeError):
            filename.base.Media()


class TestAnime:
    def test_false(self):
        name = ''
        assert filename.Animes.match(name) is False
        assert filename.Animes.parse(name) == ''


class TestSerie:
    def test_scene_false(self):
        name = 'S01E25.FOO.BAR.ext'
        assert filename.Series.match(name) is False
        assert filename.Series.parse(name) == ''

    def test_prefmt_false(self):
        name = '01x25 - Full Name.ext'
        assert filename.Series.match(name) is False
        assert filename.Series.parse(name) == ''

    def test_scene_simple(self):
        name = 'Some.Show.S01E25.FOO.BAR.ext'
        assert filename.Series.match(name) is True
        assert filename.Series.parse(name) == 'Some.Show'

    def test_prefmt_simple(self):
        name = 'Some Show - 01x25 - Full Name.ext'
        assert filename.Series.match(name) is True
        assert filename.Series.parse(name) == 'Some Show'

    def test_scene_numbers(self):
        name = '11.22.33.S01E25.FOO.BAR.ext'
        assert filename.Series.match(name) is True
        assert filename.Series.parse(name) == '11.22.33'

    def test_prefmt_numbers(self):
        name = '11.22.33 - 01x25 - Full Name.ext'
        assert filename.Series.match(name) is True
        assert filename.Series.parse(name) == '11.22.33'

    def test_scene_with_year(self):
        name = 'Some.Show.2017.S01E25.FOO.BAR.ext'
        assert filename.Series.match(name) is True
        assert filename.Series.parse(name) == 'Some.Show.2017'

    def test_premft_with_year(self):
        name = 'Some Show 2017 - 01x25 - Full Name.ext'
        assert filename.Series.match(name) is True
        assert filename.Series.parse(name) == 'Some Show 2017'

    def test_scene_with_country(self):
        name = 'Some.Show.US.S01E25.FOO.BAR.ext'
        assert filename.Series.match(name) is True
        assert filename.Series.parse(name) == 'Some.Show.US'

    def test_prefmt_with_country(self):
        name = 'Some Show US - 01x25 - Full Name.ext'
        assert filename.Series.match(name) is True
        assert filename.Series.parse(name) == 'Some Show US'

    def test_scene_multiple_eps(self):
        name = 'Some.Show.S01E24-E25.FOO.BAR.ext'
        assert filename.Series.match(name) is True
        assert filename.Series.parse(name) == 'Some.Show'

    def test_prefmt_multiple_eps(self):
        name = 'Some Show - 01x24-25 - Full Name.ext'
        assert filename.Series.match(name) is True
        assert filename.Series.parse(name) == 'Some Show'

    def test_scene_all(self):
        name = 'Some.Show.US.2017.S01E24-E25.FOO.BAR.ext'
        assert filename.Series.match(name) is True
        assert filename.Series.parse(name) == 'Some.Show.US.2017'

    def test_prefmt_all(self):
        name = 'Some Show US 2017 - 01x24-25 - Full Name.ext'
        assert filename.Series.match(name) is True
        assert filename.Series.parse(name) == 'Some Show US 2017'


class TestMovie:
    def test_false(self):
        name = 'Some.Movie.1080p.TAG1.TAG2.TAG3.ext'
        assert filename.Movies.match(name) is False
        assert filename.Movies.parse(name) == ''

    def test_sep_dots(self):
        name = 'Some.Movie.2020.1080p.TAG1.TAG2.TAG3.ext'
        assert filename.Movies.match(name) is True
        assert filename.Movies.parse(name) == 'Some.Movie.2020'

    def test_sep_spaces(self):
        name = 'Some Movie 2020.ext'
        assert filename.Movies.match(name) is True
        assert filename.Movies.parse(name) == 'Some Movie 2020'
