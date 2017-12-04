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

# get_courses_dict()
# pprint(courses)

