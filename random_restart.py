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
    res = alg(weights, MAX_NUM_SIDEWAYS)
    state, cost = res[0], res[2]

    while int(cost) != 0:
        # print "Iter %d: cost = %f" % (num_iter, cost)
        res = alg(weights, MAX_NUM_SIDEWAYS)
        state, cost = res[0], res[2]
        num_iter += 1
    time_elapsed = round(time.time() - start_time, 2)
    return (num_iter, time_elapsed)

def limited_random_restart(alg, weights, MAX_NUM_SIDEWAYS=100, MAX_NUM_RESTARTS=20, assignment=None):
    #print "in limited random restart. #restarts = ", MAX_NUM_ITER - 1
    start_time = time.time()
    num_restarts = 0

    best_state, indiv_cost_trace, indiv_num_iter, indiv_time_elapse = alg(weights, MAX_NUM_SIDEWAYS=MAX_NUM_SIDEWAYS, assignment=assignment)
    best_cost = indiv_cost_trace[-1]
    cost_trace = [best_cost]

    #print "cost, ", cost_trace

    while num_restarts < MAX_NUM_RESTARTS and best_cost != 0:
        #print "Iter %d: cost = %f" % (num_iter, best_cost)
        state,indiv_cost_trace, indiv_num_iter, indiv_time_elapsed = alg(weights, MAX_NUM_SIDEWAYS=MAX_NUM_SIDEWAYS)
        cost = indiv_cost_trace[-1]
        #print "cost, ", cost_trace

        # keep moving
        if cost <= best_cost:
            best_cost = cost
            best_state = state
        cost_trace.append(best_cost)
        num_restarts += 1

    time_elapsed = round(time.time() - start_time, 2)
    return (best_state, cost_trace, num_restarts, time_elapsed)

def random_restart_sideways_hc():
    return random_restart(sideways_hill_climbing, [1, 0, 0, 0, 0], MAX_NUM_SIDEWAYS = 0)

# print(timeit.timeit(random_restart_sideways_hc))
