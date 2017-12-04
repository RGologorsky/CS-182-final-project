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

# Problems we Faced
- Features Scaling
- Local search plateux

# Tests 

sideways moves vs. no sideways moves:
    - difference in cost found
    - diference in num. iter. needed

# Files

## constants.py - contains the course dictionary, "courses." 

We gain efficiency by not having to preprocess the CSV each time we run the program; the course dictionary is computed only once and then is a global constant imported into files.

## cost_functions.py - contains component cost functions corresponding to features. Computes the cost of an assignment over the following features:

- pre-req cost: get_pre_req_cost sums the total number of pre-req violations.
- workload cost: get_workload_cost sums the total workload. Worklad is scaled to the same range 0-10.
- qscore cost: get_qscore_cost sums (5 - qscore) over the courses in the assignment. Note qscore = 5 => lowest cost, qscore = 0 => highest cost.
- enrollment_cost: sums enrollment numbers of the courses. Enrollment numbers scaled to be in the same range and hence comparable to other feature costs.

## reqs.py - costs for not fulfilling concentration requirements.
- math cost = #classes needed to fullfill math requirement.
- sofware cost
- theory cost
- technical elective cost
- breadth cost

## csv_parser.py - parses CSV into dictionary, which is saved as a global constant.

- parsed dictionary (key, value) pairs are:
    - key is the course 
    - value is a course_info dictionary containing the course information.
- we convert start and end times to miliary time, to detect course overlap easier
- we include prereq - MEGAN FILL IN DETAILS

## helpers.py - contains useful helper functions

- coin_flip(p) returns True with probability p
- overlap(course1, course2) returns whether course1 and course2 overlap in time
- no_overlap(course, assigned_courses) returns whether the course is time-compatable with the other courses in assigned_courses
- new_course_domain(semester, flat_courses) returns a potential domain of courses not in time conflict in a given semester. Used to generate successors.

## local_search.py - local search heuristics
- hill_climbing
- sideways hill_climbing
- get_greedy_successor(assignment) returns the lowest-cost successor state. On the order of 10^3 successor states per assignment.

## main.py - runs code

## printing.py: 
Contains pretty printing functions (e.g. print out assignment)

## branch_and_bound:
Contains cost function. TO DO: if assignment doesn't satisfy concentration requirements, return MAX_COST.

# Notes

Assignment = tuple of courses to take each semester, e.g.
asignment = (["cs50", "math21a"], ["cs51, math21b"], ...)

We map over the assignment to get semesters, and map over
semesters to get the courses per each semester.
