import pytest
from pathlib import Path

from renamer import cli


def test_cli_parser_noargs():
    parser = cli.setParser()
    with pytest.raises(SystemExit):
        parser.parse_args([])


def test_cli_parser_wrong_log():
    parser = cli.setParser()
    with pytest.raises(SystemExit):
        parser.parse_args(['-l', 'wrong', 'test'])


def test_cli_parser_positional():
    parser = cli.setParser()
    args = parser.parse_args(['test', 'file', 'path'])
    assert args.path == [Path('test'), Path('file'), Path('path')]
