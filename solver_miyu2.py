#!/usr/bin/env python3

import sys
import math
import numpy as np

from common import print_solution, read_input

#データの整形
def init_data(data):
  root = []
  ex_root = []
  datalen = len(data)
  newdata = np.zeros((datalen, 2))
  for i in range (datalen):
    ex_root.append(i)
    newdata[i,0] = data[i][0]
    newdata[i,1] = data[i][1]
  return newdata, datalen, root, ex_root

#Nearest Neighbor法
def nearest_n(data, datalen, root, ex_root):

  root.append(0)
  ex_root.remove(0)

  for i in range(datalen - 1):
    min_len = 0
    min_Num = 0
    for j in range(len(ex_root)):
      if j == 0 or min_len > np.linalg.norm([data[root[i]] - data[ex_root[j]]]):
        min_len = np.linalg.norm([data[root[i]] - data[ex_root[j]]])
        min_Num = ex_root[j]
    root.append(min_Num)
    ex_root.remove(min_Num)

  return root

#2-opt法
def opt_2(data, datalen, root):
  total = 0
  while True:
    count = 0
    for i in range(datalen - 2):
      i1 = i + 1
      for j in range(i + 2, datalen):
        if j == datalen - 1:
          j1 = 0
        else:
          j1 = j + 1
        if i != 0 or j1 != 0:
          l1 = np.linalg.norm([data[root[i]] - data[root[i1]]])
          l2 = np.linalg.norm([data[root[j]] - data[root[j1]]])
          l3 = np.linalg.norm([data[root[i]] - data[root[j]]])
          l4 = np.linalg.norm([data[root[i1]] - data[root[j1]]])
          if l1 + l2 > l3 + l4:
            new_root = root[i1:j+1]
            root[i1:j+1] = new_root[::-1]
            count += 1
    total += count
    if count == 0: 
      break
  return root

if __name__ == '__main__':
    assert len(sys.argv) > 1
    data, datalen, root, ex_root = init_data(read_input(sys.argv[1]))
    root = nearest_n(data, datalen, root, ex_root)
    root = opt_2(data, datalen, root)
    print_solution(root)