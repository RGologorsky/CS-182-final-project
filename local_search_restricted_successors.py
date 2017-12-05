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
def get_greedy_successor(assignment, weights):

    min_cost = get_cost(assignment, weights)
    best_successor = assignment

    for semester_index in xrange(8):
            # successors: (0) add, (1) delete course from semester
            successor0, cost0 = get_successor_type(assignment, weights, semester_index, 0)
            successor1, cost1 = get_successor_type(assignment, weights, semester_index, 1)

            if min(cost0, cost1) <= min_cost:
                if cost0 < cost1:
                    best_successor, min_cost = (successor0, cost0)

                else:
                    best_successor, min_cost = (successor1, cost1)

    return (best_successor, min_cost)

# A state is a list of value indices.
# Randomly picks value indices until the weight limit is reached
def get_successor_type(assignment, weights, semester_index, change_type=0):

    #  add course (type 0), delete course (type 1)

    if change_type == 0:
        if len(assignment[semester_index]) == 4: # can't add if taking 4 courses
            return (None, float("inf"))

        possible_courses = new_course_domain(semester_index, assignment)
        possible_assignments = map(lambda x: add_to_assignment(assignment, semester_index, x), possible_courses)

    else:
        if len(assignment[semester_index]) == 0:  # can't mutate/delete if no course to pick
            return (None, float("inf"))

        possible_course_indices = range(len(assignment[semester_index]))
        possible_assignments = map(lambda x: del_to_assignment(assignment, semester_index, x), possible_course_indices)

    if len(possible_assignments) == 0:
            return (None, float("inf"))
    
    assignment_costs = map(lambda x: (x, get_cost(x, weights)), possible_assignments)
    return min(assignment_costs, key = lambda (x,c): c)

def general_hill_climbing(successor_fun, weights, MAX_NUM_SIDEWAYS = 100, assignment = None):
    # print "In Sideways HC, #sideways = ", MAX_NUM_SIDEWAYS
    print "WEIGHTS", weights
    num_iter     = 0
    num_sideways = 0
    num_plateux  = 0
    total_sideways_steps = 0

    if not assignment:
        assignment = get_random_assignment()
    # LATER TESTING & GRAPHS
    initial_cost = get_cost(assignment, weights)
    curr_cost = initial_cost

    trace = [assignment]
    cost_trace = [initial_cost]

    def get_avg_num_sideways():
        return 0 if num_plateux == 0 else (total_sideways_steps * 1.0)/num_plateux


    while True:
        successor, successor_cost = successor_fun(assignment, weights)

        trace.append(successor)
        cost_trace.append(successor_cost)

        # assignment is local maximum, not a shoulder
        if successor == assignment:
            return (assignment, initial_cost, curr_cost, MAX_NUM_SIDEWAYS, \
                        num_iter, num_plateux, get_avg_num_sideways())

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
        if successor_cost == curr_cost:
            if num_sideways < MAX_NUM_SIDEWAYS:
                assignment = successor
                num_iter += 1
                num_sideways += 1
            else: # no escaping the plateux
                return (assignment, initial_cost, curr_cost, MAX_NUM_SIDEWAYS, \
                            num_iter, num_plateux, get_avg_num_sideways())


def sideways_hill_climbing(weights, MAX_NUM_SIDEWAYS = 100, assignment = None):
    return general_hill_climbing(get_greedy_successor, weights, MAX_NUM_SIDEWAYS, assignment)
  
# no sideway steps allowed
def naive_hill_climbing(weights, assignment = None):
    return sideways_hill_climbing(weights, MAX_NUM_SIDEWAYS = 0, assignment = None)

# print stats
# print("Local Search Algorithm: Initial Cost: {}. Final Cost: {}.\n Assignment:{}".format(initial_cost, curr_cost, assignment))
# return a trace of values resulting from your simulated annealing
#plt.plot(cost_trace, label="Full Local Search - 1000s of Successors")
# plt.show()
