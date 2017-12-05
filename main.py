from printing import *
#from branch_and_bound import *
from local_search_restricted_successors import sideways_hill_climbing, naive_hill_climbing
from local_search_many_successors       import sideways_hill_climbing2,naive_hill_climbing2
from first_choice_hill_climbing         import sideways_first_choice,  naive_first_choice
from simulated_annealing                import simulated_annealing
from random_restart                     import random_restart, limited_random_restart 
#from simulated_annealing import *


# get_courses_dict()

# print overlap("CS182", "CS182")
# print_assignment(get_random_assignment())
#result = sideways_hill_climbing(get_random_assignment(), [1, 0, 0, 0, 0])
#print_hill_climb(result)

# ONLY COURSE REQ
weights = [0, 0, 0, 0]
MAX_NUM_SIDEWAYS = 0
MAX_NUM_RESTARTS = 20

result = limited_random_restart(sideways_first_choice, weights, MAX_NUM_SIDEWAYS, MAX_NUM_RESTARTS)
print result

result = limited_random_restart(simulated_annealing, weights, MAX_NUM_SIDEWAYS, MAX_NUM_RESTARTS)
print result
