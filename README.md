# CS-182-final-project

### Rachel Gologorsky & Megan Ross

# DONE
- Parser (Rachel)

# TODO

- Pre-Req Dictionary (Megan)
- Add normalized Q-Score and Workload columns (Megan)
- Add ES153/Physics 123 (they fulfill breadth)
- Optional, way later: interactive user weight input parser (Megan)

- greedy local search (Rachel)
- simulated annealing (Rachel)

# Files

## printing: 
Contains pretty printing functions (e.g. print out assignment)

## cost_dicts: 
Dictionary of individual and pairwise costs

## branch_and_bound:
Contains cost function. TO DO: if assignment doesn't satisfy concentration requirements, return MAX_COST.

# Notes

Assignment = tuple of courses to take each semester, e.g.
asignment = (["cs50", "math21a"], ["cs51, math21b"], ...)

We map over the assignment to get semesters, and map over
semesters to get the courses per each semester.

Individual cost of a class = "workload" of taking the class.
Pair cost[class1][class2] = cost of taking class2 given we took class1 in the past. Ex: pair_costs["cs50]["cs51"] = cost of taking cs51 given we already took cs50 = negative since it reduces the "workload" burden.

Computing pair costs: for each class, go through the future classes and
apply the cost for having taken the sequence class -> future class.
