# PRINTING FUNCTIONS

from cost_functions import *
from constants      import *

def course_list_to_times(course_list):

    def add_colon_to_time(time): 
        return time[:-4] + ":" + time[-4:]
    
    class_times = ""

    for course in course_list:
        days = courses[course]["CLOCKDAYS"] 
        start, end = courses[course]["CLOCKSTART"], courses[course]["CLOCKEND"]
        start, end = add_colon_to_time(start), add_colon_to_time(end)

        if days == "": s = "(Anytime), "
        else:          s = "(" + days + " " + start + " - " + end + "), "
            
        class_times += ("%-25s" % s)

    return class_times[:-2] + "."

def course_list_to_string(course_list):
    if len(course_list) == 0:
        return "None."
    
    res = ""
    for course in course_list:
        s = course + ", "
        res += ("%-7s" % s)

    return res[:-2] + "."

def print_cost(assignment):
    courses = get_flat_courses(assignment)
    m, m_sat = math_cost(courses)
    s, s_sat  = software_cost(courses) 
    th, th_sat  = theory_cost(courses) 
    tb, tb_sat  = technical_and_breadth_cost(courses)

    print "========== COSTS = #Classes Needed ========"
    print "Math             : ", m, ". Classes Taken: ", course_list_to_string(m_sat)
    print "Software         : ", s, ". Classes Taken: ", course_list_to_string(s_sat)
    print "Theory           : ", th, ". Classes Taken: ", course_list_to_string(th_sat)
    print "Technical/Breadth: ", tb, ". Classes Taken: ", course_list_to_string(tb_sat)

def print_assignment(assignment):
    year = 0

    print "======= POSSIBLE SCHEDULE ========"
    
    for i in xrange(len(assignment)):
        semester = assignment[i]
        even_semester = (i % 2 == 0)
        
        season = "Fall"     if even_semester else "Spring"
        year   = (year + 1) if even_semester else year

        print "Year %d, %-10s : %-35s Times: %-s" % (year, season, course_list_to_string(semester), course_list_to_times(semester))

    print_cost(assignment)
    print("\n")
       

def print_hill_climb(result):
    (assignment, initial_cost, final_cost, MAX_NUM_SIDEWAYS, num_iter, num_plateux, avg_plateux_steps) = result
    print " ====== RESULT of HILL-CLIMBING ======="
    print "INITIAL COST: %d. NOW: %d. MAX_NUM_SIDEWAYS = %d. NUM_PLATEUX = %d. AVG_PLATEUX_STEPS = %2.3f. NUM_ITER = %d." % \
        (initial_cost, final_cost, MAX_NUM_SIDEWAYS, num_plateux, avg_plateux_steps, num_iter)
    print_assignment(assignment)

