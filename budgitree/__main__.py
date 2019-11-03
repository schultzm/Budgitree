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
    parser.add_argument('tree', help='Input newick tree')
    parser.add_argument('-p', '--precision', help = '''Branch length precision
                                                       (i.e., number of decimal places to
                                                       print).''',
                        default = 6,
                        type = int)
    parser.add_argument('-b', '--dont_bifurcate_polytomies',
                        help = 'Switch off conversion of node polytomies to bifurcating',
                        default = False,
                        action='store_true')
    parser.add_argument('-c', '--collapse',
                        help = 'Collapse nodes with support values less than this.',
                        default = '0.00',
                        type = float)
    args = parser.parse_args()
    from pathlib import Path
    if not Path(args.tree).exists():
        import sys
        sys.exit(f'File \'{Path(args.tree)}\' not found.  Exiting.')
    from ete3 import Tree
    t = Tree(args.tree)
    if not args.dont_bifurcate_polytomies:
        t.resolve_polytomy(recursive=True)

    from Bio import Phylo
    from Bio.Phylo.NewickIO import Writer
    from io import StringIO
    tree = Phylo.read(StringIO(t.write(format = 0)), 'newick')
    tree.collapse_all(lambda c: c.confidence is not None and
                      c.confidence < args.collapse)
    trees = Writer([tree]).to_strings(format_branch_length=f"%1.{args.precision}f")
    for tre in trees:
        print(tre)


if __name__ == '__main__':
    main()
