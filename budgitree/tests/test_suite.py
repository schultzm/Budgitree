import unittest
from ..tests.budgitree_test import TreeTestCasePass


def suite():
    """
    This is the test suite.
    """
    suite = unittest.TestSuite()
    suite.addTest(TreeTestCasePass('ete_print_tree'))
    suite.addTest(TreeTestCasePass('ete_collapse_polytomies'))
    suite.addTest(TreeTestCasePass('biophylo_collapse_branches'))
    suite.addTest(TreeTestCasePass('biophylo_print_formatted_bls'))
    return suite
