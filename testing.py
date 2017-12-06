# testing

# graph og num iter. vs. course requirement cost.

from local_search_restricted_successors import sideways_hill_climbing, naive_hill_climbing,  get_greedy_successor
from local_search_many_successors       import sideways_hill_climbing2,naive_hill_climbing2, get_greedy_successor2, get_best_mut_successor, get_best_del_successor, get_best_mut_successor
from first_choice_hill_climbing         import sideways_first_choice,  naive_first_choice, get_first_choice_successor2, get_first_choice_mut_successor, get_first_choice_del_successor, get_first_choice_mut_successor
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



def test_get_cost():
    assignment = [
                ["AM21A"],[],
                ["MATH55A","CS121","CS105"],["AM107"],
                ["STAT110"], ["CS091R","CS152"],
                ["CS050","CS144R"],["CS051"]]
    # weights = [prereq, workload, qscore, enrollment, concentration, smoothness]
    weights = [0, 0, 0, 0, 100, 1]
    print "initial cost: ", get_cost(assignment, weights)
    get_costs(assignment, weights, printing=True)
    
    better_assignment = [
                ["AM21A"],["MATH55A"],
                ["CS121","CS105"],["AM107"],
                ["STAT110"], ["CS091R","CS152"],
                ["CS050","CS144R"],["CS051"]]
    print "better assignment: ", get_cost(better_assignment, weights)
    get_costs(better_assignment, weights, printing=True)

# test_get_cost()

def test_mutate_greedy():
    assignment = [
                [],[],
                ["CS121","CS105"],[],
                [], [],
                [],[]]
    # assignment = [
    #             ["AM21A"],[],
    #             ["MATH55A","CS121","CS105"],["AM107"],
    #             ["STAT110"], ["CS091R","CS152"],
    #             ["CS050","CS144R"],["CS051"]]
    # weights = [prereq, workload, qscore, enrollment, concentration, smoothness]
    weights = [0, 10, 0, 0, 0, 1]
    print "initial cost: ", get_cost(assignment, weights)
    print_assignment(assignment)
    get_costs(assignment, weights, printing=True)
    print "\n MUTANT:\n"
    new_assignment = get_best_mut_successor(assignment, weights, 1, 2)
    print_assignment(new_assignment[0])
    print "Cost: ", new_assignment[1]
    print "\n"
    get_costs(new_assignment[0], weights, printing=True)

# test_mutate_greedy()

def test_mutate_first_choice():
    assignment = [
                [],[],
                ["CS121","CS105"],[],
                [], [],
                [],[]]
    # assignment = [
    #             ["AM21A"],[],
    #             ["MATH55A","CS121","CS105"],["AM107"],
    #             ["STAT110"], ["CS091R","CS152"],
    #             ["CS050","CS144R"],["CS051"]]
    # weights = [prereq, workload, qscore, enrollment, concentration, smoothness]
    weights = [0, 10, 0, 0, 0, 1]
    print "initial cost: ", get_cost(assignment, weights)
    print_assignment(assignment)
    get_costs(assignment, weights, printing=True)
    print "\n MUTANT:\n"
    new_assignment = get_first_choice_mut_successor(assignment, weights, 1, 2)
    print_assignment(new_assignment[0])
    print "Cost: ", new_assignment[1]
    print "\n"
    get_costs(new_assignment[0], weights, printing=True)

test_mutate_first_choice()

def test_get_successors():
    assignment = [
                ["AM21A"],[],
                ["MATH55A","CS121","CS105"],["AM107"],
                ["STAT110"], ["CS091R","CS152"],
                ["CS050","CS144R"],["CS051"]]
    # weights = [prereq, workload, qscore, enrollment, concentration, smoothness]
    weights = [0, 10, 0, 0, 0, 1]
    best_small_successor = get_greedy_successor(assignment, weights)
    best_big_successor = get_greedy_successor2(assignment, weights)

    print "initial assignment cost", assignment,  get_cost(assignment, weights)
    print "small assignment cost: ", best_small_successor
    print "big assignment cost: ", best_big_successor

# test_get_successors()
#from simulated_annealing import *
# ONLY COURSE REQ ===> weights = [0, 0, 0, 0]
def compare_naive_algs():
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
