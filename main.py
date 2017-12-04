from printing import *
from branch_and_bound import *


result = hill_climbing([
                        ["CS109"], ["CS1"], 
                        ["CS182"], ["CS125"], 
                        ["MATH21A"], ["CS181"],
                        ["AM107"], ["MATH23A"]
                       ])
print_hill_climb(result)
