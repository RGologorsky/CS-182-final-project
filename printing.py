# PRINTING FUNCTIONS

from cost_functions import *
from constants      import *

def course_list_to_times(course_list):
    if len(course_list) == 0:
        return "None."

    def add_colon_to_time(time): 
        return time[:-4] + ":" + time[-4:]
    
    class_times = ""

    for index, course in enumerate(course_list):
        days = courses[course]["CLOCKDAYS"] 
        start, end = courses[course]["CLOCKSTART"], courses[course]["CLOCKEND"]
        start, end = add_colon_to_time(start), add_colon_to_time(end)

        if days == "": s = "(Anytime)"
        else:          s = "(" + days + " " + start + " - " + end + ")"
            
        class_times += "{0:23}".format(s)
        if index != len(course_list) - 1:
            class_times += ", "

    return class_times + "."

def course_list_to_string(course_list):
    if len(course_list) == 0:
        return "None."
    
    res = ""
    for index, course in enumerate(course_list):
        s = course
        res += "{0:8}".format(s)

        if index != len(course_list) - 1:
            res += ", "

    return res + "."

def print_cost(assignment):
    courses = get_flat_courses(assignment)
    m, m_sat = math_cost(courses)
    s, s_sat  = software_cost(courses) 
    th, th_sat  = theory_cost(courses) 
    tb, tb_sat  = technical_and_breadth_cost(courses)

    print "============================= CONCENTRATION REQUIREMENTS ======================="
    print "Math             : ", m, ". Classes Taken: ", course_list_to_string(m_sat)
    print "Software         : ", s, ". Classes Taken: ", course_list_to_string(s_sat)
    print "Theory           : ", th, ". Classes Taken: ", course_list_to_string(th_sat)
    print "Technical/Breadth: ", tb, ". Classes Taken: ", course_list_to_string(tb_sat)

def print_user(res):
    best_state, cost_trace, num_iter, time_elapsed = res
    print_assignment(best_state)
    print "Time Elapsed: {} seconds".format(time_elapsed)

def get_str_workload(semester):
    if len(semester) == 0:
        return "0"

    nums = ""
    total = 0
    for index, c in enumerate(semester):
        if c in courses:
            w = courses[c]["WORKLOAD"]
            total += w
            s = "%2.2f" % w
            if index < len(semester) - 1:
                s += ","
            nums += s
    avg = round(total/len(semester),2)
    total = round(total, 2)

    t = "%2.2f" % total

    return t + " hrs. " + "(" + nums + ")"

    workloads = map(lambda c: courses[c]["WORKLOAD"], semester)

def print_assignment(assignment):
    year = 0

    print "============================= PERSONALIZED SUGGESTION ====================="
    
    for i in xrange(len(assignment)):
        semester = assignment[i]
        even_semester = (i % 2 == 0)
        
        season = "Fall"     if even_semester else "Spring"
        year   = (year + 1) if even_semester else year

        course_list = course_list_to_string(semester)
        course_times = course_list_to_times(semester)

        workload = get_str_workload(semester)

        print "Year {0}, {1:6} : {2:35} Workload: {3:25}. Times: {4}".format(year, season, course_list, workload, course_times)

    print_cost(assignment)
    print("\n")
       

def print_hill_climb(result):
    (assignment, initial_cost, final_cost, MAX_NUM_SIDEWAYS, num_iter, num_plateux, avg_plateux_steps) = result
    print " ====== RESULT of HILL-CLIMBING ======="
    print "INITIAL COST: %d. NOW: %d. MAX_NUM_SIDEWAYS = %d. NUM_PLATEUX = %d. AVG_PLATEUX_STEPS = %2.3f. NUM_ITER = %d." % \
        (initial_cost, final_cost, MAX_NUM_SIDEWAYS, num_plateux, avg_plateux_steps, num_iter)
    print_assignment(assignment)

def short_print(result):
    (assignment, initial_cost, final_cost, MAX_NUM_SIDEWAYS, num_iter, num_plateux, avg_plateux_steps) = result

    print "INITIAL COST: %d. NOW: %d. MAX_NUM_SIDEWAYS = %d. #LOCAL_SEARCH_ITER = %d." % \
        (initial_cost, final_cost, MAX_NUM_SIDEWAYS, num_iter)
    print(assignment)

