# Return the cost of an assignment
from constants import *
from helpers import *
from math import pow

MAX_WEIGHT = 100 #
MIN_WEIGHT = 0.01

# for feature normalization

NORM_INDICES = {"Q": 0, "WORKLOAD": 1, "ENROLLMENT": 2}
MEANS = [0.4697025731,    6.573227693, 131.4900483]
STD   = [3.896434938, 10.81354724, 98.8291939]

def normalize(cost, feature):
    i = NORM_INDICES[feature]
    return (cost - (MEANS[i]))/STD[i]

def get_flat_courses(assignment):
    try:
        return [course for semester in assignment for course in semester]
    except:
        print "FAILED FAILED ", assignment
        return [course for semester in assignment for course in semester]

def get_cost(assignment, weights):
    cost_list = get_costs(assignment, weights)
    indices = range(len(weights))

    return sum(map(lambda i: weights[i] * cost_list[i], indices))


def get_costs(assignment, weights, printing=False):
    courses = get_flat_courses(assignment)
    costs = [0 for _ in range(6)]
    
    if len(courses) == 0:
        return costs

    costs[0] = get_prereq_cost(assignment, printing)   if weights[0] != 0 else 0
    costs[1] = get_workload_cost(assignment, printing) if weights[1] != 0 else 0
    costs[2] = get_q_cost(courses, printing)           if weights[2] != 0 else 0
    costs[3] = get_enrollment_cost(courses, printing)  if weights[3] != 0 else 0
    costs[4] = get_req_cost(courses)
    costs[5] = get_workload_variation_cost(assignment, printing)

    return costs

def get_feature_cost(course, feature):
    if course in courses and feature in courses[course]:
        return courses[course][feature]
    return 0

def get_prereq_cost(assignment, printing=False):
    num_violated = 0
    violations = []
    for index in range(8):
        semester = assignment[index]
        prior_courses = get_flat_courses(assignment[:index])
        for course in semester:
            prereqs = courses[course]["PREREQS"]
            for item in prereqs:
                if type(item) is str and item not in prior_courses:
                    num_violated += 1
                    violations.append(course)
                if type(item) is set:
                    # at least one in assignment prior to course
                    if len(set(prior_courses) & item) == 0:
                        num_violated += 1
                        violations.append(course)
    if printing:
        s = "No. Pre-Reqs Disregarded"
        res = "%-25s: %d" % (s, num_violated)
        if num_violated > 0:
           res += "(" + str(violations)[1:-1] + ")"
        print res
    return num_violated # feature scaling, (x - min)/s.d.

def get_workload_variation_cost(assignment, printing = False):
    # print "hi, printing: ", str(printing)
    #if printing:
    #    print("assignment: ", assignment)

    courses = get_flat_courses(assignment)
    if len(courses) == 0:
        return 0
    semester_hrs = []
    for semester in assignment:
        hrs = sum(map(lambda c: get_feature_cost(c, "WORKLOAD"), semester))
        semester_hrs.append(hrs)

    return max(semester_hrs) - min(semester_hrs)
    #avg_semester_hours = sum(semester_hrs)/8.0
    #return (max(semester_hrs) - min(hrs))
    # return len(filter(lambda x: x > 2 * MEANS[NORM_INDICES["WORKLOAD"]], hrs))
    #printing = False

    courses = get_flat_courses(assignment)
    hrs = map(lambda c: get_feature_cost(c, "WORKLOAD"), courses)
    total_hrs = sum(hrs)

    avg_hours = total_hrs/len(courses) if len(courses) != 0 else 0
    my_avg_semester_len = sum(map(lambda semester: len(semester), assignment))/8
    my_avg_semester_hours = avg_hours * my_avg_semester_len
    avg_semester_hours = avg_hours * 2 # say 2 class avg

    # add variances
    total_variance = 0

    if printing:
        print "Avg. Semester Workload : %2.2f. " % my_avg_semester_hours,

    res = "("
    for index, semester in enumerate(assignment):
        semester_hours = sum(map(lambda c: get_feature_cost(c, "WORKLOAD"), semester))
        res += str(semester_hours)
        res += ", " if index < 7 else "."
        total_variance += pow((semester_hours - my_avg_semester_hours),2)
    avg_variance_per_semester = total_variance/8

    if printing:
        print res + "). " + ("Avg. Variation (hours): %2.2f." % avg_variance_per_semester)

    # AVG VAR, AVG STD VAR
    AVG_SEM_VAR = 43.20732231       # x 4? semester = sum 4 class's var
    AVG_SEM_STD_VAR = 3.720555031  * 2  # x 2? sqrt(4) = 2?
    return (avg_variance_per_semester-AVG_SEM_VAR)/(AVG_SEM_STD_VAR)

