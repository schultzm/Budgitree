# Budgitree

[![CircleCI](https://circleci.com/gh/MDU-PHL/mdu_py_dev_repo_template.svg?style=svg&circle-token=b62526fbb9651e6217c587331b9950a6ae62de42)](https://circleci.com/gh/MDU-PHL/mdu_py_dev_repo_template)

## Why use this program?

Let's say you have just obtained your phylogenetic tree from FastTree.
This tree will likely contain polytomies, and branch lengths that are so
small that they will be represented in exponential notation.
Some programs will not accept trees with these two features (e.g., ClusterPicker).
You could remove the polytomies with the `ape` package in `R`.  But how do you
print the tree to standard out in standard float format?  You could submit
an issue to the developers of your target program and hope they respond with a fix.
Both of these options may delay your workflow.  This program provides a python3 solution
to your problems.  Given a phylogenetic tree in newick format, `budgitree`
provides an easy way to print your tree to `stdout` with:

1. Polytomies resolved (i.e., tree converted to strictly bifurcating) and/or
2. Exponential notation removed (i.e., branch lengths in float format with user-specified number of decimal places






![budgitree](https://static3.bigstockphoto.com/1/6/5/large1500/56146028.jpg)
