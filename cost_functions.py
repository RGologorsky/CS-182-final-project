# Return the cost of an assignment


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

# def get_cost():

