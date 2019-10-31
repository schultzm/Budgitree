#!/usr/bin/env python3

"""
Given a newick tree, use this program to resolve polytomies (convert to bifurcating) and
or change the formatting of branch lengths.  This program was written to convert FastTree
trees to strictly bifurcating, as well as control the formatting of branch lengths
(specifically to prevent the use of scientific notation in branch lengths).
"""







def main():
    """Perform the main routine."""
    import argparse
    parser = argparse.ArgumentParser(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            description="""
            Given a newick tree, use this program to resolve polytomies (convert to bifurcating) and
    or change the formatting of branch lengths.  This program was written to convert FastTree
    trees to strictly bifurcating, as well as control the formatting of branch lengths
    (specifically to prevent the use of scientific notation in branch lengths).
    """)
    parser.add_argument('tree', help='Input newick tree')
    parser.add_argument('-p', '--precision', help = '''Branch length precision
                                                       (i.e., number of decimal places to
                                                       print).''',
                        default = 6,
                        type = int)
    parser.add_argument('-b', '--dont_bifurcate_polytomies',
                        help = 'Swtich off conversion of node polytomies to bifurcating',
                        default = True,
                        action='store_false')
    args = parser.parse_args()
    
    from ete3 import Tree
    t = Tree(args.tree)
    if not args.dont_bifurcate_polytomies:
        t.resolve_polytomy(recursive=True)

    from Bio import Phylo
    from Bio.Phylo.NewickIO import Writer
    from io import StringIO
    tree = Phylo.read(StringIO(t.write(format = 0)), 'newick')
    trees = Writer([tree]).to_strings(format_branch_length=f"%1.{args.precision}f")
    for tre in trees:
        print(tre)


if __name__ == '__main__':
    main()
