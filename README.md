# Budgitree

[![CircleCI](https://circleci.com/gh/schultzm/Budgitree/tree/master.svg?style=svg&circle-token=23da01746bede233a29934b06e63a5cf841e27b2)](https://circleci.com/gh/schultzm/Budgitree/tree/master)

## Why use this program?

Let's say you have just obtained your phylogenetic tree from FastTree.
This tree will likely contain polytomies, and branch lengths that are so
small that they will be represented in exponential notation.
Some programs will not accept trees with these two features (e.g., ClusterPicker).
You could remove the polytomies with the `ape` package in `R`.  But how do you
print the tree to standard out with the branch lengths in standard float format?  You could submit
an issue to the developers of your target program and hope they respond with a fix.
Both of these options may delay your workflow.  This program provides a python3 solution
to your problems.  Given a phylogenetic tree in newick format, `budgitree`
provides an easy way to print your tree to `stdout` with:

1. Polytomies resolved (i.e., tree converted to strictly bifurcating) and/or
2. Exponential notation removed (i.e., branch lengths in float format with user-specified number of decimal places)
3. Collapse branches with support values less than the specified cutoff (default is do nothing)

## Usage

### Get help

```{bash}
$ budgitree
usage: budgitree [-h]  ...

Given a newick tree, use this program to resolve polytomies (convert to
bifurcating) and or change the formatting of branch lengths.

optional arguments:
  -h, --help  show this help message and exit

Sub-commands help:
  
    smuggle   Smuggle the budgies.
    version   Print version.
    test      Run test suite.
```

### Start smuggling

```{bash}
$ budgitree smuggle -h
usage: budgitree smuggle [-h] [-p PRECISION] [-b] [-c COLLAPSE] tree

Process the tree.

positional arguments:
  tree                  Input newick tree

optional arguments:
  -h, --help            show this help message and exit
  -p PRECISION, --precision PRECISION
                        Branch length precision (i.e., number of decimal
                        places to print).
  -b, --dont_bifurcate_polytomies
                        Switch off conversion of node polytomies to
                        bifurcating
  -c COLLAPSE, --collapse COLLAPSE
                        Collapse nodes with support values less than this.
```

#### Collapse branches

Collapse branches with less than 0.5 support:

```{bash}
budgitree smuggle treefile.tre -c 0.50`
```

#### Print tree with branch supports to 20 decimal places (remove exponential notation):

```{bash}
budgitree smuggle treefile.tre -p 20
```

#### Stop removal of polytomies during run:

If for some reason you would like to retain the polytomies, switch the feature off:

```{bash}
budgitree smuggle treefile.tre -b
```

#### Combine the options

Remove polytomies, print branch lengths to 15 decimal places, collapse nodes <0.5:

```{bash}
budgitree smuggle treefile.tre -p 15 -c 0.5
```

## Installation

Using `pip`:

```{bash}
pip3 install budgitree
```

The development version:

```{bash}
pip3 install git+https://github.com/schultzm/Budgitree.git
```


## Testing

Run the test suite to check the software works as intended:

```{bash}
budgitree test
```

## Version

Print the version to stdout:

```{bash}
budgitree version
```

## Etymology

The budgerigar, or "budgie", is an Australian bird (_Melopsittacus undulatus_), keeping 
with an Australian theme after @tseemann.  The software sets digits on branches – if you
are imaginative, that kind of sounds like `budgit`.  `tree` is because it operates on
phylogenetic trees.  The `smuggle` feature of `budgitree` has to do with an Australian
joke involving budgies and swimwear.

![budgitree](https://www.hbw.com/sites/default/files/styles/ibc_1k/public/ibc/p/budgerigar_2015_bh_5d_miaboolya_with_les.jpg?itok=l2lThq-t)
