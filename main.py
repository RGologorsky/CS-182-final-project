from printing import *
from helpers import *
#from branch_and_bound import *
from local_search_restricted_successors import sideways_hill_climbing, naive_hill_climbing
from local_search_many_successors       import sideways_hill_climbing2,naive_hill_climbing2
from first_choice_hill_climbing         import sideways_first_choice,  naive_first_choice, sideways_first_choice2,  naive_first_choice2 
from simulated_annealing                import simulated_annealing
from random_restart                     import random_restart, limited_random_restart 

from csv_parser import list_to_csv

ALGS = [sideways_hill_climbing, naive_hill_climbing,
        sideways_hill_climbing2,naive_hill_climbing2,
        sideways_first_choice, naive_first_choice,
        sideways_first_choice2, naive_first_choice2,
        simulated_annealing]

NAMES= ["Sideways Greedy HC-1", "Greedy HC-1",
        "Sideways Greedy HC-2", "Greedy HC-2",
        "Sideways First Choice HC-1", "First Choice HC-1",
        "Sideways First Choice HC-2", "First Choice HC-2",
        "Simulated Annealing"]

META = [limited_random_restart]

MAX_NUM_SIDEWAYS = 0 
MAX_NUM_ITER = 1

MAX_WEIGHT = 100
MIN_WEIGHT = 0.01

def get_valid_weights():
    weights = None
    while type(weights) is not list or len(weights) != 4:
        try:
            weights = list(input("Please enter your weights, seperated by commas: "))
        except:
            pass

    weights.append(MAX_WEIGHT * max(weights))
    weights.append(MIN_WEIGHT * min(filter(lambda x: x != 0, weights)))

    return weights

def chooose_alg():
    print "Algorithm Options: "
    print str(NAMES)
    alg_index = None
    while not alg_index or alg_index < 0 or alg_index >= len(ALGS):
        try:
            alg_index = int(raw_input("Please enter the index of the alg. you'd like to try (recommend FC HC-2, index 7): "))
        except:
            pass
    return ALGS[alg_index]

def chooose_num_restarts():
    s = "Please enter #random restarts (0 = no restarts = 1 alg iter): "
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
    print "Please rate how much you care about the following features in your course assignment (floats and negatives allowed):"
    print "(A) Pre-reqs (enter a high number if you want to follow all of them)"
    print "(B) Workload (enter a high number if you want to minimize #hours)"
    print "(C) Q-Score  (enter a high number if you want to maximize q-score)"
    print "(D) Smaller Class Sizes (enter a high number if you prefer <50 class size)"
    
    print "\n"
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
            next_step = raw_input("Choose c = Continue (choose another alg, same weights), r = Restart (new alg and weights), q = Quit: ")

        if next_step == "q":
            quit = True
        
        if next_step == "r":
            weights = get_valid_weights()
        
        
        
def main():
    interact()

main()
