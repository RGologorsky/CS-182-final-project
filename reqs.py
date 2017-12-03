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

def fulfill_

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
