"""Tests for remote URL detection and normalization."""

from harness_eval.remote import is_remote, normalize_url


def test_https_url_is_remote():
    assert is_remote("https://github.com/user/repo")


def test_git_ssh_is_remote():
    assert is_remote("git@github.com:user/repo.git")


def test_github_shorthand_is_remote():
    assert is_remote("user/repo")


def test_local_path_not_remote():
    assert not is_remote(".")
    assert not is_remote("/tmp/my-project")
    assert not is_remote("./relative/path")


def test_normalize_shorthand():
    assert normalize_url("user/repo") == "https://github.com/user/repo.git"


def test_normalize_full_url_unchanged():
    url = "https://github.com/user/repo.git"
    assert normalize_url(url) == url
