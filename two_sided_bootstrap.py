#!/usr/bin/python
__author__ = "Dasha Bogdanova"
__email__ = "dasha.bogdanova@gmail.com"
""" This script implements the two-sided bootstrap resampling statistical significance test 
(see Fig.1 in Randomized significance tests in machine translation. Yvette Graham, Nitika Mathur, and Timothy Baldwin. ACL 2014.)
"""

from random import randint
import matplotlib.pyplot as plt
from sys import argv
import seaborn as sns

def p_at_1(S_x):
  return float(S_x.count(1))/len(S_x)

def bootstrap_resample(S_x, S_y, samples=10000, alpha=0.05):
  assert len(S_x) == len(S_y), 'S_x and S_y should be of the same length'
  c = 0
  # actual statistic of P_at_1 differences
  score = p_at_1(S_x) - p_at_1(S_y)
  print score
  # pseudo-statistic values
  pseudo_statistics = []

  # generating the bootstrap samples for S_x and S_y
  for s in xrange(samples):
    random_indices = [randint(0,len(S_x)-1) for i in xrange(len(S_x))]
    assert len(random_indices) == len(S_x), 'resampled should be the same size as the original'
    # random samples of both systems
    S_x_b = [S_x[i] for i in random_indices]
    S_y_b = [S_y[i] for i in random_indices]
    diff = p_at_1(S_x_b) - p_at_1(S_y_b)
    pseudo_statistics.append(diff)

  # mean p_at_1 difference of bootstrapped samples
  mean_t = sum(pseudo_statistics)/float(len(pseudo_statistics))
  for ps in pseudo_statistics:
    if abs(ps - mean_t) >= abs(score):
      c += 1
  if float(c)/samples <= alpha:
    return True, pseudo_statistics, c
  return False, pseudo_statistics, c

# plots the differences
def plot(statistics):
  sns.distplot(statistics)
  sns.plt.show()

if __name__ == '__main__':
  fin = open(argv[1])
  S_x = map(int,fin.readlines())
  fin.close()
  fin = open(argv[2])
  S_y = map(int,fin.readlines())
  fin.close()
  sign, stats, c = bootstrap_resample(S_x, S_y)
  print 'Significant: ', sign
  print 'c =', c
  plot(stats)


  
  
  
  
  
  
  
