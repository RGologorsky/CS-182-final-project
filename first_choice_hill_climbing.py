from random         import randint, choice, sample
from printing       import *
from helpers        import *
from constants      import *
from cost_functions import *
from cost_dicts     import *
from copy           import deepcopy

# FIRST CHOICE HILL CLILMBING: PICKS FIRST RANDOM NEIGHBOR THAT'S BETTER
# GOOD WHEN MANY SUCCESSOR STATES

# ASSIGNMENT = list of 8 semesters; each semester is a list of up to 4 classes
# SUCCESSOR = 1 course ADDED, MUTATED, or DELETED from the ASSIGNMENT

# ASSIGNMENT: 8 semesters, each semester has <=4 classes. for each semester:
# ~25 add options, ~4 delete options, 20x4 = 80 mutate options => 1000 successors

# returns the first choice successor state.
def get_first_choice_successor2(assignment, weights):

    curr_cost = get_cost(assignment, weights)

    random_semester_order = sample(range(8), 8)
    for semester_index in random_semester_order:
        random_action_order = sample(range(3), 3)
        for action in random_action_order:
            successor, cost = get_successor_type2(assignment, weights, \
                                            semester_index, action, curr_cost)

            if (cost < curr_cost):
                return (successor, cost)
    return assignment, curr_cost


# returns successor state of given action type (add course, mutate, delete)
def get_successor_type2(assignment, weights, semester_index, change_type, curr_cost):

    #  add course (type 0), delete course (type 1), muate course (type 2)

    # can't delete if no courses in semester
    if change_type == 1 and len(assignment[semester_index]) == 0:
        return assignment, curr_cost

    # can't add if alreadying taking 4 courses
    if change_type == 0 and len(assignment[semester_index]) == 4:
        return assignment, curr_cost

    if change_type == 0: # adding a course
        possible_courses = new_course_domain(semester_index, assignment)
        possible_assignments = map(lambda x: \
            add_to_assignment(assignment, semester_index, x), possible_courses)
       
        for a in possible_assignments:
            c = get_cost(a, weights)
            if c < curr_cost:
                return a, c
        return a, curr_cost

    if change_type == 1 or change_type == 2: # deleting a course
        # possibilities for the course index to delete.
        possible_course_indices = range(len(assignment[semester_index]))
        possible_assignments = map(lambda x: del_to_assignment(assignment, semester_index, x), possible_course_indices)
        
        if change_type == 1: # we just delete, and are done.
            for a in possible_assignments:
                c = get_cost(a, weights)
                if c < curr_cost:
                    return a, c
            return a, curr_cost

        # for mutation, we now check add back a course.
        for a in possible_assignments:
            a_new, c_new = get_successor_type2(a, weights, semester_index, 0, curr_cost)
            if c_new < curr_cost:
                return a_new, c_new
        return assignment, curr_cost

# we allow sideways movements to overcome plateux
def sideways_first_choice(weights, MAX_NUM_SIDEWAYS = 100):
    num_iter     = 0
    num_sideways = 0
    num_plateux  = 0
    total_sideways_steps = 0

    assignment = get_random_assignment()
    
    # LATER TESTING & GRAPHS
    initial_cost = get_cost(assignment, weights)
    curr_cost = initial_cost

    trace = [assignment]
    cost_trace = [initial_cost]

    def get_avg_num_sideways():
        return 0 if num_plateux == 0 else (total_sideways_steps * 1.0)/num_plateux


    while True:
        successor, successor_cost = get_first_choice_successor2(assignment, weights)

        trace.append(successor)
        cost_trace.append(successor_cost)

        # assignment is local maximum, not a shoulder; no improvement.
        if successor == assignment:
            return (assignment, initial_cost, curr_cost, MAX_NUM_SIDEWAYS, \
                        num_iter, num_plateux, get_avg_num_sideways())

        # in a shoulder, check if we can go sideways
        if successor_cost == curr_cost:
            if num_sideways < MAX_NUM_SIDEWAYS:
                assignment = successor
                num_iter += 1
                num_sideways += 1
            else: # we tried, but there's no escaping the plateux
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
    print("First-Choice Algorithm: Initial Cost: {}. Final Cost: {}.\n Assignment:{}".format(initial_cost, curr_cost, assignment))
    # return a trace of values resulting from your simulated annealing
    #plt.plot(cost_trace, label="First Choice Search - 1000s of Successors")
    #plt.show()
    return assignment
