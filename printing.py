# PRINTING FUNCTIONS

from reqs import *

def course_list_to_string(course_list):
    res = ""
    for course in course_list:
        res += course 
        res += ", "
    return res[:-2] + "."

def print_cost(assignment):
    courses = get_flat_courses(assignment)
    m = math_cost(courses)
    s = software_cost(courses) 
    th = theory_cost(courses) 
    tec = technical_cost(courses)
    b = breadth_cost(courses)

    print "========== COSTS = #Classes Needed ========"
    print "Math     : ", m[0], ". Classes Taken: ", course_list_to_string(m[1])
    print "Software : ", s[0], ". Classes Taken: ", course_list_to_string(s[1])
    print "Theory   : ", th[0], ". Classes Taken: ", course_list_to_string(th[1])
    print "Technical: ", tec[0], ". Classes Taken: ", course_list_to_string(tec[1])
    print "Breadth  : ",    b[0], ". Classes Taken: ", course_list_to_string(b[1])

def print_assignment(assignment):
    year = 0

    print "======= POSSIBLE SCHEDULE ========"
    
    for i in xrange(len(assignment)):
        semester = assignment[i]
        even_semester = (i % 2 == 0)
        
        season = "Fall"     if even_semester else "Spring"
        year   = (year + 1) if even_semester else year

        print "Year %d, %7s Classes: %s" % (year, season, course_list_to_string(semester))

    print_cost(assignment)
    print("\n")
       

def print_hill_climb(result):
    (assignment, MAX_NUM_SIDEWAYS, num_iter, num_plateux) = result
    print " ====== RESULT of HILL-CLIMBING ======="
    print "MAX_NUM_SIDEWAYS = %d. NUM_PLATEUX = %d. NUM_ITER = %d." % \
        (MAX_NUM_SIDEWAYS, num_plateux, num_iter)
    print_assignment(assignment)

