from random         import randint, choice
from printing       import *
from helpers        import *
from constants      import *
from cost_functions import *
from cost_dicts     import *
from copy           import deepcopy

# ASSIGNMENT = list of 8 semesters; each semester is a list of up to 4 classes
# SUCCESSOR = 1 course ADDED, MUTATED, or DELETED from the ASSIGNMENT

# ASSIGNMENT: 8 semesters, each semester has <=4 classes, ~20 options per class
# ~ 1100 SUCCESSORS: 8 semesters, each semester <= 4 classes, for each class:
# ~25 add options, ~4 delete options => 30 choices
# ==> 8 * 30 ~ 240 SUCCESSORS

# returns the greedy successor state.
def get_greedy_successor(assignment):

    min_cost = get_cost(assignment)

    best_successor = assignment

    for semester_index in xrange(8):
            # successors: (0) add, (1) delete course from semester
            successor0 = get_successor_type(assignment, semester_index, 0)
            successor1 = get_successor_type(assignment, semester_index, 1)

            cost0, cost1 = get_cost(successor0), get_cost(successor1)

            # motivates adding over deleting
            if successor0 < successor1:
                successor = successor0
                successor_cost = cost0
            else:
                successor = successor1
                successor_cost = cost1

            if successor_cost <= min_cost:
                best_successor = successor
                min_cost = successor_cost

    return (best_successor, min_cost)

# A state is a list of value indices.
# Randomly picks value indices until the weight limit is reached

def get_successor_type(assignment, semester_index, change_type=0):

    #  add course (type 0), delete course (type 1)

    # can't delete if no courses in semester
    if change_type == 1 and len(assignment[semester_index]) == 0:
        return assignment

    # can't add if alreadying taking 4 courses
    if change_type == 0 and len(assignment[semester_index]) == 4:
            return assignment

    if change_type == 0: # adding a course
        possible_courses = new_course_domain(semester_index, assignment)
        possible_assignments = map(lambda x: add_assignment(assignment, semester_index, x), possible_courses)
        return min(possible_assignments, key = lambda a: get_cost(a))

    # possibilities for the course index to delete.
    possible_course_indices = range(len(assignment[semester_index]))
    possible_assignments = map(lambda x: del_assignment(assignment, semester_index, x), possible_course_indices)
    return min(possible_assignments, key = lambda a: get_cost(a))
        

def sideways_hill_climbing(assignment, MAX_NUM_SIDEWAYS = 100):
    num_iter     = 0
    num_sideways = 0
    num_plateux  = 0
    total_sideways_steps = 0

    # LATER TESTING & GRAPHS
    initial_cost = get_cost(assignment)
    curr_cost = initial_cost

    trace = [assignment]
    cost_trace = [initial_cost]

    def get_avg_num_sideways():
        return 0 if num_plateux == 0 else (total_sideways_steps * 1.0)/num_plateux


    while True:
        successor, successor_cost = get_greedy_successor(assignment)

        trace.append(successor)
        cost_trace.append(successor_cost)

        # assignment is local maximum, not a shoulder
        if successor == assignment:
            return (assignment, initial_cost, curr_cost, MAX_NUM_SIDEWAYS, \
                        num_iter, num_plateux, get_avg_num_sideways())

        # in a shoulder, check if we can go sideways
        if successor_cost == curr_cost:
            if num_sideways < MAX_NUM_SIDEWAYS:
                assignment = successor
                num_iter += 1
                num_sideways += 1
            else: # no escaping the plateux
                return (assignment, initial_cost, curr_cost, MAX_NUM_SIDEWAYS, \
                            num_iter, num_plateux, get_avg_num_sideways())

        # all good! hill-climb to neighbor
        else:
            assignment = successor
            curr_cost = successor_cost
            num_iter += 1

            # check if just overcame a plateux, reset num sideways
            if num_sideways > 0:
                num_plateux += 1
                total_sideways_steps += num_sideways
                num_sideways = 0


def naive_hill_climbing(assignment):
    return sideways_hill_climbing(assignment, MAX_NUM_SIDEWAYS = 0)
