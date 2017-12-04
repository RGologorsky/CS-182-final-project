# constants
MAX_COST = 1000

# courses dictionary
courses = {'AM106': {'COURSE': 'AM106',
           'DAYS': set(['M', 'W']),
           'END': 1559,
           'SEMESTER': 'F',
           'START': 1430},
 'AM107': {'COURSE': 'AM107',
           'DAYS': set(['R', 'T']),
           'END': 1129,
           'SEMESTER': 'S',
           'START': 1000},
 'AM120': {'COURSE': 'AM120',
           'DAYS': set(['R', 'T']),
           'END': 1129,
           'SEMESTER': 'S',
           'START': 1000},
 'AM121': {'COURSE': 'AM121',
           'DAYS': set(['M', 'W']),
           'END': 1129,
           'SEMESTER': 'F',
           'START': 1000},
 'AM21A': {'COURSE': 'AM21A',
           'DAYS': set(['F', 'M', 'W']),
           'END': 1159,
           'SEMESTER': 'F',
           'START': 1100},
 'AM21B': {'COURSE': 'AM21B',
           'DAYS': set(['F', 'M', 'W']),
           'END': 1159,
           'SEMESTER': 'S',
           'START': 1100},
 'CS1': {'COURSE': 'CS1',
         'DAYS': set(['R', 'T']),
         'END': 1129,
         'SEMESTER': 'S',
         'START': 1000},
 'CS105': {'COURSE': 'CS105',
           'DAYS': set(['R', 'T']),
           'END': 1429,
           'SEMESTER': 'F',
           'START': 1300},
 'CS108': {'COURSE': 'CS108',
           'DAYS': set(['R', 'T']),
           'END': 1259,
           'SEMESTER': 'F',
           'START': 1130},
 'CS109A': {'COURSE': 'CS109A',
            'DAYS': set(['M', 'W']),
            'END': 1429,
            'SEMESTER': 'F',
            'START': 1300},
 'CS109B': {'COURSE': 'CS109B',
            'DAYS': set(['M', 'W']),
            'END': 1429,
            'SEMESTER': 'S',
            'START': 1300},
 'CS121': {'COURSE': 'CS121',
           'DAYS': set(['R', 'T']),
           'END': 1129,
           'SEMESTER': 'F',
           'START': 1000},
 'CS124': {'COURSE': 'CS124',
           'DAYS': set(['R', 'T']),
           'END': 1259,
           'SEMESTER': 'S',
           'START': 1130},
 'CS126': {'COURSE': 'CS126',
           'DAYS': set(['R', 'T']),
           'END': 1129,
           'SEMESTER': 'F',
           'START': 1000},
 'CS127': {'COURSE': 'CS127',
           'DAYS': set(['R', 'T']),
           'END': 1129,
           'SEMESTER': 'S',
           'START': 1000},
 'CS134': {'COURSE': 'CS134',
           'DAYS': set(['M', 'W']),
           'END': 1559,
           'SEMESTER': 'F',
           'START': 1430},
 'CS136': {'COURSE': 'CS136',
           'DAYS': set(['M', 'W']),
           'END': 1259,
           'SEMESTER': 'F',
           'START': 1130},
 'CS141': {'COURSE': 'CS141',
           'DAYS': set(['M', 'W']),
           'END': 1129,
           'SEMESTER': 'F',
           'START': 1000},
 'CS143': {'COURSE': 'CS143',
           'DAYS': set(['M', 'W']),
           'END': 1559,
           'SEMESTER': 'F',
           'START': 1430},
 'CS144R': {'COURSE': 'CS144R',
            'DAYS': set(['M', 'W']),
            'END': 1559,
            'SEMESTER': 'S',
            'START': 1430},
 'CS148': {'COURSE': 'CS148',
           'DAYS': set(['R', 'T']),
           'END': 1259,
           'SEMESTER': 'S',
           'START': 1130},
 'CS152': {'COURSE': 'CS152',
           'DAYS': set(['R', 'T']),
           'END': 1129,
           'SEMESTER': 'S',
           'START': 1000},
 'CS165': {'COURSE': 'CS165',
           'DAYS': set(['M', 'W']),
           'END': 1729,
           'SEMESTER': 'F',
           'START': 1600},
 'CS171': {'COURSE': 'CS171',
           'DAYS': set(['R', 'T']),
           'END': 1559,
           'SEMESTER': 'F',
           'START': 1430},
 'CS175': {'COURSE': 'CS175',
           'DAYS': set(['M', 'W']),
           'END': 1429,
           'SEMESTER': 'F',
           'START': 1300},
 'CS179': {'COURSE': 'CS179',
           'DAYS': set(['R', 'T']),
           'END': 1559,
           'SEMESTER': 'S',
           'START': 1430},
 'CS181': {'COURSE': 'CS181',
           'DAYS': set(['M', 'W']),
           'END': 1029,
           'SEMESTER': 'S',
           'START': 900},
 'CS182': {'COURSE': 'CS182',
           'DAYS': set(['R', 'T']),
           'END': 1429,
           'SEMESTER': 'F',
           'START': 1300},
 'CS189': {'COURSE': 'CS189',
           'DAYS': set(['F']),
           'END': 1559,
           'SEMESTER': 'S',
           'START': 1300},
 'CS191': {'COURSE': 'CS191',
           'DAYS': set(['M', 'W']),
           'END': 1029,
           'SEMESTER': 'S',
           'START': 900},
 'CS20': {'COURSE': 'CS20',
          'DAYS': set(['F', 'M', 'W']),
          'END': 1059,
          'SEMESTER': 'S',
          'START': 1000},
 'CS50': {'COURSE': 'CS50',
          'DAYS': set(['F']),
          'END': 1159,
          'SEMESTER': 'F',
          'START': 1000},
 'CS51': {'COURSE': 'CS51',
          'DAYS': set(['T']),
          'END': 1429,
          'SEMESTER': 'S',
          'START': 1300},
 'CS61': {'COURSE': 'CS61',
          'DAYS': set(['R', 'T']),
          'END': 1559,
          'SEMESTER': 'F',
          'START': 1430},
 'CS91R': {'COURSE': 'CS91R',
           'DAYS': set([]),
           'END': -1,
           'SEMESTER': 'F',
           'START': -1},
 'CS96': {'COURSE': 'CS96',
          'DAYS': set(['F', 'M', 'W']),
          'END': 1759,
          'SEMESTER': 'F',
          'START': 1600},
 'ES50': {'COURSE': 'ES50',
          'DAYS': set(['M', 'W']),
          'END': 1559,
          'SEMESTER': 'F',
          'START': 1430},
 'ES52': {'COURSE': 'ES52',
          'DAYS': set(['M', 'W']),
          'END': 1429,
          'SEMESTER': 'F',
          'START': 1300},
 'MATH154': {'COURSE': 'MATH154',
             'DAYS': set(['F', 'M', 'W']),
             'END': 1259,
             'SEMESTER': 'S',
             'START': 1200},
 'MATH21A': {'COURSE': 'MATH21A',
             'DAYS': set([]),
             'END': -1,
             'SEMESTER': 'FS',
             'START': -1},
 'MATH21B': {'COURSE': 'MATH21B',
             'DAYS': set([]),
             'END': -1,
             'SEMESTER': 'FS',
             'START': -1},
 'MATH23A': {'COURSE': 'MATH23A',
             'DAYS': set(['F']),
             'END': 1359,
             'SEMESTER': 'F',
             'START': 1300},
 'MATH23B': {'COURSE': 'MATH23B',
             'DAYS': set(['R', 'T']),
             'END': 1559,
             'SEMESTER': 'S',
             'START': 1430},
 'MATH25A': {'COURSE': 'MATH25A',
             'DAYS': set(['F', 'M', 'W']),
             'END': 1059,
             'SEMESTER': 'F',
             'START': 1000},
 'MATH25B': {'COURSE': 'MATH25B',
             'DAYS': set(['F', 'M', 'W']),
             'END': 1059,
             'SEMESTER': 'S',
             'START': 1000},
 'MATH55A': {'COURSE': 'MATH55A',
             'DAYS': set(['F', 'M', 'W']),
             'END': 1159,
             'SEMESTER': 'F',
             'START': 1100},
 'MATH55B': {'COURSE': 'MATH55B',
             'DAYS': set(['F', 'M', 'W']),
             'END': 1159,
             'SEMESTER': 'S',
             'START': 1100},
 'STAT110': {'COURSE': 'STAT110',
             'DAYS': set(['R', 'T']),
             'END': 1559,
             'SEMESTER': 'F',
             'START': 1430},
 'STAT121A': {'COURSE': 'STAT121A',
              'DAYS': set(['M', 'W']),
              'END': 1429,
              'SEMESTER': 'F',
              'START': 1300},
 'STAT121B': {'COURSE': 'STAT121B',
              'DAYS': set(['M', 'W']),
              'END': 1429,
              'SEMESTER': 'S',
              'START': 1300}}


# To ensure positive total costs: pre-req cost reduction < cost of taking class
# i.e. class gets easier with pre-reqs but always is a positive amount of work.


# individual cost of taking a course = "workload"
indiv_costs = {
    "cs50": 10,
    "cs51": 10,
    "cs121": 5,
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

