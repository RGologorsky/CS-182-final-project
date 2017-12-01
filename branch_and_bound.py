from printing import *
from cost_dicts import *

# Assignment = tuple of courses to take each semester, e.g.
# asignment = (["cs50", "math21a"], ["cs51, math21b"], ...)

# Note we map over the assignment to get semesters, and map over
# semesters to get the courses per each semester.

# individual cost of a class = cost ("workload") of taking the class
# pair cost is the cost of taking class2 given we took class1 in the past.
# so pair_costs["cs50]["cs51"] = cost of taking cs51 given we already took cs50


# computing the pair costs: for each class, go through the future classes and
# apply the cost for having taken the sequence class -> future class.

def lookup_pair_cost(course1, course2):
    if course1 in pair_costs and course2 in pair_costs[course1]:
        pair_costs[course1][course2]
    return 0

# this is O(n^2) in n = #classes = 32, so very fast.

def cost(assignment):
    # add the individual course costs (workload)
    total_cost = sum(map(lambda semester: \
                        sum(map(lambda course: indiv_costs[course], semester)),
                    assignment))
    
    num_semesters = len(assignment)

    for i in xrange(num_semesters):
        courses = assignment[i] # = list of courses to take in semester i
        future_semesters = assignment[i+1:]

        for course1 in courses:
            
            # go through future classes, apply cost of course1 -> course2
            pairs = map(lambda semester: sum(\
                        map(lambda course2: lookup_pair_cost(course1,course2), 
                            semester)),
                    future_semesters)
        
            total_cost += sum(pairs)

    return total_cost
