# def is_in_course_group()

def get_flat_courses(assignment):
    return [course for semester in assignment for course in semester]

def common(course_list, courses):
    return set(course_list) & set(courses)

def math_cost(courses):
    lin_alg    = ["AM21A","MATH21A", "MATH23A","MATH25B", "MATH55B"]
    multi_calc = ["AM21B","MATH21B", "MATH23B","MATH25A", "MATH55A"]

    matches1 = common(lin_alg, courses) 
    matches2 = common(multi_calc, courses) 

    cost = 2
    if len(matches1) >= 1: cost -= 1
    if len(matches2) >= 1: cost -= 1

    return (cost, matches1 | matches2)
    
def software_cost(courses):
    software = ["CS50", "CS51", "CS61"]

    matches = common(software, courses) 
    return (max(0, 2 - len(matches)), matches)
   

def theory_cost(courses):
    theory = filter(lambda x: (x == "AM106" or x == "AM107") or \
                                (x[:2] == "CS" and x[-2] == "2"),
                            courses)

    matches = common(theory, courses) 
    num_matches = len(matches)
    
    if "CS125" in matches:
        if "CS121" in matches or "CS124" in matches: 
            # one class doesn't count, adds 1 to cost
            return (max(0, (2 - num_matches + 1)), matches)
        else:
            return (max(0, 2 - num_matches), matches) # everything counts

    if "CS121" in matches:
        return (max(0, 2 - num_matches), matches)

    # we need CS121, adds 1 to cost
    return (max(0, 2 - num_matches + 1), matches)

def technical_cost(courses):
    technical_courses = []

    noncs = ["STAT110", "MATH154", "AM106", "AM107", "AM120", "AM121", "ES50", "ES52"]
    intro = ["CS50", "CS51", "CS61"]

    if common(intro, courses) == set(intro):
        technical_courses.append("CS61") # TO DO: RETURN TO THIS

    for course in courses:
        is_cs = (course[:2] == "CS")

        if is_cs and course not in ["CS1", "CS20", "CS50", "CS51", "CS61"]:
            technical_courses.append(course)
        if not is_cs and course in noncs:
            technical_courses.append(course)

    cost = max(0, 4 - len(technical_courses))
    return (cost, technical_courses)

def breadth_cost(courses):
    _, technical_courses = technical_cost(courses)
    matches = []
    num_breadth = 0
    seen = []
    for course in technical_courses:
        is_cs = (course[:2] == "CS")
        if is_cs:
            course_penultimate = course[-2]
            if course_penultimate not in seen:
                if course_penultimate not in ["0", "1", "2"]:
                    seen.append(course_penultimate)
                    matches.append(course)
                    num_breadth += 1
                else:
                    # TO DO
                    pass
    return (max(0, 2 - num_breadth), matches)


def get_req_cost(assignment):
    courses = get_flat_courses(assignment)
    return math_cost(courses)[0] + software_cost(courses)[0] \
            + theory_cost(courses)[0] \
            + technical_cost(courses)[0] + breadth_cost(courses)[0]
       



def basic_req(assignment):
    req = copy.deepcopy(requirements)

    flat_courses = get_flat_courses(assignment)
    for course in flat_courses:
        course = course[0].upper()
        used = False
        for cat in req:
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

# def honor_req(assignment):
