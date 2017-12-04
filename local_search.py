from random import *
import numpy as np
import matplotlib.pyplot as plt
from copy import deepcopy

from printing import *
from constants import *
from cost_functions import *
from cost_dicts import *
from reqs import *

# returns True with probability p
def coin_flip(p):
    return random() <= p

def get_mutation_index(assignment):
    semester_index = randint(0, 7) # randint is inclusive both bounds
    course_index = randint(0, len(assignment[semester_index]) - 1)

    return (semester_index, course_index)

def pick_course(domain):
    return choice(domain)

def overlap(course1, course2):

    if course1 not in courses or course2 not in courses:
        return False

    if courses[course1]["SEMESTER"] != courses[course2]["SEMESTER"]:
        return False

    days1 = courses[course1]["DAYS"]
    days2 = courses[course2]["DAYS"]

    # handles when no days: overlap is 0
    if len(days1 & days2) == 0:
        return False

    start1 = courses[course1]["START"]
    end1   = courses[course1]["END"]

    start2 = courses[course2]["START"]
    end2   = courses[course2]["END"]

    # class 1 first or class 2 first
    return (start1 < start2 and end1 < start2) or \
            (start2 < start1 and end2 < start1)


def no_overlap(course, assigned_courses):
    for assigned_course in assigned_courses:
        if overlap(course, assigned_course):
            return False
    return True

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

    elif change_type == 0:
        if len(assignment[semester_index]) == 4:
            return assignment

    else:
        # remove random course from assignment
        course_index = randint(0, len(assignment[semester_index]) - 1)
        flat_courses.remove(assignment[semester_index][course_index])


    # compute rough domain
    semester = 'F' if semester_index % 2 == 0 else 'S'
    domain = []

    for course in courses:
        course_info = courses[course]
        if course_info["SEMESTER"] == semester and no_overlap(course, flat_courses):
            domain.append(course)


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


MAX_NUM_SIDEWAYS = 100

def hill_climbing(assignment):
    num_iter     = 0
    num_sideways = 0

    print_assignment(assignment)
    curr_cost = get_req_cost(assignment)
    
    while True:
        successor = get_greedy_successor(assignment)
        successor_cost = get_req_cost(successor)
        
        print_assignment(successor)
        
        if successor_cost < curr_cost:
            assignment = successor
            curr_cost = successor_cost 
            num_iter += 1
            num_sideways = 0 # overcome  plateux, reset num sideways
        else:
            num_sideways += 1
            
            if num_sideways < MAX_NUM_SIDEWAYS:
                assignment = successor
                num_iter += 1
            else: # no escaping the plateux
                return assignment

result = hill_climbing([
                        ["CS109"], ["CS1"], 
                        ["CS182"], ["CS125"], 
                        ["MATH21A"], ["CS181"],
                        ["AM107"], ["MATH23A"]
                       ])
print result
