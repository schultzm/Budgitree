"""
An example test file
"""

import pandas
from package_name import example


def test_hello():
    """
    Example simple test looking at the return of a function in package_name
    """
    greeting = example.hello("Trillian")
    assert greeting == "Hello Trillian!"


def test_use_tmpdir(tmpdata):
    """
    Checking the outcome of a function that does something to a file and
    has some external output.
    This uses the tmpdata fixture created in the conftest.py
    """
    data_file = tmpdata / "example_data.csv"
    example.add_sample(data_file)
    output = pandas.Series(
        {"ID": "sample3", "FILEPATH": "/path/to/sample3.txt"}, name=2
    )
    tab = pandas.read_csv(data_file)
    pandas.testing.assert_series_equal(output, tab.iloc[2])
