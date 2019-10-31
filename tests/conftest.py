"""
Example conftest.py

Here, I add a fixture that copies some data to a temp folder that
can then be accessed by other tests
"""

import pathlib
import shutil
import pkg_resources
import pytest


@pytest.fixture
def tmpdata(tmpdir_factory):
    """
    Creating a fixture that all tests can use with a temporary folder and
    with the package data
    """
    tmpdir = pathlib.Path(tmpdir_factory.mktemp("data"))
    datafile = pkg_resources.resource_filename("package_name", "data/example_data.csv")
    shutil.copy(datafile, tmpdir.absolute())
    return tmpdir
