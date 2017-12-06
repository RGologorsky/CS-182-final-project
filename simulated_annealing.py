import numpy as np
from helpers import *
from constants import *
from cost_functions import *
import random
import matplotlib.pyplot as plt

import time
# returns random neighbor. Neighbor is an assignment were one class is added/dropped
def get_random_neighbor(assignment):
    change_type = randint(0,1) # 0 = add course, 1 = delete course

    no_add = False
    no_del = False

    semester_index = randint(0, 7)
    add_semester_indices = range(8)
    del_semester_indices = range(8)

    if change_type == 0:
      add_semester_index = choice(add_semester_indices)
      while change_type == 0 and len(add_semester_indices) > 0 and len(assignment[add_semester_index]) == 4:
        add_semester_indices.remove(add_semester_index)

        if len(add_semester_indices) == 0:
            no_add = True # we can't add; we are full.
            change_type = 1
        else:
          add_semester_index = choice(add_semester_indices)

      if len(assignment[add_semester_index]) < 4:
          semester_index = add_semester_index


    if change_type == 1:
      del_semester_index = choice(del_semester_indices)
      while change_type == 1 and len(del_semester_indices) > 0 and len(assignment[del_semester_index]) == 0:
        del_semester_indices.remove(del_semester_index)

        if len(del_semester_indices) == 0:
          no_del = True # we can't del; we are empty.
          change_type = 0
        else:
          del_semester_index = choice(del_semester_indices)
      if len(assignment[del_semester_index]) > 0:
          semester_index = del_semester_index


    # can't add if alreadying taking 4 courses - try again
    if change_type == 0 and len(assignment[semester_index]) == 4:
      return assignment

    # can't delete if no courses in semester - try again
    if change_type == 1 and len(assignment[semester_index]) == 0:
        return assignment

    if no_add and no_del: # impossible - we can add if we are empty.
      return assignment

    # add a course to the semester
    if change_type == 0:
        possible_courses = new_course_domain(semester_index, assignment)
        if len(possible_courses) == 0:
          # semester_indices.remove(semester_index)
          # semester_index = choice(semester_indices)
          return get_random_neighbor(assignment)

        return add_to_assignment(assignment, semester_index, choice(possible_courses))

    # del a course to the semester
    return del_to_assignment(assignment, semester_index, randint(0, -1 + len(assignment[semester_index])))

def simulated_annealing(weights, assignment = None):
  start_time = time.time()

  curr_state = assignment if assignment else get_random_assignment()
  curr_cost = get_cost(curr_state, weights)

  cost_trace = [curr_cost]

  T = 1.0
  alpha = 0.999
  MAX_ITER = 5000

  for t in xrange(MAX_ITER):
      if int(curr_cost) == 0:
        time_elapsed = round(time.time() - start_time, 2)
        return (curr_state, cost_trace, t, time_elapsed)

      neighbor = get_random_neighbor(curr_state)
      neighbor_cost = get_cost(neighbor, weights)

      delta_E = (curr_cost - neighbor_cost)/curr_cost # normalization
      switch_probability = np.exp(delta_E/T) # used only when delta_E < 0

      # switch to neighbor if its advantageous or random move
      if delta_E > 0 or coin_flip(switch_probability):
          curr_state, curr_cost = neighbor, neighbor_cost

      cost_trace.append(curr_cost)
      T = alpha * T

  time_elapsed = round(time.time() - start_time, 2)
  return (curr_state, cost_trace, MAX_ITER, time_elapsed)
