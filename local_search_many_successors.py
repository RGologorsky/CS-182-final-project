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
def get_best_add_successor(assignment, weights, add_index):
    if len(assignment[add_index]) == 4: # can't add if taking 4 courses
        return (None, float("inf"))

    possible_adds = new_course_domain(add_index, assignment)
    new_assignments = map(lambda x: add_to_assignment(assignment, add_index, x), possible_adds)

    if len(new_assignments) == 0:
        return (None, float("inf"))

    costs = map(lambda x: (x, get_cost(x, weights)), new_assignments)
    return min(costs, key = lambda (x,c): c)

def get_best_del_successor(assignment, weights, del_index):
    if len(assignment[del_index]) == 0: # can't del if taking 0 courses
        return (None, float("inf"))

    possible_dels = range(len(assignment[del_index]))
    new_assignments = map(lambda x: del_to_assignment(assignment, del_index, x), possible_dels)

    if len(new_assignments) == 0:
        return (None, float("inf"))

    assignment_costs = map(lambda x: (x, get_cost(x, weights)), new_assignments)
    return min(assignment_costs, key = lambda (x,c): c)

# given a good add index anda  good delete index.
def get_best_mut_successor(assignment, weights, add_index, del_index):
    # if full at semester add index or empty at delete index, 
    # simplifies to pure add/del. Else: first del, then add.

    possible_dels = range(len(assignment[del_index]))
    del_assignments = map(lambda x: del_to_assignment(assignment, del_index, x), possible_dels)

    if len(del_assignments) == 0:
        return (None, float("inf"))  

    curr_best_cost = float("inf")
    curr_best_mut = None
    for  del_assignment in del_assignments:
        possible_adds = new_course_domain(add_index, del_assignment)
        add_assignments = map(lambda x: add_to_assignment(del_assignment, add_index, x), possible_adds)
        for mut in add_assignments:
            mut_cost = get_cost(mut, weights)
            if mut_cost < curr_best_cost:
                curr_best_cost = mut_cost
                curr_best_mut  = mut
    return curr_best_mut, curr_best_cost



def get_greedy_successor2(assignment, weights):

    min_cost = get_cost(assignment, weights)
    best_successor = assignment

    # check mutation: add from any, delete from any (including just add/del)
    for add_index in xrange(-1,8):
        for del_index in xrange(-1,8):
            
            if add_index == -1 and del_index == -1:
                cost = min_cost
            
            elif add_index == -1 or len(assignment[add_index]) == 4:
                successor, cost = \
                    get_best_del_successor(assignment, weights, del_index)
            
            elif del_index == -1 or len(assignment[del_index]) == 0:
                successor, cost = \
                     get_best_add_successor(assignment, weights, add_index)
            
            else:
                successor, cost = \
                    get_best_mut_successor(assignment, weights, add_index, del_index)

            if cost < min_cost:
                best_successor, min_cost = (successor, cost)

    return (best_successor, min_cost)

# we allow sideways movements to overcome plateux
def sideways_hill_climbing2(weights, MAX_NUM_SIDEWAYS = 100, assignment = None):
    return general_hill_climbing(get_greedy_successor2, weights, MAX_NUM_SIDEWAYS, assignment)

# no sideway steps allowed
def naive_hill_climbing2(weights, assignment = None):
    return sideways_hill_climbing2(weights, 0, assignment)
