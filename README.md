# NUSInternshipReports

This repository contains reports about my ongoing research and notes on research papers I have been reading in my ongoing internship with Prof. Kuldeep Meel and his PhD student Yash Pote at NUS School of Computing.

My work so far has been revolving around three tasks:
1. Theoretically bounding the probabilistic search range for the number of hashes required after an initial call named RoughMC and verified reduced experimental running time as well as reduced theoretical time complexity.
2. Analysing experimentally and theoretically the effect of using equally sparse hashing matrices instead of sampling matrices from the Rennes family of hashing matrices described [here](https://arxiv.org/pdf/2004.14692.pdf).
3. Attempting to parametrise an edge isoperimetric inequality derived by Rashtchian [here](https://arxiv.org/pdf/1909.10435.pdf) for powers of the hypercube using treewidth of primal and dual graphs of the CNF formula corresponding to the hypercube.

If successful, these tasks will help improve the probabilistic bounds and/or time complexity of [ApproxMC](https://github.com/meelgroup/approxmc): a sparse XOR-hashing based approximate model counter.
