from random         import randint, choice
from printing       import *
from helpers        import *
from constants      import *
from cost_functions import *
from cost_dicts     import *
from copy           import deepcopy

import time
# ASSIGNMENT = list of 8 semesters; each semester is a list of up to 4 classes
# SUCCESSOR = 1 course ADDED, MUTATED, or DELETED from the ASSIGNMENT

# ASSIGNMENT: 8 semesters, each semester has <=4 classes, ~20 options per class
# ~ 1100 SUCCESSORS: 8 semesters, each semester <= 4 classes, for each class:
# ~25 add options, ~4 delete options => 30 choices
# ==> 8 * 30 ~ 240 SUCCESSORS


# returns the greedy successor state.
def get_greedy_successor(assignment, weights):

    min_cost = get_cost(assignment, weights)
    best_successor = assignment

    for semester_index in xrange(8):
            # successors: (0) add, (1) delete course from semester
            successor0, cost0 = get_successor_type(assignment, weights, semester_index, 0)
            successor1, cost1 = get_successor_type(assignment, weights, semester_index, 1)

            if min(cost0, cost1) <= min_cost:
                if cost0 < cost1:
                    #print "adding back"
                    best_successor, min_cost = (successor0, cost0)

                else:
                    #print "choose to delete"
                    best_successor, min_cost = (successor1, cost1)
                    #print "s"

    # print "returning successor with length"
    # print len(get_flat_courses(best_successor))
    return (best_successor, min_cost)

# A state is a list of value indices.
# Randomly picks value indices until the weight limit is reached
def get_successor_type(assignment, weights, semester_index, change_type):

    #  add course (type 0), delete course (type 1)
    # print "my assignment has len: ", len(get_flat_courses(assignment))
    if change_type == 0:
        if len(assignment[semester_index]) == 4: # can't add if taking 4 courses
            return (None, float("inf"))

        possible_courses = new_course_domain(semester_index, assignment)
        possible_assignments = map(lambda x: add_to_assignment(assignment, semester_index, x), possible_courses)

    else:
        # print len(assignment[semester_index])
        if len(assignment[semester_index]) == 0:  # can't mutate/delete if no course to pick
            return (None, float("inf"))

        possible_course_indices = range(len(assignment[semester_index]))
        # print "mutating assignments"
        possible_assignments = map(lambda x: del_to_assignment(assignment, semester_index, x), possible_course_indices)

    if len(possible_assignments) == 0:
        return (None, float("inf"))
    
    assignment_costs = map(lambda x: (x, get_cost(x, weights)), possible_assignments)
    # print map(lambda x: x[1], assignment_costs)
    # print "returning successor len: ", len(get_flat_courses(min(assignment_costs, key = lambda (x,c): c)[0]))
    return min(assignment_costs, key = lambda (x,c): c)

def general_hill_climbing(successor_fun, weights, MAX_NUM_SIDEWAYS = 100, assignment = None):
    #print "in general hill climbing"

    start_time = time.time()
    num_sideways = 0
    num_iter = 0

    if not assignment:
        assignment = get_random_assignment()
    
    # LATER TESTING & GRAPHS
    curr_cost = get_cost(assignment, weights)
    cost_trace = [curr_cost]

    while True:
        successor, successor_cost = successor_fun(assignment, weights)
        # print "successor cost: ", successor_cost
        cost_trace.append(successor_cost)

        # assignment is local maximum, not a shoulder
        if successor == assignment:
            # print "in here"
            time_elapsed = round(time.time() - start_time, 2)
            return (assignment, cost_trace, num_iter, time_elapsed)

        # all good! hill-climb to neighbor
        if successor_cost < curr_cost:
            assignment = successor
            curr_cost = successor_cost
            num_iter += 1

            # check if just overcame a plateux, reset num sideways
            if num_sideways > 0:
                num_plateux += 1
                total_sideways_steps += num_sideways
                num_sideways = 0

        # in a shoulder, check if we can go sideways
        else:
            if successor_cost == curr_cost and num_sideways < MAX_NUM_SIDEWAYS:
                assignment = successor
                num_iter += 1
                num_sideways += 1
            else: # no escaping the plateux
                time_elapsed = round(time.time() - start_time, 2)
                return (assignment, cost_trace, num_iter, time_elapsed)


def sideways_hill_climbing(weights, MAX_NUM_SIDEWAYS = 100, assignment = None):
    return general_hill_climbing(get_greedy_successor, weights, MAX_NUM_SIDEWAYS, assignment)
  
# no sideway steps allowed
def naive_hill_climbing(weights, assignment = None, MAX_NUM_SIDEWAYS=0):
    # print "in naive hill climbing"
    return sideways_hill_climbing(weights, 0, assignment)

# print stats
# print("Local Search Algorithm: Initial Cost: {}. Final Cost: {}.\n Assignment:{}".format(initial_cost, curr_cost, assignment))
# return a trace of values resulting from your simulated annealing
#plt.plot(cost_trace, label="Full Local Search - 1000s of Successors")
# plt.show()
