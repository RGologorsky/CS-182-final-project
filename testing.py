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
import numpy as np

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

def get_iqr(data):
    return np.percentile(data, 75) - np.percentile(data, 25)

def compare_random_restarts(file_index, NUM_TRIALS=50):
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
                #print "#restarts ", str(i), " testing alg ", NAMES[alg_index]   
                (_, cost_trace, _, time_elapsed) = \
                    limited_random_restart(alg, weights, assignment = assignment, \
                                            MAX_NUM_RESTARTS = MAX_NUM_RESTARTS - 1)
                cost = cost_trace[-1]

                alg_all_costs[alg_index][i][trial] = cost
                alg_all_times[alg_index][i][trial] = time_elapsed
                #print "cost ", cost, ", time elapsed: ", time_elapsed
                #pprint(alg_all_costs)
    # pprint(alg_all_costs)
    
    # for each alg, get median value & std of cost/time trace over the trials
    # alg_med_costs[alg_index][num restarts] = median cost over the trials
    # alg_std_costs[alg_index][num restarts] = std of cost over the trials
    
    alg_med_costs = [[-1 for _ in range(MAX_NUM_RESTARTS)] for _ in range(NUM_ALGS)]
    alg_std_costs = [[-1 for _ in range(MAX_NUM_RESTARTS)] for _ in range(NUM_ALGS)]

    alg_med_times = [[-1 for _ in range(MAX_NUM_RESTARTS)] for _ in range(NUM_ALGS)]
    alg_std_times = [[-1 for _ in range(MAX_NUM_RESTARTS)] for _ in range(NUM_ALGS)]

    # for each alg, get min, max, and median cost per trial
    for alg_index in range(NUM_ALGS):

        for i in range(MAX_NUM_RESTARTS):
            # calculate the IQR of the trials
            costs_arr = np.array(alg_all_costs[alg_index][i])
            alg_med_costs[alg_index][i] = np.median(costs_arr)
            alg_std_costs[alg_index][i] = get_iqr(costs_arr)

            times_arr = np.array(alg_all_times[alg_index][i])
            alg_med_times[alg_index][i] = np.median(times_arr)
            alg_std_times[alg_index][i] = get_iqr(times_arr)

    csv_list = []
    results = [alg_med_costs, alg_std_costs, \
                alg_med_times, alg_std_times]
    titles = ["Med-Cost-", "IQR-Cost-", "Med-Time-", "IQR-Time-"]
    # pprint(results)
    for i in range(MAX_NUM_RESTARTS):
        row_dict = {}
        headers = []
        for j in range(len(results)):
            title = titles[j]
            for alg_index in xrange(len(NAIVE_ALGS)):
                name = title + NAMES[alg_index]
                headers.append(name)
                row_dict[name] = results[j][alg_index][i]
        csv_list.append(row_dict)

    list_to_csv(csv_list, file_name, headers)

# many_compare_naive_algs()
compare_random_restarts(file_index=25, NUM_TRIALS=100)
#compare_naive_algs(file_index=5)

def compare_cost_traces(file_index, NUM_TRIALS=50):
    print "in compare cost traces"
    # compare avg. costs of sol
    file_name = "compare_cost_traces" + str(file_index) + ".csv"
    results = []


    NAIVE_ALGS = [naive_hill_climbing, naive_hill_climbing2,
                    naive_first_choice, naive_first_choice2,
                    simulated_annealing]
    NAMES = ["HC-1", "HC-2",
            "FC-1", "FC-2",  
            "SA"]

    NUM_ALGS = len(NAIVE_ALGS)

    alg_avg_cost_traces = [[] for _ in range(NUM_ALGS)]
    max_num_iter = -1

    # get avg. cost trace over different weights & assignments
    # alg_avg_cost_traces[i] = avg. cost trace of alg i over the trials
    for trial in range(NUM_TRIALS):
        print "in trial ", trial
        weights = get_random_weights()
        assignment = get_random_assignment()

        # alg_avg_cost_trace[alg_index] = [c1 ... cn] avg cost values on iter i
        
        # find avg_cost_trace
        for alg_index in range(NUM_ALGS):
            alg = NAIVE_ALGS[alg_index]
        
            #print "#restarts ", str(i), " testing alg ", NAMES[alg_index]   
            (_, cost_trace, num_iter, _) = \
                alg(weights, assignment = assignment)
            max_num_iter = max(num_iter, max_num_iter)

            avg_cost_trace = map(lambda c: c*1.0/NUM_TRIALS, cost_trace)

            if len(alg_avg_cost_traces[alg_index]) == 0:
                alg_avg_cost_traces[alg_index] = avg_cost_trace
            else:
                for i in range(len(avg_cost_trace)):
                    if i < len(alg_avg_cost_traces[alg_index]):
                        alg_avg_cost_traces[alg_index][i] += avg_cost_trace[i]
                    else:
                        alg_avg_cost_traces[alg_index].append(avg_cost_trace[i])

    pprint(alg_avg_cost_traces)
    # turn alg_avg_cost_traces into a csv 
    csv_list = []
    for i in xrange(max_num_iter):
        row_dict = {}
        for alg_index in range(NUM_ALGS):
            avg_cost_trace = alg_avg_cost_traces[alg_index]
            alg_name = NAMES[alg_index]
            if i < len(avg_cost_trace):
                row_dict[alg_name] = avg_cost_trace[i]
        csv_list.append(row_dict)
    list_to_csv(csv_list, file_name, headers=None)

