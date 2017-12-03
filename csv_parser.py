

def get_dictionary():

    with open('normalized_courses.csv', mode='r') as infile:
        reader = csv.reader(infile)
        sum_workload = 0
        sum_qscore = 0
        with open('normalized_courses.csv', mode='w') as outfile:
            writer = csv.writer(outfile)
            for rows in reader:


            mydict = {rows[0]:rows[1] for rows in reader}
