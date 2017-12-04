from random         import randint, choice
from printing       import *
from helpers        import *
from constants      import *
from cost_functions import *
from cost_dicts     import *
from reqs           import *
from copy           import deepcopy

# ASSIGNMENT = list of 8 semesters; each semester is a list of up to 4 classes
# SUCCESSOR = 1 course ADDED, MUTATED, or DELETED from the ASSIGNMENT

# ASSIGNMENT: 8 semesters, each semester has <=4 classes, ~20 options per class
# ~ 1100 SUCCESSORS: 8 semesters, each semester <= 4 classes, for each class:
# ~25 add options, ~4 delete options, ~25x4 mutate options => 140 choices
# ==> 8 * 140 ~ 1100 SUCCESSORS


# returns the greedy successor state.
def get_greedy_successor(assignment):
   
    min_cost = get_req_cost(assignment)

    best_successor = assignment
    
    for semester_index in xrange(8):
            # successors: (0) add, (1) mutate, (2) delete course from semester
            successor0 = get_successor_type(assignment, semester_index, 0)
            successor1 = get_successor_type(assignment, semester_index, 1)
            successor2 = get_successor_type(assignment, semester_index, 2)

            cost0 = get_req_cost(successor0)
            cost1 = get_req_cost(successor1)
            cost2 = get_req_cost(successor2)

            min_new = min(cost0, cost1, cost2)

            if min_new == cost0: successor = successor0
            if min_new == cost1: successor = successor1
            if min_new == cost2: successor = successor2

            if min_new <= min_cost:
                best_successor = successor
                min_cost = min_new

    return best_successor

# A state is a list of value indices.
# Randomly picks value indices until the weight limit is reached
def get_successor_type(assignment, semester_index, change_type=0):

    flat_courses = get_flat_courses(assignment)

    #  add course (type 0), mutate course (type 1), delete course (type 2)
    if change_type == 2 and len(assignment[semester_index]) == 0:
        return assignment

    if change_type == 0 and len(assignment[semester_index]) == 4:
            return assignment

    if change_type == 1 or change_type == 2: # choose course to mutate/delete 
        # remove random course from assignment
        course_index = randint(0, len(assignment[semester_index]) - 1)
        flat_courses.remove(assignment[semester_index][course_index])


    # compute domain for a new course to add to the assignment
    semester = 'F' if semester_index % 2 == 0 else 'S'
    domain = new_course_domain(semester, flat_courses)

    def new_assignment(course):
        a = deepcopy(assignment)

        if change_type == 0: # add a course
            a[semester_index].append(course)

        if change_type == 1: # mutate a course
            a[semester_index][course_index] = course
        
        if change_type == 2: # delete a course
            a[semester_index].pop(course_index)

        return a

    successor = min(map(lambda x: new_assignment(x), domain), \
                key = lambda x: get_req_cost(x))
    return successor


def hill_climbing(assignment, MAX_NUM_SIDEWAYS = 100):
    num_iter     = 0
    num_sideways = 0
    num_plateux  = 0

    curr_cost = get_req_cost(assignment)
    
    while True:
        successor = get_greedy_successor(assignment)
        successor_cost = get_req_cost(successor)
                
        if successor_cost < curr_cost:
            assignment = successor
            curr_cost = successor_cost 
            num_iter += 1
            num_sideways = 0 # overcome  plateux, reset num sideways
            num_plateux += 1
        else:
            num_sideways += 1
            
            if num_sideways < MAX_NUM_SIDEWAYS:
                assignment = successor
                num_iter += 1
            else: # no escaping the plateux
                return (assignment, MAX_NUM_SIDEWAYS, num_iter, num_plateux)

result = hill_climbing([
                        ["CS109"], ["CS1"], 
                        ["CS182"], ["CS125"], 
                        ["MATH21A"], ["CS181"],
                        ["AM107"], ["MATH23A"]
                       ])
print_hill_climb(result)
