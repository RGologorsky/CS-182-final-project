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

NAMES= ["Sideways HC-1", "HC-1",
        "Sideways HC-2", "HC-2",
        "Sideways FC HC-2", "Sideways FC", "FC HC-2",
        simulated_annealing]
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
        res = limited_random_restart(naive_first_choice, weights, \
                                            MAX_NUM_SIDEWAYS, MAX_NUM_RESTARTS)
        print_user(res)
        print("\n")
        c =get_costs(res[0], weights, printing=True)
        print "Costs: ", c
        next_step = raw_input("Hope you liked it! Choose c = Continue, r = Restart, q = Quit: ")

        if next_step == "q":
            quit = True
        
        elif next_step == "r":
            weights = get_valid_weights()
        
        elif next_step == "c":
            pass
        
        else:
            next_step = raw_input("Options: Continue, r = Restart, q = Quit: ")

def main():
    interact()

main()
