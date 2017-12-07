from printing import *
from helpers import *
#from branch_and_bound import *
from local_search_restricted_successors import sideways_hill_climbing, naive_hill_climbing
from local_search_many_successors       import sideways_hill_climbing2,naive_hill_climbing2
from first_choice_hill_climbing         import sideways_first_choice,  naive_first_choice
from simulated_annealing                import simulated_annealing
from random_restart                     import random_restart, limited_random_restart 

from csv_parser import list_to_csv

ALGS = [sideways_hill_climbing, naive_hill_climbing,
        sideways_hill_climbing2,naive_hill_climbing2,
        sideways_first_choice, naive_first_choice,
        simulated_annealing]

NAMES= ["Sideways Greedy HC-1", "Greedy HC-1",
        "Sideways Greedy HC-2", "Greedy HC-2",
        "Sideways First Choice HC-2", "First Choice HC-2",
        "Simulated Annealing"]

META = [limited_random_restart]

MAX_NUM_SIDEWAYS = 0 
MAX_NUM_RESTARTS = 1

MAX_WEIGHT = 100
MIN_WEIGHT = 0.01

def get_valid_weights():
    weights = None
    while type(weights) is not list:
        try:
            weights = list(input("Please enter your weights, seperated by commas. "))
        except:
            pass

    weights.append(MAX_WEIGHT * max(weights))
    weights.append(MIN_WEIGHT * min(filter(lambda x: x != 0, weights)))

    return weights

def chooose_alg():
    print "Algorithm Options: "
    print str(NAMES)
    alg_index = None
    while not alg_index or alg_index < 0 or alg_index >= len(NAMES):
        try:
            alg_index = int(raw_input("Please enter the index of the alg. you'd like to try (recommend FC HC-2, index 5): "))
        except:
            pass
    return ALGS[alg_index]

def chooose_num_restarts():
    s = "Please enter the #alg iterations (random restart). (1 alg iter = no restarts): "
    num_restarts = None
    while not num_restarts or num_restarts < 1:
        try:
            num_restarts = int(raw_input(s))
        except:
            pass
    return num_restarts

def interact():
    quit = False

    # INTRO
    print "\nHello! Welcome to the CS Study Plan Generator!\n"
    print "Enter in your preferences, and we'll output an individualized study plan for you."
    print "Please rate how much you care about the following features in your course assignment:"
    print "Pre-reqs, Workload, Q-Score, Smaller Class Sizes. Floats allowed."
    
    weights = get_valid_weights()

    # maybe? normalize wts, so cost func. not too high. Easier to graph then.
    while not quit:
        alg = chooose_alg()
        num_restarts = chooose_num_restarts()

        res = limited_random_restart(alg, weights, \
                                            MAX_NUM_SIDEWAYS, num_restarts)
        print_user(res)
        get_costs(res[0],weights,  printing=True)
        print("Hope you liked it!\n")
        
        next_step = ""
        while next_step not in ["q", "r", "c"]:
            next_step = raw_input("Choose c = Continue (re-run alg w/same weights), r = Restart (new weights), q = Quit: ")

        if next_step == "q":
            quit = True
        
        if next_step == "r":
            weights = get_valid_weights()
        
        
        
def main():
    interact()

main()
