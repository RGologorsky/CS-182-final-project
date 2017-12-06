# testing

# graph og num iter. vs. course requirement cost.

from local_search_restricted_successors import sideways_hill_climbing, naive_hill_climbing
from local_search_many_successors       import sideways_hill_climbing2,naive_hill_climbing2
from first_choice_hill_climbing         import sideways_first_choice,  naive_first_choice
from simulated_annealing                import simulated_annealing
from random_restart                     import random_restart, limited_random_restart 
#from branch_and_bound import *
from helpers import *
from printing import *

from csv_parser import list_to_csv

# pre-req, workload, qscore, enrollemnt
weights = [20, 5, 5, 0]
NUM_REPEATS = 5
best_state, cost_trace, num_iter, time_elapsed  = naive_hill_climbing(weights)

ALGS = [sideways_hill_climbing, naive_hill_climbing,
        sideways_hill_climbing2,naive_hill_climbing2,
        sideways_first_choice, naive_first_choice,
        simulated_annealing]

NAMES= ["Sideways HC-1", "HC-1",
        "Sideways HC-2", "HC-2",
        "Sideways FC HC-2", "Sideways FC", "FC HC-2",
        simulated_annealing]
META = [limited_random_restart]

#from simulated_annealing import *
# ONLY COURSE REQ ===> weights = [0, 0, 0, 0]
MAX_NUM_SIDEWAYS = 0
MAX_NUM_RESTARTS = 10

NUM_REPEATS = 5 # TODO
# compare avg. costs of sol

results = []

weights = get_random_weights()
assignment = get_random_assignment()

all_cost_traces = []
all_times = []
all_num_iter = []

NAIVE_ALGS = [naive_hill_climbing, naive_hill_climbing2, 
                naive_first_choice,
                simulated_annealing]
NAMES = ["Naive HC-1", "Naive HC-2", "Naive FC-2", "SA"]
for alg in NAIVE_ALGS:
    (_, cost_trace, num_iter, time_elapsed) = alg(weights, assignment)
    all_cost_traces.append(cost_trace)
    all_times.append(time_elapsed)
    all_num_iter.append(num_iter)

print "all_times: "
print all_times

def safely_get_value(i, alg_index):
    if i >= len(all_cost_traces[alg_index]):
        return 0
    return all_cost_traces[alg_index][i]

csv_list = []
max_num_iter = max(all_num_iter)
for i in xrange(max_num_iter):
    row_dict = {}
    row_dict["Iter"] = i

    for alg_index in xrange(len(NAIVE_ALGS)):
        name = NAMES[alg_index]
        if i < len(all_cost_traces[alg_index]):
            row_dict[name] = all_cost_traces[alg_index][i]
    csv_list.append(row_dict)

list_to_csv(csv_list, "naive_algs.csv")


    # DO 1-ITER
    # results[alg(weights)


    # COMPARE WITH REPEATED ITER








# result = limited_random_restart(sideways_first_choice, weights, MAX_NUM_SIDEWAYS, MAX_NUM_RESTARTS)
# print result

# result = limited_random_restart(simulated_annealing, weights, MAX_NUM_SIDEWAYS, MAX_NUM_RESTARTS)
# print result
