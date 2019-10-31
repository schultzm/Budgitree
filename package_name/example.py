"""
An example python file
"""

import pandas


def hello(name):
    """
    Function returns Hello Name string.
    """
    return f"Hello {name}!"


def add_sample(filename):
    """
    Function reads file to pandas.DataFrame, adds a row, and saves it back to file
    """
    tab = pandas.read_csv(filename)
    tab = tab.append(
        pandas.Series({"ID": "sample3", "FILEPATH": "/path/to/sample3.txt"}),
        ignore_index=True,
    )
    tab.to_csv(filename, index=False)
