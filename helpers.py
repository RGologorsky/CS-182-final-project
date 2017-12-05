# HELPER FUNCTIONS

from random         import *
from printing       import *
from constants      import *
from cost_functions import *
from cost_dicts     import *
from reqs           import *

# returns True with probability p
def coin_flip(p):
    return random() <= p

# returns whether course1 and course2 overlap in time
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
    # print start1, end1, start2, end2
    return not ((end1 < start2) or (end2 < start1))


# returns whether course has no overlap with the other courses
def no_overlap(course, assigned_courses):
    for assigned_course in assigned_courses:
        if overlap(course, assigned_course):
            return False
    return True

def get_flat_courses(assignment):
    return [course for semester in assignment for course in semester]

# return rough domain of a course to add to assignment.
def new_course_domain(semester_index, assignment):
    semester = 'F' if semester_index % 2 == 0 else 'S'
    already_taken = get_flat_courses(assignment)
    return filter(lambda c: courses[c]["SEMESTER"] == semester and \
        c not in already_taken and no_overlap(c, assignment[semester_index]), \
        courses.keys())