#compare_cost_traces(file_index=11,NUM_TRIALS=50)
# result = limited_random_restart(sideways_first_choice, weights, MAX_NUM_SIDEWAYS, MAX_NUM_RESTARTS)
# print result

# result = limited_random_restart(simulated_annealing, weights, MAX_NUM_SIDEWAYS, MAX_NUM_RESTARTS)
# print result

def compare_repeated_cost_traces(file_index, NUM_TRIALS=2, MAX_NUM_RESTARTS=5):
    print "in repeated compare cost traces"

    # compare avg. costs of sol
    file_name = "repeated_compare_cost_traces" + str(file_index) + ".csv"
    results = []


    NAIVE_ALGS = [naive_hill_climbing, naive_hill_climbing2,
                    naive_first_choice, naive_first_choice2,
                    simulated_annealing]
    NAMES = ["HC-1", "HC-2",
            "FC-1", "FC-2",  
            "SA"]

    NUM_ALGS = len(NAIVE_ALGS)

    alg_avg_cost_traces = [[] for _ in range(NUM_ALGS)]
    max_num_iter = -1

    # get avg. cost trace over different weights & assignments
    # alg_avg_cost_traces[i] = avg. cost trace of alg i over the trials
    for trial in range(NUM_TRIALS):
        print "in trial ", trial
        weights = get_random_weights()
        assignment = get_random_assignment()

        # alg_avg_cost_trace[alg_index] = [c1 ... cn] avg cost values on iter i
        
        # find avg_cost_trace
        for alg_index in range(NUM_ALGS):
            alg = NAIVE_ALGS[alg_index]
        
            #print "#restarts ", str(i), " testing alg ", NAMES[alg_index]   
            (_, cost_trace, num_iter, _) = \
                limited_random_restart(alg, weights, assignment = assignment, MAX_NUM_RESTARTS = MAX_NUM_RESTARTS)
            max_num_iter = max(num_iter, max_num_iter)

            avg_cost_trace = map(lambda c: c*1.0/NUM_TRIALS, cost_trace)

            if len(alg_avg_cost_traces[alg_index]) == 0:
                alg_avg_cost_traces[alg_index] = avg_cost_trace
            else:
                for i in range(len(avg_cost_trace)):
                    if i < len(alg_avg_cost_traces[alg_index]):
                        alg_avg_cost_traces[alg_index][i] += avg_cost_trace[i]
                    else:
                        alg_avg_cost_traces[alg_index].append(avg_cost_trace[i])

    pprint(alg_avg_cost_traces)
    # turn alg_avg_cost_traces into a csv 
    csv_list = []
    for i in xrange(max_num_iter):
        row_dict = {}
        for alg_index in range(NUM_ALGS):
            avg_cost_trace = alg_avg_cost_traces[alg_index]
            alg_name = NAMES[alg_index]
            if i < len(avg_cost_trace):
                row_dict[alg_name] = avg_cost_trace[i]
        csv_list.append(row_dict)
    list_to_csv(csv_list, file_name, headers=None)

#compare_repeated_cost_traces(file_index=20,NUM_TRIALS=20,MAX_NUM_RESTARTS=9)
