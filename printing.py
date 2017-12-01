# PRINTING FUNCTIONS

def course_list_to_string(course_list):
    res = ""
    for course in course_list:
        res += course 
        res += ", "
    return res[:-2] + "."

def print_assignment(assignment):
    year = 0
    
    print "======= POSSIBLE SCHEDULE ========"
    
    for i in xrange(len(assignment)):
        semester = assignment[i]
        even_semester = (i % 2 == 0)
        
        season = "Fall"     if even_semester else "Spring"
        year   = (year + 1) if even_semester else year

        print "Year %d, %s: %s" % (year, season, course_list_to_string(semester))

    print "\n"
