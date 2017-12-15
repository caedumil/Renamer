import pytest

from renamer import cli


def test_cli_parser_noargs():
    parser = cli.setParser()
    with pytest.raises(SystemExit):
        parser.parse_args([])


def test_cli_parser_wrong_log():
    parser = cli.setParser()
    with pytest.raises(SystemExit):
        parser.parse_args(['-l', 'wrong', 'test'])


def test_cli_parser_flags():
    parser = cli.setParser()
    args = parser.parse_args(['-s', '-r', '-y', 'test'])
    assert args.simple is True
    assert args.recursive is True
    assert args.no_confirm is True


def test_cli_parser_positional():
    test = ['test', 'file', 'path']
    parser = cli.setParser()
    args = parser.parse_args(test)
    assert args.path == test
