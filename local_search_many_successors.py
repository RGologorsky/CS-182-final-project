from random         import randint, choice
from printing       import *
from helpers        import *
from constants      import *
from cost_functions import *
from cost_dicts     import *
from copy           import deepcopy

# ASSIGNMENT = list of 8 semesters; each semester is a list of up to 4 classes
# SUCCESSOR = 1 course ADDED, MUTATED, or DELETED from the ASSIGNMENT

# ASSIGNMENT = list of 8 semesters; each semester is a list of up to 4 classes
# SUCCESSOR = 1 course ADDED, MUTATED, or DELETED from the ASSIGNMENT

# ASSIGNMENT: 8 semesters, each semester has <=4 classes. for each semester:
# ~25 add options, ~4 delete options, 20x4 = 80 mutate options => 1000 successors


# returns the greedy - lowest cost - successor state.
def get_greedy_successor2(assignment, wts):

    min_cost = get_cost(assignment, wts)

    best_successor = assignment

    for semester_index in xrange(8):
            # successors: (0) add, (1) delete course from semester
            successor0 = get_successor_type2(assignment, semester_index, 0)
            successor1 = get_successor_type2(assignment, semester_index, 1)
            successor2 = get_successor_type2(assignment, semester_index, 2)

            cost0, cost1, cost2 = get_cost(successor0, wts), get_cost(successor1, wts), get_cost(successor2, wts)

            # motivates adding over deleting
            if successor0 <= successor1 and successor0 <= successor2:
                successor = successor0
                successor_cost = cost0
            
            elif successor1 <= successor2 and successor1 <= successor3:
                successor = successor1
                successor_cost = cost1
            
            else:
                successor = successor2
                successor_cost = cost2

            if successor_cost <= min_cost:
                best_successor = successor
                min_cost = successor_cost

    return (best_successor, min_cost)


# returns lowest cost successor state of given action - add, mutate, delete
def get_successor_type2(assignment, semester_index, change_type=0):

    #  add course (type 0), delete course (type 1), muate course (type 2)

    # can't delete if no courses in semester
    if change_type == 1 and len(assignment[semester_index]) == 0:
        return assignment

    # can't add if alreadying taking 4 courses
    if change_type == 0 and len(assignment[semester_index]) == 4:
            return assignment

    if change_type == 0: # adding a course
        possible_courses = new_course_domain(semester_index, assignment)
        possible_assignments = map(lambda x: add_assignment(assignment, semester_index, x), possible_courses)
        if len(possible_assignments) == 0:
            return assignment   
        return min(possible_assignments, key = lambda a: get_cost(a, wts))

    if change_type == 1 or change_type == 2: # deleting a course
        # possibilities for the course index to delete.
        possible_course_indices = range(len(assignment[semester_index]))
        possible_assignments = map(lambda x: del_assignment(assignment, semester_index, x), possible_course_indices)
        
        if len(possible_assignments) == 0:
            return assignment  

        if change_type == 1: # if just delete, we are done.
            return min(possible_assignments, key = lambda a: get_cost(a, wts))

        # for mutation, we now check best add state.
        return min(possible_assignments, \
            key = lambda a: get_cost(get_successor_type2(a, wts, semester_index, 0)))


# we allow sideways movements to overcome plateux
def sideways_hill_climbing2(assignment, wts, MAX_NUM_SIDEWAYS = 100):
    num_iter     = 0
    num_sideways = 0
    num_plateux  = 0
    total_sideways_steps = 0

    # LATER TESTING & GRAPHS
    initial_cost = get_cost(assignment, wts)
    curr_cost = initial_cost

    trace = [assignment]
    cost_trace = [initial_cost]

    def get_avg_num_sideways():
        return 0 if num_plateux == 0 else (total_sideways_steps * 1.0)/num_plateux


    while True:
        successor, successor_cost = get_greedy_successor2(assignment)

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
    # print stats
    print("Local Search Algorithm: Initial Cost: {}. Final Cost: {}.\n Assignment:{}".format(initial_cost, curr_cost, assignment))
    # return a trace of values resulting from your simulated annealing
    plt.plot(cost_trace, label="Full Local Search - 1000s of Successors")
    plt.show()
    return assignment
  
# no sideway steps allowed
def naive_hill_climbing2(assignment, weights):
    return sideways_hill_climbing(assignment, weights, MAX_NUM_SIDEWAYS = 0)
