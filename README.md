# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

Writing an algorithm for the Udacity AI Nanodegree to solve sudoku. The code employs 3 strategies: elimination, only choice, naked twins, and search.

Elimination: If there are solved boxes, find their peers and remove the solved values from possible choices.

Only Choice: Find which possible solution is unique to a box in each unit (e.g., 9 boxes in a column or row or square). If a unique possilbe solution is found, assign that value to the box.

Naked Twins: Find a pair of boxes (twins) that share the same two possible solutions in a unit. With these two boxes take up the two possible solutions, remove the two possible solutions from all other boxes that are in the same space with the twins.

Search: Go through the possible solutions one by one until the sudoku is solved.

The alogrithm applies elimination, only choice and naked twins repeatedly until it is stalled. When it is stalled, utilize the search strategy to exmaine which path may lead to eventual solution.

Note. Beside solving standard sudoku, the algorithm is also capable of solving diagonal sudoku which requires the boxes in the the main diagonal to be unique as well.