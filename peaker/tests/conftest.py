"""Fixtures for tests."""

import pytest


@pytest.fixture(scope="session")
def tmpdir(tmp_path_factory):
    return tmp_path_factory.mktemp("tmpdir")

