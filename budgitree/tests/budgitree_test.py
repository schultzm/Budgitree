"""
Unit Tests.
"""

import unittest
from pathlib import Path
from .. import __parent_dir__, __test_tree__
import pkg_resources
from ete3 import Tree


class TreeTestCasePass(unittest.TestCase):
    maxDiff = None
    def setUp(self):
        print("Using ete3.Tree(example.tree)")
        self.tree = Tree(pkg_resources.resource_filename(__parent_dir__, __test_tree__))

    def ete_print_tree(self):
        print("Check that the tree can be printed, to verify approximately functional ete3")
        self.assertEqual(self.tree.write(), '(XXYY-143_1:0.067294999999999993712,((XXYY-39_1:0.043139999999999997793,(XXYY-278_1:0.02903499999999999831,XXYY-307_1:0.038563000000000000056,XXYY-4_1:0.039558999999999996944)0.14000000000000001332:0.001278999999999999972)0.76000000000000000888:0.0014890000000000000891,((XXYY-64_1:0.017392999999999998739,(XXYY-144_1:0.036755000000000002947,XXYY-88_1:0.032626000000000002221)0.98999999999999999112:0.0039550000000000001821)0.70999999999999996447:0.0011559999999999999096,XXYY-45_1:0.027032000000000000473)0.86999999999999999556:0.0027290000000000000889)0.97999999999999998224:0.0069399999999999999883);')

    def ete_collapse_polytomies(self):
        self.tree.resolve_polytomy(recursive=True)
        print("Print tree after resolving polytomies with ete3")
        self.assertEqual(self.tree.write(), '(XXYY-143_1:0.067294999999999993712,((XXYY-39_1:0.043139999999999997793,((XXYY-307_1:0.038563000000000000056,XXYY-4_1:0.039558999999999996944)0:0,XXYY-278_1:0.02903499999999999831)0.14000000000000001332:0.001278999999999999972)0.76000000000000000888:0.0014890000000000000891,((XXYY-64_1:0.017392999999999998739,(XXYY-144_1:0.036755000000000002947,XXYY-88_1:0.032626000000000002221)0.98999999999999999112:0.0039550000000000001821)0.70999999999999996447:0.0011559999999999999096,XXYY-45_1:0.027032000000000000473)0.86999999999999999556:0.0027290000000000000889)0.97999999999999998224:0.0069399999999999999883);')

    def biophylo_collapse_branches(self):
        print("Check nodes with low support (<0.98) were collapsed using BioPhylo as intended.")
        from Bio import Phylo
        from io import StringIO
        tree = Phylo.read(StringIO(self.tree.write(format = 0)), "newick")
        tree.collapse_all(lambda c: c.confidence is not None and
                          c.confidence < 0.95)
        self.assertEqual(tree.format('newick'), '(XXYY-143_1:0.06729,(XXYY-39_1:0.04463,XXYY-45_1:0.02976,XXYY-278_1:0.03180,XXYY-307_1:0.04133,XXYY-4_1:0.04233,XXYY-64_1:0.02128,(XXYY-144_1:0.03676,XXYY-88_1:0.03263)0.99:0.00784)0.98:0.00694):0.00000;\n')

    def biophylo_print_formatted_bls(self):
        print("Check that branch lengths can be reformatted using BioPhylo (10 decimal places).")
        from Bio.Phylo.NewickIO import Writer
        from Bio import Phylo
        from io import StringIO
        tree = Phylo.read(StringIO(self.tree.write(format = 0)), "newick")
        trees = Writer([tree]).to_strings(format_branch_length=f"%1.10f")
        tree = [tree for tree in trees][0]
        self.assertEqual(tree, '(XXYY-143_1:0.0672950000,((XXYY-39_1:0.0431400000,(XXYY-278_1:0.0290350000,XXYY-307_1:0.0385630000,XXYY-4_1:0.0395590000)0.14:0.0012790000)0.76:0.0014890000,((XXYY-64_1:0.0173930000,(XXYY-144_1:0.0367550000,XXYY-88_1:0.0326260000)0.99:0.0039550000)0.71:0.0011560000,XXYY-45_1:0.0270320000)0.87:0.0027290000)0.98:0.0069400000):0.0000000000;')

