# testing

# graph og num iter. vs. course requirement cost.

from local_search_restricted_successors import sideways_hill_climbing, naive_hill_climbing,  get_greedy_successor
from local_search_many_successors       import sideways_hill_climbing2,naive_hill_climbing2, get_greedy_successor2, get_best_mut_successor, get_best_del_successor, get_best_mut_successor
from first_choice_hill_climbing         import sideways_first_choice,  naive_first_choice, sideways_first_choice2, naive_first_choice2, get_first_choice_successor2, get_first_choice_mut_successor, get_first_choice_del_successor, get_first_choice_mut_successor
from simulated_annealing                import simulated_annealing
from random_restart                     import random_restart, limited_random_restart 
#from branch_and_bound import *
from helpers import *
from printing import *

from pprint import pprint
from csv_parser import list_to_csv
from copy import deepcopy
import numpy

# pre-req, workload, qscore, enrollemnt
#weights = [20, 5, 5, 0]
#NUM_REPEATS = 5
#best_state, cost_trace, num_iter, time_elapsed  = naive_hill_climbing(weights)

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

# test_mutate_first_choice()

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
# def get_avg(NUM_REPEATS):
#     avg_cost_trace = None
#     avg_time_elapsed = 
#     for i in NUM_REPEATS:


def compare_naive_algs(file_index, NUM_TRIALS=5):
    # compare avg. costs of sol
    file_name = "rr_comparison" + str(file_index) + ".csv"
    results = []

    weights = get_random_weights()
    assignment = get_random_assignment()

    all_cost_traces = []
    all_times = []
    all_num_iter = []

    NAIVE_ALGS = [naive_hill_climbing, naive_hill_climbing2, 
                    naive_first_choice,
                    simulated_annealing]
    NAMES = ["HC-1", "HC-2", "FC-2", "SA"]
    # for i in range(len(NAMES)):
    #     NAMES[i] = NAMES[i]


    for alg in NAIVE_ALGS:
        (_, cost_trace, num_iter, time_elapsed) = alg(weights, assignment)

        all_cost_traces.append(cost_trace)
        all_times.append(time_elapsed)
        all_num_iter.append(num_iter)

    print "all_times: "
    print all_times


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

    list_to_csv(csv_list, file_name)


    # DO 1-ITER
    # results[alg(weights)


    # COMPARE WITH REPEATED ITER


def many_compare_naive_algs():
    for i in xrange(3):
        compare_naive_algs(file_index=i)

