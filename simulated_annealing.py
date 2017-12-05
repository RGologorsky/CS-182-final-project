import numpy as np

def simulated_annealing(weights):

  curr_state = get_random_assignment()

  initial_cost = get_cost(assignment, weights)
  curr_cost = initial_cost

  trace = [assignment]
  cost_trace = [initial_cost]

  T = 1.0
  alpha = 0.99

  for t in xrange(10000):
      neighbor, neighbor_cost = get_neighbor(curr_state, curr_cost)
      delta_E = (neighbor_cost - curr_cost)/curr_cost # normalization
      switch_probability = np.exp(delta_E/T) # used only when delta_E < 0

      # switch to neighbor if its advantageous or random move
      if delta_E > 0 or coin_flip(switch_probability):
          curr_state, curr_wt, curr_val = neighbor, neighbor_wt, neighbor_val

      trace.append(curr_val)
      wt_trace.append(curr_wt)
      T = alpha * T

  # print stats
  print("SA Algorithm: Value:{}, Weight:{}\nBag:{}".format(curr_val, curr_wt, curr_state))
  # return a trace of values resulting from your simulated annealing
  return trace

if __name__ == "__main__":
  # Greedy result is maximize v/w
  vw_ratio = sorted(map(lambda x: (x, 1.*v[x]/w[x]), range(N)), key= lambda x: -x[1])
  greedy_val = 0
  greedy_weight = 0
  greedy_bag = []
  index = 0
  while greedy_weight + w[vw_ratio[index][0]] < W:
      greedy_val += v[vw_ratio[index][0]]
      greedy_weight += w[vw_ratio[index][0]]
      greedy_bag += [vw_ratio[index][0]]
      index += 1

  print("Greedy Algorithm:\nValue:{}, Weight:{}\nBag:{}".format(greedy_val, greedy_weight, greedy_bag))
  SA_trace = simulated_annealing()
  plt.plot([greedy_val]*len(SA_trace), label="Greedy")
  plt.plot(SA_trace, label="SA")
  plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
         ncol=2, mode="expand", borderaxespad=0.)
  plt.show()
