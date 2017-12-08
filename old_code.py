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

def compare_naive_algs(file_index, NUM_TRIALS=11):
    # compare avg. costs of sol
    file_name = "naive_algs" + str(file_index) + ".csv"
    MAX_NUM_ITER = 5000


    NAIVE_ALGS = [naive_hill_climbing, naive_hill_climbing2, 
                    naive_first_choice, naive_first_choice2,
                    simulated_annealing]
    NAMES = ["HC-1", "HC-2", "FC-1", "FC-2", "SA"]
    NUM_ALGS = len(NAIVE_ALGS)
    # for i in range(len(NAMES)):
    #     NAMES[i] = NAMES

    alg_all_avg_cost_traces = [[0 for _ in range(NUM_ALGS)] for _ in range(NUM_TRIALS)]
    
    file2 = "times-and-costs" + str(file_index) + ".csv"
    alg_all_costs = [[-1 for _ in range(NUM_ALGS)] for _ in range(NUM_TRIALS)]
    alg_all_times = [[-1 for _ in range(NUM_ALGS)] for _ in range(NUM_TRIALS)]

    # get costs and times over different weights & assignments
    for trial in range(NUM_TRIALS):
        weights = get_random_weights()
        assignment = get_random_assignment()

        costs = [0 for _ in range(NUM_ALGS)]
        times = [0 for _ in range(NUM_ALGS)]


        for alg_index in range(NUM_ALGS):  
            alg = NAIVE_ALGS[alg_index]
            (_, cost_trace, _, time_elapsed) = \
                alg(weights, assignment, MAX_NUM_ITER = MAX_NUM_ITER)
            cost = cost_trace[-1]

            for i in xrange(len(cost_trace)):
                alg_all_avg_cost_traces[alg_index][i] += cost_trace[i] * 1.0/NUM_TRIALS

            alg_all_costs[trial][alg_index] = cost
            alg_all_times[trial][alg_index] = time_elapsed

    # for each alg, get minimum, maximum, & median cost/time trace over the trials
    alg_min_costs = [-1 for _ in range(NUM_ALGS)]
    alg_max_costs = [-1 for _ in range(NUM_ALGS)]
    alg_avg_costs = [-1 for _ in range(NUM_ALGS)]

    alg_min_times = [-1 for _ in range(NUM_ALGS)]
    alg_max_times = [-1 for _ in range(NUM_ALGS)]
    alg_med_times = [-1 for _ in range(NUM_ALGS)]

    # for each alg, get min, max, and median cost per trial
    for alg in range(NUM_ALGS):
        min_costs = [-1 for _ in range(MAX_NUM_ITER)]
        max_costs = [-1 for _ in range(MAX_NUM_ITER)]
        med_costs = [-1 for _ in range(MAX_NUM_ITER)]

        min_times = [-1 for _ in range(MAX_NUM_ITER)]
        max_times = [-1 for _ in range(MAX_NUM_ITER)]
        med_times = [-1 for _ in range(MAX_NUM_ITER)]

        for i in range(MAX_NUM_ITER):
            sorted_i_vals = map(lambda trial: safe_cost_lookup(trial, alg, i), \
                                range(NUM_TRIALS))
            sorted_i_vals.sort()

            min_costs[i] = sorted_i_vals[1]
            max_costs[i] = sorted_i_vals[-1]
            med_costs[i] = sorted_i_vals[NUM_TRIALS/2]        

            sorted_i_vals = map(lambda trial: alg_all_times[trial][alg], \
                                range(NUM_TRIALS))
            sorted_i_vals.sort()

            min_times[i] = sorted_i_vals[1]
            max_times[i] = sorted_i_vals[-1]
            med_times[i] = sorted_i_vals[NUM_TRIALS/2]

        alg_min_costs[alg] = min_costs
        alg_max_costs[alg] = max_costs
        alg_med_costs[alg] = med_costs

        alg_min_times[alg] = min_times
        alg_max_times[alg] = max_times
        alg_med_times[alg] = med_times


    csv_list = []
    results = [alg_med_costs, alg_min_costs, alg_max_costs, \
                alg_med_times, alg_min_times, alg_max_times]

    for i in range(MAX_NUM_ITER):
        for j in range(len(results)):
            row_dict = {}
            title = ["Median-", "Min-", "Max-"][j%3] + ["Cost", "Time"][j/3]
            for alg_index in xrange(len(NAIVE_ALGS)):
                title = title + NAMES[alg_index]
                row_dict[title] = results[j][alg_index][i]
                csv_list.append(row_dict)

    list_to_csv(csv_list, file_name)
