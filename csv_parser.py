import csv
from pprint import *

from constants import *
# TO DO: NORMALIZE SPREADSHEET
# courses = dict()

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

def prereq_parser(s):
    if len(s) == 0 or s == "[]" or s == "CHECK":
        return []
    return s

def convert_to_float(num, key):
    WORKLOAD_DEFAULT = 5
    Q_DEFAULT = 3.5
    ENROLLMENT_DEFAULT = 25

    try:
        return float(num)
    except:
        if key == "WORKLOAD":   return WORKLOAD_DEFAULT
        if key == "Q":          return Q_DEFAULT
        if key == "ENROLLMENT": return ENROLLMENT_DEFAULT 

def get_courses_dict():

    with open('all_courses.csv', mode='r') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            # print "row", row
            course = row["COURSE"]

            row["PREREQS"] = prereq_dict[course]

            row["WORKLOAD"]   = convert_to_float(row["WORKLOAD"], "WORKLOAD")
            row["Q"]          = convert_to_float(row["Q"], "Q")
            row["ENROLLMENT"] = int(convert_to_float(row["ENROLLMENT"], "ENROLLMENT"))

            row["CLOCKSTART"] = row["START"]
            row["CLOCKEND"]   = row["END"]
            row["CLOCKDAYS"]  = row["DAYS"]

            row["DAYS"]  = set(row["DAYS"])

            row["START"] = get_military_time(row["START"])
            row["END"]   = get_military_time(row["END"])

            courses[course] = row


# overwrites
def list_to_csv(csv_list, filename, headers=None):
    if len(csv_list) == 0:
        return
    if not headers:
        headers = csv_list[0].keys()

    with open(filename, 'wb') as f:  # Just use 'w' mode in 3.x
        writer = csv.DictWriter(f, headers)
        writer.writeheader()
        writer.writerows(csv_list)

# adict = [{"alg1": 5, "alg2": 6},{"alg1": 1, "alg2": 3}, {"alg1": 2, "alg2": 4}] 
# dict_to_csv(adict, "t.csv")
# get_courses_dict()
# prereq_dict = dict()
# print dict(courses)
# for course in dict(courses):
#     print course
#     prereq_dict[course] = courses[course]['PREREQS']
# pprint(prereq_dict)
# pprint(courses)
