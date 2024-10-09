from ...constants import *  # NOQA
from . import cmd, generate_archiver_tests, RK_ENCRYPTION

pytest_generate_tests = lambda metafunc: generate_archiver_tests(metafunc, kinds="local")  # NOQA


def test_tag_set(archivers, request):
    archiver = request.getfixturevalue(archivers)
    cmd(archiver, "repo-create", RK_ENCRYPTION)
    cmd(archiver, "create", "archive", archiver.input_path)
    output = cmd(archiver, "tag", "-a", "archive", "--set", "aa")
    assert "tags: aa." in output
    output = cmd(archiver, "tag", "-a", "archive", "--set", "bb")
    assert "tags: bb." in output
    output = cmd(archiver, "tag", "-a", "archive", "--set", "bb", "--set", "aa")
    assert "tags: aa,bb." in output  # sorted!
    output = cmd(archiver, "tag", "-a", "archive", "--set", "")
    assert "tags: ." in output  # no tags!


def test_tag_add_remove(archivers, request):
    archiver = request.getfixturevalue(archivers)
    cmd(archiver, "repo-create", RK_ENCRYPTION)
    cmd(archiver, "create", "archive", archiver.input_path)
    output = cmd(archiver, "tag", "-a", "archive", "--add", "aa")
    assert "tags: aa." in output
    output = cmd(archiver, "tag", "-a", "archive", "--add", "bb")
    assert "tags: aa,bb." in output
    output = cmd(archiver, "tag", "-a", "archive", "--remove", "aa")
    assert "tags: bb." in output
    output = cmd(archiver, "tag", "-a", "archive", "--remove", "bb")
    assert "tags: ." in output