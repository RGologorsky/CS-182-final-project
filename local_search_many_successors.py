from random         import randint, choice
from printing       import *
from helpers        import *
from constants      import *
from cost_functions import *
from cost_dicts     import *
from copy           import deepcopy
from local_search_restricted_successors import general_hill_climbing

# ASSIGNMENT = list of 8 semesters; each semester is a list of up to 4 classes
# SUCCESSOR = 1 course ADDED, MUTATED, or DELETED from the ASSIGNMENT

# ASSIGNMENT = list of 8 semesters; each semester is a list of up to 4 classes
# SUCCESSOR = 1 course ADDED, MUTATED, or DELETED from the ASSIGNMENT

# ASSIGNMENT: 8 semesters, each semester has <=4 classes. for each semester:
# ~25 add options, ~4 delete options, 20x4 = 80 mutate options => 1000 successors


# returns the greedy - lowest cost - successor state.
def get_greedy_successor2(assignment, weights):

    min_cost = get_cost(assignment, weights)
    best_successor = assignment

    for semester_index in xrange(8):
            # successors: (0) add, (1) delete course from semester
            successor0, cost0 = get_successor_type2(assignment, weights, semester_index, 0)
            successor1, cost1 = get_successor_type2(assignment, weights, semester_index, 1)
            successor2, cost2 = get_successor_type2(assignment, weights, semester_index, 2)

            if min(cost0, cost1, cost2) <= min_cost:
                if cost0 < cost1 and cost0 < cost2:
                    best_successor, min_cost = (successor0, cost0)
                elif cost1 < cost0 and cost1 < cost2:
                    best_successor, min_cost = (successor1, cost1)
                else:
                    best_successor, min_cost = (successor2, cost2)

    return (best_successor, min_cost)

# returns lowest cost successor state of given action - add, mutate, delete
def get_successor_type2(assignment, weights, semester_index, change_type=0):

    #  add course (type 0), delete course (type 1), muate course (type 2)

    if change_type == 0: # adding a course
        if len(assignment[semester_index]) == 4: # can't add if taking 4 courses
            return (None, float("inf"))

        possible_courses = new_course_domain(semester_index, assignment)
        possible_assignments = map(lambda x: add_to_assignment(assignment, semester_index, x), possible_courses)
        
        if len(possible_assignments) == 0:
            return (None, float("inf"))
        
        assignment_costs = map(lambda x: (x, get_cost(x, weights)), possible_assignments)
        return min(assignment_costs, key = lambda (x,c): c)

    if change_type == 1 or change_type == 2: 
        if len(assignment[semester_index]) == 0: # can't mutate/delete if none
            return (None, float("inf"))

        # possibilities for the course index to delete.
        possible_course_indices = range(len(assignment[semester_index]))
        possible_assignments = map(lambda x: del_to_assignment(assignment, semester_index, x), possible_course_indices)
        
        if len(possible_assignments) == 0:
            return (None, float("inf"))

        if change_type == 1: # if just delete, we are done.
            assignment_costs = map(lambda x: (x, get_cost(x, weights)), possible_assignments)
            return min(assignment_costs, key = lambda (x,c): c)

        # for mutation, we now check best add state.
        possible_add_assignment_costs = map(lambda a: get_successor_type2(a, weights, semester_index, 0), possible_assignments)
        return min(possible_add_assignment_costs, key = lambda (x,c): c)


# we allow sideways movements to overcome plateux
def sideways_hill_climbing2(weights, MAX_NUM_SIDEWAYS = 100, assignment = None):
    return general_hill_climbing(get_greedy_successor2, weights, MAX_NUM_SIDEWAYS, assignment)
  
# no sideway steps allowed
def naive_hill_climbing2(weights, assignment = None):
    return sideways_hill_climbing(weights, MAX_NUM_SIDEWAYS = 0, assignment = None)
