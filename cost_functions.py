# Return the cost of an assignment

MAX_COST = float("inf")


def get_feature_cost(course, feature):
    if course in courses and feature in courses[course]:
        return courses[course][feature]
    return 0

def get_pair_cost(course1, course2):
    if course1 in pair_costs and course2 in pair_costs[course1]:
        return pair_costs[course1][course2]
    return 0

def workload_cost(assignment):
    return sum(map(lambda c: get_feature_cost(c, "workload"), assignment))

def qscore_cost(assignment):
    return sum(map(lambda c: 5 - get_feature_cost(c, "qscore"), assignment))

def enrollment_cost(assignment):
    return sum(map(lambda c: get_feature_cost(c, "enrollment"), assignment))   


# requirements implemented as lists with number from the set needed to fulfill conc. req)
requirements = {
    'software': (["CS50", "CS51", "CS61"], 2), 
    'theory1': (["CS121"], 1), 
    'theory2': (["CS124", "AM107"], 1),
    }

def at_least_n(n, course_list, courses):
    num_done = 0

    for course in course_list:
        if course in courses:
            num_done += 1

    return (num_done >= n)

def fulfill_math(courses):
    lin_alg    = ["AM21a","MATH21a", "MATH23a","MATH25b", "MATH55b"]
    multi_calc = ["AM21b","MATH21b", "MATH23b","MATH25a", "MATH55a"]
    return at_least(1, lin_alg, courses) and at_least(1, multi_calc, courses)

def fulfill_software(courses):
    software = ["CS50", "CS51", "CS61"]
    return at_least(2, software, courses)

def basic_req(assignment):
    req = copy.deepcopy(requirements)
    flat_courses = [course for semester in assignment for course in semester]

    for course in assignment:
        course = course[0].upper()
        used = False
        for cat in req:
            reqs = req[cat]
            if course in reqs[0] and reqs[1] > 0:
                        used = True
                        reqs[0].remove(course)
                        num_left = reqs[1] - 1
                        req[cat] = (reqs[0], num_left)
                if used == True:
                    continue
    fulfilled = True
    for cat in req:
        if req[cat][1] != 0:
            fulfilled = False
            break
    return fulfilled

def honor_req(assignment):

def get_cost():
