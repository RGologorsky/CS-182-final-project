from random         import randint, choice, sample
from printing       import *
from helpers        import *
from constants      import *
from cost_functions import *
from cost_dicts     import *
from copy           import deepcopy

from local_search_restricted_successors import general_hill_climbing


# FIRST CHOICE HILL CLILMBING: PICKS FIRST RANDOM NEIGHBOR THAT'S BETTER
# GOOD WHEN MANY SUCCESSOR STATES

# ASSIGNMENT = list of 8 semesters; each semester is a list of up to 4 classes
# SUCCESSOR = 1 course ADDED, MUTATED, or DELETED from the ASSIGNMENT

# ASSIGNMENT: 8 semesters, each semester has <=4 classes. for each semester:
# ~25 add options, ~4 delete options, 20x4 = 80 mutate options => 1000 successors

# returns the first choice successor state.
# def get_first_choice_successor2(assignment, weights):
#     curr_cost = get_cost(assignment, weights)
#     random_semester_order = sample(range(8), 8)
#     for semester_index in random_semester_order:
#         random_action_order = sample(range(3), 3)
#         for action in random_action_order:
#             successor, cost = get_successor_type2(assignment, weights, \
#                                             semester_index, action, curr_cost)

#             if (cost < curr_cost):
#                 return (successor, cost)
#     return assignment, curr_cost
# returns the greedy - lowest cost - successor state.
def get_first_choice_add_successor(assignment, weights, add_index):
    if len(assignment[add_index]) == 4: # can't add if taking 4 courses
        return (None, float("inf"))

    curr_c = get_cost(assignment, weights)

    possible_adds = new_course_domain(add_index, assignment)
    for a in possible_adds:
        new_a = add_to_assignment(assignment, add_index, a)
        cost_a = get_cost(new_a, weights)

        if cost_a < curr_c:
            return (new_a, cost_a)

    return (None, float("inf"))

def get_first_choice_del_successor(assignment, weights, del_index):
    if len(assignment[del_index]) == 0: # can't add if taking 4 courses
        return (None, float("inf"))

    curr_c = get_cost(assignment, weights)

    course_del_indices = range(len(assignment[del_index]))

    for course_del_index in course_del_indices:
        new_a = del_to_assignment(assignment, del_index, course_del_index)
        cost_a = get_cost(new_a, weights)

        if cost_a < curr_c:
            return (new_a, cost_a)

    return (None, float("inf"))


# given a good add index anda  good delete index.
def get_first_choice_mut_successor(assignment, weights, add_index, del_index):
    # if full at semester add index or empty at delete index, 
    # simplifies to pure add/del. Else: first del, then add.
    curr_c = get_cost(assignment, weights)
    course_del_indices = range(len(assignment[del_index]))

    for course_del_index in course_del_indices:
        del_assignment = del_to_assignment(assignment, del_index, course_del_index)

        
        possible_adds = new_course_domain(add_index, del_assignment)
        for course in possible_adds:
            mut_a = add_to_assignment(del_assignment, add_index, course)
            mut_cost = get_cost(mut_a, weights)
            if mut_cost < curr_c:
               return (mut_a, mut_cost)

    return (None, float("inf"))


def get_first_choice_successor2(assignment, weights):

    min_cost = get_cost(assignment, weights)

    # check mutation: add from any, delete from any (including just add/del)
    randomized_adds = sample(range(-1,8), 9)

    for add_index in randomized_adds:
        randomized_dels = sample(range(-1,8), 9)

        for del_index in randomized_dels:
            
            if add_index == -1 and del_index == -1:
                cost = min_cost
            
            elif add_index == -1 or len(assignment[add_index]) == 4:
                successor, cost = \
                    get_first_choice_del_successor(assignment, weights, del_index)

                if cost < min_cost:
                    return successor, cost
            
            elif del_index == -1 or len(assignment[del_index]) == 0:
                successor, cost = \
                     get_first_choice_add_successor(assignment, weights, add_index)

                if cost < min_cost:
                    return successor, cost
            
            else:
                successor, cost = \
                    get_first_choice_mut_successor(assignment, weights, add_index, del_index)

                if cost < min_cost:
                    return successor, cost

    return (assignment, min_cost)

def get_first_choice_successor1(assignment, weights):

    min_cost = get_cost(assignment, weights)

    # check mutation: add from any, delete from any (including just add/del)
    randomized_semesters = sample(range(8), 8)
    successor_functions = [get_first_choice_add_successor, 
                           get_first_choice_del_successor]

    for semester_index in randomized_semesters:

        randomized_action = sample(range(2), 2)

        for i in randomized_action:
            successor_function = successor_functions[i]

            successor, cost = \
                successor_function(assignment, weights, semester_index)

            if cost < min_cost:
                return successor, cost

    return (assignment, min_cost)

# we allow sideways movements to overcome plateux
def sideways_first_choice2(weights, MAX_NUM_SIDEWAYS = 100, assignment = None):
    return general_hill_climbing(get_first_choice_successor2, weights, MAX_NUM_SIDEWAYS, assignment)
  
# no sideway steps allowed
def naive_first_choice2(weights, assignment = None, MAX_NUM_SIDEWAYS=0):
    return sideways_first_choice2(weights, 0, assignment)

# we allow sideways movements to overcome plateux
def sideways_first_choice(weights, MAX_NUM_SIDEWAYS = 100, assignment = None):
    return general_hill_climbing(get_first_choice_successor1, weights, MAX_NUM_SIDEWAYS, assignment)
  
# no sideway steps allowed
def naive_first_choice(weights, assignment = None, MAX_NUM_SIDEWAYS=0):
    return sideways_first_choice(weights, 0, assignment)

# print stats
    # print("First-Choice Algorithm: Initial Cost: {}. Final Cost: {}.\n Assignment:{}".format(initial_cost, curr_cost, assignment))
    # return a trace of values resulting from your simulated annealing
    #plt.plot(cost_trace, label="First Choice Search - 1000s of Successors")
    #plt.show()
