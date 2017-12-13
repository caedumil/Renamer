import pytest

from renamer.localpath import types, error


def test_filename():
    name = '/some/path/Some.Show.S01E05.FOO.BAR.ext'
    test = types.LocalPath(name)
    assert test.dirName == '/some/path'
    assert test.curFileName == 'Some.Show.S01E05.FOO.BAR.ext'
    assert test.fileNameExt == '.ext'


def test_samefile_error():
    name = '/some/path/Some.Show.S01E05.FOO.BAR.ext'
    test = types.LocalPath(name)
    test.newFileName = 'Some.Show.S01E05.FOO.BAR'
    with pytest.raises(error.SameFileError):
        test.rename()
