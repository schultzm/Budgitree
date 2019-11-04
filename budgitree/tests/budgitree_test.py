"""
Unit Tests.
"""

import unittest
from pathlib import Path
from .. import __parent_dir__, __test_tree__
import pkg_resources
from ete3 import Tree


class TreeTestCasePass(unittest.TestCase):
    def setUp(self):
        self.tree = Tree(pkg_resources.resource_filename(__parent_dir__, __test_tree__))

    def ete_print_tree(self):
        self.assertEqual(self.tree.write(), '(XXYY-143_1:0.067295,((XXYY-39_1:0.04314,(XXYY-278_1:0.029035,XXYY-307_1:0.038563,XXYY-4_1:0.039559)0.14:0.001279)0.76:0.001489,((XXYY-64_1:0.017393,(XXYY-144_1:0.036755,XXYY-88_1:0.032626)0.99:0.003955)0.71:0.001156,XXYY-45_1:0.027032)0.87:0.002729)0.98:0.00694);')

    def ete_collapse_polytomies(self):
        self.tree.resolve_polytomy(recursive=True)
        self.assertEqual(self.tree.write(), '(XXYY-143_1:0.067295,((XXYY-39_1:0.04314,((XXYY-307_1:0.038563,XXYY-4_1:0.039559)0:0,XXYY-278_1:0.029035)0.14:0.001279)0.76:0.001489,((XXYY-64_1:0.017393,(XXYY-144_1:0.036755,XXYY-88_1:0.032626)0.99:0.003955)0.71:0.001156,XXYY-45_1:0.027032)0.87:0.002729)0.98:0.00694);')

    def biophylo_collapse_branches(self):
        from Bio import Phylo
        from io import StringIO
        tree = Phylo.read(StringIO(self.tree.write(format = 0)), "newick")
        tree.collapse_all(lambda c: c.confidence is not None and
                          c.confidence < 0.95)
        self.assertEqual(tree.format('newick'), '(XXYY-143_1:0.06729,(XXYY-39_1:0.04463,XXYY-45_1:0.02976,XXYY-278_1:0.03180,XXYY-307_1:0.04133,XXYY-4_1:0.04233,XXYY-64_1:0.02128,(XXYY-144_1:0.03676,XXYY-88_1:0.03263)0.99:0.00784)0.98:0.00694):0.00000;\n')

    def biophylo_print_formatted_bls(self):
        from Bio.Phylo.NewickIO import Writer
        from Bio import Phylo
        from io import StringIO
        tree = Phylo.read(StringIO(self.tree.write(format = 0)), "newick")
        trees = Writer([tree]).to_strings(format_branch_length=f"%1.10f")
        tree = [tree for tree in trees][0]
        self.assertEqual(tree, '(XXYY-143_1:0.0672950000,((XXYY-39_1:0.0431400000,(XXYY-278_1:0.0290350000,XXYY-307_1:0.0385630000,XXYY-4_1:0.0395590000)0.14:0.0012790000)0.76:0.0014890000,((XXYY-64_1:0.0173930000,(XXYY-144_1:0.0367550000,XXYY-88_1:0.0326260000)0.99:0.0039550000)0.71:0.0011560000,XXYY-45_1:0.0270320000)0.87:0.0027290000)0.98:0.0069400000):0.0000000000;')

