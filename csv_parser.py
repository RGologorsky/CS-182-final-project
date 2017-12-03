import csv
from pprint import *

# TO DO: NORMALIZE SPREADSHEET
courses = dict()

# converts "130PM" -> 1330, etc.

def get_military_time(time):
    if time == "":
        return -1

    hr = int(time[:-4])
    is_pm = (time[-2:] == "PM")

    if is_pm and hr != 12:
        hr += 12
    military_time = str(hr) + time[-4:-2]
    return int(military_time)


def get_courses_dict():

    with open('all_courses.csv', mode='r') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            print "row", row

            row["DAYS"]  = set(row["DAYS"])
            row["START"] = get_military_time(row["START"])
            row["END"]   = get_military_time(row["END"])
            
            course = row["COURSE"]
            courses[course] = row

get_courses_dict()
pprint(courses)

def overlap(course1, course2):

    if courses[course1]["SEMESTER"] != courses[course2]["SEMESTER"]:
        return False

    days1 = courses[course1]["DAYS"]
    days2 = courses[course2]["DAYS"]

    # handles when no days: overlap is 0
    if len(days1 & days2) == 0:
        return False

    start1 = courses[course1]["START"]
    end1   = courses[course1]["END"]

    start2 = courses[course2]["START"]
    end2   = courses[course2]["END"]

    # class 1 first or class 2 first
    return (start1 < start2 and end1 < start2) or \
            (start2 < start1 and end2 < start1)


