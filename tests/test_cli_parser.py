import pytest
from pathlib import Path

from renamer import cli


@pytest.fixture
def parser():
    return cli.setParser()


class TestCLI:
    def test_cli_parser_noargs(self, parser):
        with pytest.raises(SystemExit):
            parser.parse_args([])

    def test_cli_parser_set_log_lowercase(self, parser):
        args = parser.parse_args(['-l', 'debug', 'test'])
        assert args.loglevel == 'DEBUG'

    def test_cli_parser_set_log_uppercase(self, parser):
        args = parser.parse_args(['-l', 'ERROR', 'test'])
        assert args.loglevel == 'ERROR'

    def test_cli_parser_wrong_log(self, parser):
        with pytest.raises(SystemExit):
            parser.parse_args(['-l', 'wrong', 'test'])

    def test_cli_parser_positional(self, parser):
        args = parser.parse_args(['test', 'file', 'path'])
        assert args.path == [Path('test'), Path('file'), Path('path')]