def compare_random_restarts(file_index, NUM_TRIALS=100):
    # compare avg. costs of sol
    file_name = "random_restarts" + str(file_index) + ".csv"
    results = []
    MAX_NUM_RESTARTS = 1


    NAIVE_ALGS = [naive_hill_climbing, sideways_hill_climbing,
                    naive_hill_climbing2, sideways_hill_climbing2,
                    naive_first_choice, 
                    naive_first_choice2,
                    simulated_annealing]
    NAMES = ["HC-1", "S-HC-1", 
             "HC-2", "S-HC-2", 
             "FC-1", 
             "FC-2",
             "SA"]
    NUM_ALGS = len(NAIVE_ALGS)
    # for i in range(len(NAMES)):
    #     NAMES[i] = NAMES

    # alg_all_costs[alg_index][num_restarts] = [trial 1... trial n] cost values
    alg_all_costs = [[[-1 for _ in range(NUM_TRIALS)] for _ in range(MAX_NUM_RESTARTS)] for _ in range(NUM_ALGS)]
    alg_all_times = [[[-1 for _ in range(NUM_TRIALS)] for _ in range(MAX_NUM_RESTARTS)] for _ in range(NUM_ALGS)]


    # get costs and times over different weights & assignments
    for trial in range(NUM_TRIALS):
        print "in trial ", trial
        weights = get_random_weights()
        assignment = get_random_assignment()

        for alg_index in range(NUM_ALGS):  
            alg = NAIVE_ALGS[alg_index]
            for i in range(MAX_NUM_RESTARTS):   
                print "#restarts ", str(i), " testing alg ", NAMES[alg_index]   
                (_, cost_trace, _, time_elapsed) = \
                    limited_random_restart(alg, weights, assignment = assignment, \
                                            MAX_NUM_RESTARTS = MAX_NUM_RESTARTS - 1)
                cost = cost_trace[-1]

                alg_all_costs[alg_index][i][trial] = cost
                alg_all_times[alg_index][i][trial] = time_elapsed
                print "cost ", cost, ", time elapsed: ", time_elapsed
                #pprint(alg_all_costs)
    pprint(alg_all_costs)
    #pprint(alg_all_times)
    # for each alg, get minimum, maximum, & median cost/time trace over the trials
    # alg_min_costs[alg_index][num restarts] = min cost trial
    
    # alg_min_costs = [[-1 for _ in range(MAX_NUM_RESTARTS)] for _ in range(NUM_ALGS)]
    alg_med_costs = [[-1 for _ in range(MAX_NUM_RESTARTS)] for _ in range(NUM_ALGS)]
    alg_std_costs = [[-1 for _ in range(MAX_NUM_RESTARTS)] for _ in range(NUM_ALGS)]

    alg_med_times = [[-1 for _ in range(MAX_NUM_RESTARTS)] for _ in range(NUM_ALGS)]
    alg_std_times = [[-1 for _ in range(MAX_NUM_RESTARTS)] for _ in range(NUM_ALGS)]
    # alg_med_times = [[-1 for _ in range(MAX_NUM_RESTARTS)] for _ in range(NUM_ALGS)]

    # for each alg, get min, max, and median cost per trial
    for alg_index in range(NUM_ALGS):

        for i in range(MAX_NUM_RESTARTS):
            # calculate the std of the trials
            costs_arr = numpy.array(alg_all_costs[alg_index][i])
            alg_med_costs[alg_index][i] = numpy.median(costs_arr)
            alg_std_costs[alg_index][i] = numpy.std(costs_arr)

            times_arr = numpy.array(alg_all_times[alg_index][i])
            alg_med_costs[alg_index][i] = numpy.median(times_arr)
            alg_std_costs[alg_index][i] = numpy.std(times_arr)
            # sort the trials so that now they are in increasing cost
            # sorted_i_vals = alg_all_costs[alg_index][i]
            # sorted_i_vals.sort()

            # alg_min_costs[alg_index][i] = sorted_i_vals[0]
            # alg_max_costs[alg_index][i] = sorted_i_vals[-1]
            # alg_med_costs[alg_index][i] = sorted_i_vals[NUM_TRIALS/2]        

            # sorted_i_vals = alg_all_times[alg_index][i]
            # sorted_i_vals.sort()

            # alg_min_times[alg_index][i] = sorted_i_vals[0]
            # alg_max_times[alg_index][i] = sorted_i_vals[-1]
            # alg_med_times[alg_index][i] = sorted_i_vals[NUM_TRIALS/2]


    csv_list = []
    results = [alg_med_costs, alg_std_costs, \
                alg_med_times, alg_std_times]
    # results = [alg_med_costs, alg_min_costs, alg_max_costs, \
    #             alg_med_times, alg_min_times, alg_max_times]

    pprint(results)
    headers = []
    for i in range(MAX_NUM_RESTARTS):
        row_dict = {}
        for j in range(len(results)):
            title = ["Med-", "Std-"][j%2] + ["Cost-", "Time-"][j/2]
            for alg_index in xrange(len(NAIVE_ALGS)):
                name = title + NAMES[alg_index]
                headers.append(name)
                row_dict[name] = results[j][alg_index][i]
        csv_list.append(row_dict)

    list_to_csv(csv_list, file_name, headers)

def safe_cost_lookup(trial, alg, i):
            if i < len(alg_all_costs[trial][alg]):
                return alg_all_costs[trial][alg][i]
            return 0

