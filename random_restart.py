from first_choice_hill_climbing import *
from local_search_with_many_successors import *
from local_search_with_restricted_successors import *

from helpers import *
# from cost_functions import *


def random_restart(alg, weights):
    num_iter = 0
    state = get_random_assignment()
    cost = alg(state, weights)

    while cost != 0:
        state = get_random_assignment()
        cost = alg(state, weights)
        num_iter += 1
    return num_iter

random_restart(sideways_hill_climbing, [1, 0, 0, 0, 0])
