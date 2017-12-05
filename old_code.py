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