def compare_naive_algs(file_index, NUM_TRIALS=11):
    # compare avg. costs of sol
    file_name = "naive_algs" + str(file_index) + ".csv"
    MAX_NUM_ITER = 5000


    NAIVE_ALGS = [naive_hill_climbing, naive_hill_climbing2, 
                    naive_first_choice, naive_first_choice2,
                    simulated_annealing]
    NAMES = ["HC-1", "HC-2", "FC-1", "FC-2", "SA"]
    NUM_ALGS = len(NAIVE_ALGS)
    # for i in range(len(NAMES)):
    #     NAMES[i] = NAMES

    alg_all_avg_cost_traces = [[0 for _ in range(NUM_ALGS)] for _ in range(NUM_TRIALS)]
    
    file2 = "times-and-costs" + str(file_index) + ".csv"
    alg_all_costs = [[-1 for _ in range(NUM_ALGS)] for _ in range(NUM_TRIALS)]
    alg_all_times = [[-1 for _ in range(NUM_ALGS)] for _ in range(NUM_TRIALS)]

    # get costs and times over different weights & assignments
    for trial in range(NUM_TRIALS):
        weights = get_random_weights()
        assignment = get_random_assignment()

        costs = [0 for _ in range(NUM_ALGS)]
        times = [0 for _ in range(NUM_ALGS)]


        for alg_index in range(NUM_ALGS):  
            alg = NAIVE_ALGS[alg_index]
            (_, cost_trace, _, time_elapsed) = \
                alg(weights, assignment, MAX_NUM_ITER = MAX_NUM_ITER)
            cost = cost_trace[-1]

            for i in xrange(len(cost_trace)):
                alg_all_avg_cost_traces[alg_index][i] += cost_trace[i] * 1.0/NUM_TRIALS

            alg_all_costs[trial][alg_index] = cost
            alg_all_times[trial][alg_index] = time_elapsed

    # for each alg, get minimum, maximum, & median cost/time trace over the trials
    alg_min_costs = [-1 for _ in range(NUM_ALGS)]
    alg_max_costs = [-1 for _ in range(NUM_ALGS)]
    alg_avg_costs = [-1 for _ in range(NUM_ALGS)]

    alg_min_times = [-1 for _ in range(NUM_ALGS)]
    alg_max_times = [-1 for _ in range(NUM_ALGS)]
    alg_med_times = [-1 for _ in range(NUM_ALGS)]

    # for each alg, get min, max, and median cost per trial
    for alg in range(NUM_ALGS):
        min_costs = [-1 for _ in range(MAX_NUM_ITER)]
        max_costs = [-1 for _ in range(MAX_NUM_ITER)]
        med_costs = [-1 for _ in range(MAX_NUM_ITER)]

        min_times = [-1 for _ in range(MAX_NUM_ITER)]
        max_times = [-1 for _ in range(MAX_NUM_ITER)]
        med_times = [-1 for _ in range(MAX_NUM_ITER)]

        for i in range(MAX_NUM_ITER):
            sorted_i_vals = map(lambda trial: safe_cost_lookup(trial, alg, i), \
                                range(NUM_TRIALS))
            sorted_i_vals.sort()

            min_costs[i] = sorted_i_vals[1]
            max_costs[i] = sorted_i_vals[-1]
            med_costs[i] = sorted_i_vals[NUM_TRIALS/2]        

            sorted_i_vals = map(lambda trial: alg_all_times[trial][alg], \
                                range(NUM_TRIALS))
            sorted_i_vals.sort()

            min_times[i] = sorted_i_vals[1]
            max_times[i] = sorted_i_vals[-1]
            med_times[i] = sorted_i_vals[NUM_TRIALS/2]

        alg_min_costs[alg] = min_costs
        alg_max_costs[alg] = max_costs
        alg_med_costs[alg] = med_costs

        alg_min_times[alg] = min_times
        alg_max_times[alg] = max_times
        alg_med_times[alg] = med_times


    csv_list = []
    results = [alg_med_costs, alg_min_costs, alg_max_costs, \
                alg_med_times, alg_min_times, alg_max_times]

    for i in range(MAX_NUM_ITER):
        for j in range(len(results)):
            row_dict = {}
            title = ["Median-", "Min-", "Max-"][j%3] + ["Cost", "Time"][j/3]
            for alg_index in xrange(len(NAIVE_ALGS)):
                title = title + NAMES[alg_index]
                row_dict[title] = results[j][alg_index][i]
                csv_list.append(row_dict)

    list_to_csv(csv_list, file_name)
# many_compare_naive_algs()
compare_random_restarts(file_index=5)
#compare_naive_algs(file_index=5)
# result = limited_random_restart(sideways_first_choice, weights, MAX_NUM_SIDEWAYS, MAX_NUM_RESTARTS)
# print result

# result = limited_random_restart(simulated_annealing, weights, MAX_NUM_SIDEWAYS, MAX_NUM_RESTARTS)
# print result
