# returns successor state of given action type (add course, mutate, delete)
# returns lowest cost successor state of given action - add, mutate, delete
def get_successor_many_type2(assignment, weights, add_index, del_index, change_type):

    #  add course (type 0), delete course (type 1), muate course (type 2)

    if change_type == 0: # adding a course
        if len(assignment[add_index]) == 4: # can't add if taking 4 courses
            return (None, float("inf"))

        possible_courses = new_course_domain(add_index, assignment)
        possible_assignments = map(lambda x: add_to_assignment(assignment, add_index, x), possible_courses)

        if len(possible_assignments) == 0:
            return (None, float("inf"))

        assignment_costs = map(lambda x: (x, get_cost(x, weights)), possible_assignments)
        return min(assignment_costs, key = lambda (x,c): c)

    if change_type == 1: # deleting a course
        if len(assignment[del_index]) == 0: # can't delete if none
            return (None, float("inf"))

        # possibilities for the course index to delete.
        possible_course_indices = range(len(assignment[del_index]))
        possible_assignments = map(lambda x: del_to_assignment(assignment, del_index, x), possible_course_indices)

        if len(possible_assignments) == 0:
            return (None, float("inf"))

        assignment_costs = map(lambda x: (x, get_cost(x, weights)), possible_assignments)
        return min(assignment_costs, key = lambda (x,c): c)

    if change_type == 2: # mutation: = delete from possible deletes, then add

        # for mutation, we get delete states and add over deletes.
        # possibilities for the course index to delete.
        possible_course_indices = range(len(assignment[del_index]))
        if len(possible_course_indices) == 0: # empty assignment
            return (None, float("inf"))

        possible_assignments = map(lambda x: del_to_assignment(assignment, del_index, x), possible_course_indices)

        add_assignment_costs = map(lambda a: get_successor_type2(a, weights, add_index, -1, 0), possible_assignments)
        return min(add_assignment_costs, key = lambda (x,c): c)

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
    
def get_successor_type2(assignment, weights, semester_index, change_type, curr_cost):

    #  add course (type 0), delete course (type 1), muate course (type 2)

    if change_type == 0: # adding a course
        if len(assignment[semester_index]) == 4: # can't add if taking 4 courses
            return (None, float("inf"))

        possible_courses = new_course_domain(semester_index, assignment)
        possible_assignments = map(lambda x: add_to_assignment(assignment, semester_index, x), possible_courses)
        
        if len(possible_assignments) == 0:
            return (None, float("inf"))

        for a in possible_assignments:
            c = get_cost(a, weights)
            if c < curr_cost:
                return a, c
        return a, curr_cost

    if change_type == 1 or change_type == 2: # deleting a course
        if len(assignment[semester_index]) == 0: # can't mutate/delete if none
            return (None, float("inf"))

        # possibilities for the course index to delete.
        possible_course_indices = range(len(assignment[semester_index]))
        possible_assignments = map(lambda x: del_to_assignment(assignment, semester_index, x), possible_course_indices)
        
        if len(possible_assignments) == 0:
            return (None, float("inf"))

        if change_type == 1: # we just delete, and are done.
            for a in possible_assignments:
                c = get_cost(a, weights)
                if c < curr_cost:
                    return a, c
            return a, curr_cost

        # for mutation, we now check add back a course.
        for a in possible_assignments:
            a_new, c_new = get_successor_type2(a, weights, semester_index, 0, curr_cost)
            if c_new < curr_cost:
                return a_new, c_new
        return assignment, curr_cost


# def honor_req(assignment):