def get_workload_cost(assignment, printing=False):
    courses = get_flat_courses(assignment)
    hrs = map(lambda c: get_feature_cost(c, "WORKLOAD"), courses)
    total_hrs = sum(hrs)

    avg_hours = total_hrs/len(courses) if len(courses) > 0 else 0
    my_avg_semester_len = sum(map(lambda semester: len(semester), assignment))/8
    my_avg_semester_hours = avg_hours * my_avg_semester_len
    avg_semester_hours = avg_hours * 2 # say 2 class avg

    # add variances
    total_variance = 0

    if printing:
        s = "Avg. Semester Workload"
        print "%-25s : %2.2f. " % (s,my_avg_semester_hours),

    res = "("
    for index, semester in enumerate(assignment):
        semester_hours = sum(map(lambda c: get_feature_cost(c, "WORKLOAD"), semester))
        res += str(semester_hours)
        res += ", " if index < 7 else "."
        total_variance += pow((semester_hours - my_avg_semester_hours),2)
    avg_variance_per_semester = total_variance/8

    if printing:
        print res + "). " + ("Avg. Variation (hours): %2.2f." % avg_variance_per_semester)

    # AVG VAR, AVG STD VAR
    AVG_SEM_VAR = 43.20732231       # x 4? semester = sum 4 class's var
    AVG_SEM_STD_VAR = 3.720555031  * 2  # x 2? sqrt(4) = 2?
    return normalize(avg_hours, "WORKLOAD")

def get_q_cost(courses, printing=False):
    if len(courses) > 0:
        avg_q_cost = sum(map(lambda c: 5 - get_feature_cost(c, "Q"), courses))/len(courses)
    else:
        return 0
    if printing:
        s = "Avg. Q-Score"
        print "%-25s: %2.2f" % (s, 5- avg_q_cost)
    return (avg_q_cost - (5 - MEANS[0]))/STD[NORM_INDICES["Q"]]

def get_enrollment_cost(courses, printing=False):
    if len(courses) > 0:
        avg_enrollment = sum(map(lambda c: get_feature_cost(c, "ENROLLMENT"), courses))/len(courses)

    if printing:
        s = "Avg. Enrollment"
        print "%-25s: %2.2f" % (s, avg_enrollment)

    if len(courses) == 0 or avg_enrollment < 50:
        return 0

    return (avg_enrollment - 50)/STD[NORM_INDICES["ENROLLMENT"]]

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
    lin_alg    = ["AM21A","MATH21A", "MATH23B","MATH25B", "MATH55B"]
    multi_calc = ["AM21B","MATH21B", "MATH23A","MATH25A", "MATH55A"]

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

    # same sequence cost
    if len(used_to_satisfy) >= 2:
        class1 = used_to_satisfy[0]
        class2 = used_to_satisfy[1]
        cost += 0.50 * int(class1[0:-1] != class2[0:-1])

    #extra = my_lin_alg | my_multi_calc
    #return (cost, used_to_satisfy, extra)
    return (cost, used_to_satisfy)

def software_cost(courses):
    software = ["CS050", "CS051", "CS061"]
    used_to_satisfy = []

    cost = 2
    for course in software:
        if course in courses:
            used_to_satisfy.append(course)
            cost -= 1

            if cost == 0:
                return (cost, used_to_satisfy)
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
        last_digit = -2 if course[-1] in ["A", "B", "R"] else -1
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
    costs = [math_cost(courses), software_cost(courses), \
             theory_cost(courses), technical_and_breadth_cost(courses)]

    satisfy_cost       = sum(map(lambda x: x[0], costs))
    extra_classes_cost = len(courses) - sum(map(lambda x: len(x[1]), costs))

    return satisfy_cost + extra_classes_cost
