from printing import *
from branch_and_bound import *
from local_search import *
from random import *
from helpers import *

from csv_parser import *

# get_courses_dict()

# print overlap("CS182", "CS182")
# print_assignment(get_random_assignment())
result = sideways_hill_climbing2(get_random_assignment())
print_hill_climb(result)
