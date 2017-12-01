# CS-182-final-project

### Rachel Gologorsky & Megan Ross

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

Note we map over the assignment to get semesters, and map over
#semesters to get the courses per each semester.

individual cost of a class = cost ("workload") of taking the class
pair cost is the cost of taking class2 given we took class1 in the past.
so pair_costs["cs50]["cs51"] = cost of taking cs51 given we already took cs50

computing the pair costs: for each class, go through the future classes and
apply the cost for having taken the sequence class -> future class.
