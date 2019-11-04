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
            bifurcating) and or change the formatting of branch lengths.""")
    subparser_args1 = argparse.ArgumentParser(add_help=False)
    subparser_args1.add_argument("tree", help="Input newick tree")
    subparser_args1.add_argument("-p", "--precision", help = """Branch length precision
                                                       (i.e., number of decimal places to
                                                       print).""",
                        default = 6,
                        type = int)
    subparser_args1.add_argument("-b", "--dont_bifurcate_polytomies",
                        help = "Switch off conversion of node polytomies to bifurcating",
                        default = False,
                        action="store_true")
    subparser_args1.add_argument("-c", "--collapse",
                        help = "Collapse nodes with support values less than this.",
                        default = "0.00",
                        type = float)
    subparser_modules = parser.add_subparsers(
        title="Sub-commands help", help="", metavar="", dest="subparser_name")
    subparser_modules.add_parser(
        "smuggle", help="Smuggle the budgies.", description="Process the tree.",
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
    elif args.subparser_name == 'version':
        from budgitree import __version__ as version
        print(version)
    elif args.subparser_name == 'test':
        import unittest
        from .tests.test_suite import suite
        runner = unittest.TextTestRunner(verbosity=2)
        runner.run(suite())

    elif args.subparser_name == 'smuggle':
        from pathlib import Path
        if not Path(args.tree).exists():
            import sys
            sys.exit(f"File '{Path(args.tree).absolute()}' not found.  Exiting.")

        from ete3 import Tree
        t = Tree(args.tree)
        if not args.dont_bifurcate_polytomies:
            t.resolve_polytomy(recursive=True)

        from Bio import Phylo
        from Bio.Phylo.NewickIO import Writer
        from io import StringIO
        tree = Phylo.read(StringIO(t.write(format = 0)), "newick")
        tree.collapse_all(lambda c: c.confidence is not None and
                          c.confidence < args.collapse)
        trees = Writer([tree]).to_strings(format_branch_length=f"%1.{args.precision}f")

        for tre in trees:
            print(tre)


if __name__ == "__main__":
    main()
