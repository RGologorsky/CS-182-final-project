# from first_choice_hill_climbing import *
# from local_search_many_successors import *
from local_search_restricted_successors import *
from helpers import *

import time
import timeit
# from cost_functions import *


def random_restart(alg, weights, MAX_NUM_SIDEWAYS):
    print "in rr"
    start_time = time.time()
    num_iter = 0
    state = get_random_assignment()
    cost = alg(state, weights, MAX_NUM_SIDEWAYS)[2]

    while int(cost) != 0:
        # print "Iter %d: cost = %f" % (num_iter, cost)
        state = get_random_assignment()
        cost = alg(state, weights, MAX_NUM_SIDEWAYS)[2]
        num_iter += 1
    time_elapsed = round(time.time() - start_time, 2)
    return (num_iter, time_elapsed)

def limited_random_restart(alg, weights, MAX_NUM_SIDEWAYS, MAX_NUM_RESTARTS):
    print "in limited rr"
    start_time = time.time()
    num_iter = 0
    best_state = get_random_assignment()
    best_cost = alg(best_state, weights, MAX_NUM_SIDEWAYS)[2]

    while num_iter < MAX_NUM_RESTARTS and best_cost != 0:
        # print "Iter %d: cost = %f" % (num_iter, best_cost)
        state = get_random_assignment()
        cost = alg(state, weights, MAX_NUM_SIDEWAYS)[2]

        # keep moving
        if cost <= best_cost:
            best_cost = cost
            best_state = state
        num_iter += 1

    time_elapsed = round(time.time() - start_time, 2)
    print "time: ", time_elapsed, "num_iter: ", num_iter, ", best cost: ", best_cost
    return (best_state, time_elapsed, num_iter, MAX_NUM_RESTARTS)

def random_restart_sideways_hc():
    print "in restract sideways hc"
    return random_restart(sideways_hill_climbing, [1, 0, 0, 0, 0], MAX_NUM_SIDEWAYS = 0)

# print(timeit.timeit(random_restart_sideways_hc))
