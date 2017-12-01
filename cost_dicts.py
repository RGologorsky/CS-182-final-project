# constants

# domain
domain = ["cs50", "cs51", "cs121", "cs124", "am107"]
domain_fall = ["cs50", "cs121"]
domain_spring = ["cs51", "cs124", "am107"]


# variables. 1 = Fall 1, 2 = Spring 1, 3 = Fall 2, 4 = Spring 2
X = {"year1_fall", "year1_spring", "year2_fall", "year2_spring"}


MAX_COST = 1000

# To ensure positive total costs: pre-req cost reduction < cost of taking class
# i.e. class gets easier with pre-reqs but always is a positive amount of work.


# individual cost of taking a course = "workload"
indiv_costs = {
    "cs50": 10,
    "cs51": 10,
    "cs121": 0,
    "cs124": 50,
    "am107": 5,
}


# pair cost is the cost of taking class2 given we took class1 in the past.
# so pair_costs["cs50]["cs51"] = cost of taking cs51 given we already took cs50
# pair_cost < 0 for prereqs: taking the pre-req makes the class easier.
# taking a class twice is forbidden, so pair_costs[class1][clas1] = MAX_COST. 

# NOTE - DO NOT FACTOR IN CO-REQUISITES, ANT-REQUISITES: ONLY PRE-REQUISITES
pair_costs = {
    "cs50": {
             "cs50": MAX_COST, 
             "cs51": -2, 
             "cs121": -1, 
             "cs124": -10
            },
    "cs51": {
             "cs50": -1, 
             "cs51": MAX_COST, 
             "cs121": -1, 
             "cs124": -5
            },
    "cs121": {
               "cs50": -2, 
               "cs51": -1, 
               "cs121": MAX_COST, 
               "cs124": -10
             },
    "cs124": {
               "cs50": -10, 
               "cs51": -10,
               "cs121": -5, 
               "cs124": MAX_COST
             },
    "am107": {
               "am107": MAX_COST, 
               "cs124": -10
             },
}
