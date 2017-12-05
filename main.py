from printing import *
from branch_and_bound import *
from local_search import *
from random import *
from helpers import *

from csv_parser import *

# get_courses_dict()

def get_random_assignment():
    assignment = [[] for _ in xrange(8)]

    free_semesters = range(8)

    while len(free_semesters) > 0:
    
        semester_index = choice(free_semesters)

        domain = new_course_domain(semester_index, assignment)

        if len(domain) == 0:
            free_semesters.remove(semester_index)

        else:
            course = choice(domain)
            assignment[semester_index].append(course)

            if len(assignment[semester_index]) == 4:
                free_semesters.remove(semester_index)

    return assignment

 
# print overlap("CS182", "CS182")   
# print_assignment(get_random_assignment())
result = sideways_hill_climbing(get_random_assignment())
print_hill_climb(result)

