#!/usr/bin/env python3

"""
Given a newick tree, use this program to resolve polytomies (convert to bifurcating) and
or change the formatting of branch lengths.  This program was written to convert FastTree
trees to strictly bifurcating, as well as control the formatting of branch lengths
(specifically to prevent the use of scientific notation in branch lengths).  Does not
support multiple branch support values on individual branches such as that which can
be output by IQ-Tree (e.g., 100/98).
"""

def main():
    """Perform the main routine."""
    import argparse
    parser = argparse.ArgumentParser(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            description="""
            Given a newick tree, use this program to resolve polytomies (convert to
            bifurcating), and/or change the precision of branch lengths,
            and/or collapse.""")
    subparser_args1 = argparse.ArgumentParser(add_help=False)
    subparser_args1.add_argument("tree", help="Input newick tree")
    subparser_args1.add_argument("-p", "--precision", help = """Branch length precision
                                                       (i.e., number of decimal places to
                                                       print).""",
                        default = None,
                        type = int)
    subparser_args1.add_argument("-b", "--dont_bifurcate_polytomies",
                        help = "Switch off conversion of node polytomies to bifurcating",
                        default = False,
                        action="store_true")
    subparser_args1.add_argument("-c", "--collapse",
                        help = "Collapse nodes with support values less than this.",
                        default = None,
                        type = float)
    subparser_modules = parser.add_subparsers(
        title="Sub-commands help", help="", metavar="", dest="subparser_name")
    subparser_modules.add_parser(
        "smuggle", help="Smuggle the budgie.", description="Process the tree.",
        parents=[subparser_args1])

    subparser_modules.add_parser(
        "version", help="Print version.", description="Print version.")
    subparser_modules.add_parser(
        "test", help="Run test suite.",
        description="Run test suite.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    args = parser.parse_args()

    if not args.subparser_name:
        parser.print_help()
    elif args.subparser_name == "version":
        from budgitree import __version__ as version
        print(version)
    elif args.subparser_name == "test":
        import unittest
        from .tests.test_suite import suite
        runner = unittest.TextTestRunner(verbosity=2)
        runner.run(suite())

    elif args.subparser_name == "smuggle":
        import sys
        from pathlib import Path
        # Check if file exists
        if not Path(args.tree).exists():
            sys.exit(f"File '{Path(args.tree).absolute()}' not found.  Exiting.")

        from Bio import Phylo
        from Bio.Phylo.NewickIO import Writer
        from io import StringIO
        # Read the tree
        tree = Phylo.read(args.tree, "newick")
        # Collapse the low-support nodes if requested
        if args.collapse is not None:
            print(f"Collapsing nodes with support < {args.collapse}.", file = sys.stderr)
            tree.collapse_all(lambda c: c.confidence is not None and
                              c.confidence < args.collapse)
        if not args.dont_bifurcate_polytomies:
            print("Removing polytomies.", file = sys.stderr)
            from ete3 import Tree
            t = Tree(tree.format("newick"))
            t.standardize()
            tree = Phylo.read(StringIO(t.write(format = 0)), "newick")
        # Polytomies created by collapsing nodes still need to be parseable.
        # Achieve this by increasing the recursion limit
        sys.setrecursionlimit(3000)
        # but don"t let it get too high (to prevent stack overflow)
        sys.setrecursionlimit(tree.count_terminals() * 2)
        trees = None
        if args.precision is not None:
            print(f"Reformatting branch lengths to {args.precision} decimal places.",
                  file = sys.stderr)
            trees = Writer([tree]). \
            to_strings(format_branch_length = f"%1.{args.precision}f")
        else:
            trees = Writer([tree]). \
            to_strings(format_branch_length = f"%g")
        # there is only one tree in trees, so:
        print(next(trees))

if __name__ == "__main__":
    main()
