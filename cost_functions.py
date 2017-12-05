# Return the cost of an assignment
from constants import *
from helpers import *

def get_flat_courses(assignment):
    return [course for semester in assignment for course in semester]

def get_cost(assignment, weights = [100, 1, 1, 1, 1]):
    courses = get_flat_courses(assignment)
    return weights[0] * get_req_cost(courses) + \
        weights[1] * get_prereq_cost(assignment) + \
        weights[2] * get_workload_cost(assignment) + \
        weights[3] * get_q_cost(courses) + \
        weights[4] * get_enrollment_cost(courses)

def get_feature_cost(course, feature):
    if course in courses and feature in courses[course]:
        return courses[course][feature]
    return 0

def get_prereq_cost(assignment):
    num_violated = 0
    for index in range(8):
        semester = assignment[index]
        prior_courses = get_flat_courses(assignment[:index])
        for course in semester:
            prereqs = courses[course]["PREREQS"]
            for item in prereqs:
                if type(item) is str and item not in prior_courses:
                    num_violated += 1
                if type(item) is set:
                    # at least one in assignment prior to course
                    if len(set(prior_courses) & item) == 0:
                        num_violated += 1
    return num_violated

def get_workload_cost(assignment):
    courses = get_flat_courses(assignment)
    total_hrs = sum(map(lambda c: get_feature_cost(c, "WORKLOAD"), courses))
    avg_hours = total_hrs/len(courses)

    scaled_hrs = hrs/200.0
    # add variances
    total_variance = 0
    for semester in assignment:
        total_variance += sum(lambda c: (c - avg_hours)^2, semester)

    return scaled_hrs + total_variance

def get_q_cost(courses):
    return sum(map(lambda c: 5 - get_feature_cost(c, "Q"), courses))

def get_enrollment_cost(courses):
    return sum(map(lambda c: get_feature_cost(c, "ENROLLMENT"), courses))/25.0   

# course requirement cost
# def get_req_cost(assignment):
#     courses = get_flat_courses(assignment)
#     return math_cost(courses)[0] + software_cost(courses)[0] \
#            + theory_cost(courses)[0] \
#            + technical_and_breadth_cost(courses)[0]
       


# COURSE REQUIREMENT COSTS

def common(course_list, courses):
    return set(course_list) & set(courses)

def math_cost(courses):
    lin_alg    = ["AM21A","MATH21A", "MATH23A","MATH25B", "MATH55B"]
    multi_calc = ["AM21B","MATH21B", "MATH23B","MATH25A", "MATH55A"]

    my_lin_alg    = common(lin_alg, courses) 
    my_multi_calc = common(multi_calc, courses) 

    cost = 2

    used_to_satisfy = []    
    if len(my_lin_alg) >= 1: 
        used_to_satisfy.append(my_lin_alg.pop())
        cost -= 1

    if len(my_multi_calc) >= 1: 
        used_to_satisfy.append(my_multi_calc.pop())
        cost -= 1

    #extra = my_lin_alg | my_multi_calc
    #return (cost, used_to_satisfy, extra)
    return (cost, used_to_satisfy)
    
def software_cost(courses):
    software = ["CS050", "CS051", "CS061"]

    my_software = common(software, courses) 
    used_to_satisfy = []

    cost = 2

    if len(my_software) == 1:
        used_to_satisfy.append(my_software.pop())
        cost -= 1

    # decreases size by 1
    if len(my_software) == 1:
        used_to_satisfy.append(my_software.pop())
        cost -= 1

    # note remaining courses in my_sofware are the extra ones
    # return (cost, used_to_satisfy, my_software)
    return (cost, used_to_satisfy)
   

def theory_cost(courses):
    def is_theory_class(x):
        if x == "CS020":
            return False
        return x in ["AM106","AM107"] or (x[:2] == "CS" and x[-2] == "2")

    my_theory = set(filter(is_theory_class, courses))
    used_to_satisfy = []

    cost = 2

    if "CS125" not in my_theory:
        if "CS121" in my_theory:
            used_to_satisfy.append("CS121")
            my_theory.remove("CS121")
            cost -= 1

        if len(my_theory) >= 1:
            used_to_satisfy.append(my_theory.pop())
            cost -= 1
    else:
        used_to_satisfy.append("CS125")
        cost -= 1

        my_theory.discard("CS121")
        my_theory.discard("CS124")

        if len(my_theory) >= 1:
            used_to_satisfy.append(my_theory.pop())
            cost -= 1

    # return (cost, used_to_satisfy, my_theory)
    return (cost, used_to_satisfy)

# returns best technical courses to maximize breadth
def technical_and_breadth_cost(courses):
    def is_cs(x): return (course[:2] == "CS")

    def get_penultimate(x):
        last_digit = -2 if course[-1] in ["A", "B"] else -1
        return x[last_digit-1]

    my_theory = theory_cost(courses)[1]

    used_to_satisfy = []
    my_penultimates = []

    def valid_breadth(penultimate): 
        return penultimate not in my_penultimates and penultimate not in ["0", "2", "9"]
    
    technical_cost = 4
    breadth_cost = 2


    noncs = ["STAT110", "MATH154", "AM106", "AM107", "AM120", "AM121", "ES50", "ES52"]
    intro = ["CS001", "CS020", "CS050", "CS051", "CS061"]

    intro_elective = "CS050" in courses and "CS051" in courses and "CS061" in courses


    for course in courses:
        if technical_cost > 0 and course in noncs and course not in my_theory:
            used_to_satisfy.append(course)
            technical_cost -= 1

        if is_cs(course) and course not in my_theory and course not in intro:
            penultimate = get_penultimate(course)

            if breadth_cost > 0 and valid_breadth(penultimate):
                my_penultimates.append(penultimate)
                used_to_satisfy.append(course)
                breadth_cost -= 1

                technical_cost = max(0, technical_cost - 1)

            else:
                if technical_cost > 0 and course not in my_theory:
                    used_to_satisfy.append(course)
                    technical_cost -= 1

    # consider CS51 or 61
    if intro_elective:
        if breadth_cost > 0 and "5" not in my_penultimates:
            my_penultimates.append("5")
            used_to_satisfy.append("CS051")
            breadth_cost -= 1
            technical_cost = max(0, technical_cost - 1)
        
        elif breadth_cost > 0 and "6" not in my_penultimates:
                my_penultimates.append("6")
                used_to_satisfy.append("CS061")
                breadth_cost -= 1
                technical_cost = max(0, technical_cost - 1)

        else:
            if technical_cost > 0:
                used_to_satisfy.append("CS061")
                technical_cost -= 1

    cost = breadth_cost + technical_cost

    #return (cost, used_to_satisfy, set(my_technical) - set(used_to_satisfy))
    return (cost, used_to_satisfy)

def get_req_cost(courses):
    return math_cost(courses)[0] + software_cost(courses)[0] \
        + theory_cost(courses)[0] \
        + technical_and_breadth_cost(courses)[0]
       
