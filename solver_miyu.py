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

#グラハムスキャン(https://qiita.com/s-yoshiki/items/3c6fcaa2ffa4bb79936e)
def convex(data):
    datalen = len(data)
    #y座標最小のものを探す
    min = 0
    for i in range(datalen):
      if (data[min, 1] > data[i, 1]):
        min = i
      elif (data[min, 1] == data[i, 1] and  data[min, 0] < data[i, 0]):
        min = i

    #反時計周りでの角度を調べる
    angle = np.zeros((datalen,2))
    for i in range(datalen):
      if (i == min):
        angle[i] = [0, i]
      else:
        theta = math.atan2((data[i, 1] - data[min, 1]), data[i, 0] - data[min, 0])
        if (theta < 0):
          theta = (2 * math.pi) + theta
        angle[i] = [theta, i]

    #角度順にソート
    sorted = angle[angle[:,0].argsort(), :]

    stack = []
    stack.extend([sorted[0, 1], sorted[1, 1], sorted[2, 1]])

    for i in range(3, datalen):
      stacktop = len(stack)
      while(True):
        theta1 = math.atan2(data[int(stack[stacktop - 1]), 1] - data[int(stack[stacktop - 2]), 1],
                            data[int(stack[stacktop - 1]), 0] - data[int(stack[stacktop - 2]), 0])
        if (theta1 < 0): 
          theta1 = 2 * math.pi + theta1
        theta2 = math.atan2(data[int(sorted[i, 1]), 1] - data[int(stack[stacktop - 1]), 1],
                            data[int(sorted[i, 1]), 0] - data[int(stack[stacktop - 1]), 0])
        if (theta2 <= 0): 
          theta2 = 2 * math.pi + theta2
        if (theta2 - theta1 < 0):
          del stack[stacktop - 1]
          stacktop -= 1
        else:
          break
      stack.append(sorted[i, 1])

    for i in range (len(stack)):
      stack[i] = int(stack[i])
    return stack

#追加コストを計算
def cal_cost(data,i,j,k):
    return np.linalg.norm([data[i] - data[k]]) + np.linalg.norm([data[k] - data[j]])\
           - np.linalg.norm([data[i] - data[j]])

#コスト比を計算
def cal_costratio(data,i,j,k):
    return (np.linalg.norm([data[i] - data[k]]) + np.linalg.norm([data[k] - data[j]])) / np.linalg.norm([data[i] - data[j]])

#最近挿入法
def insertion(data, root, ex_root):
    for i , number in enumerate(root):
        ex_root.remove(number)

    while (True):
        min = 0
        costratio = [0 for i in range(len(root))]
        minNum = [0 for i in range(len(root))]
        for i in range (len(root)):
            for j in range(0, len(ex_root)):
                if j == 0 or min > cal_cost(data,root[i - 1], root[i], ex_root[j]):
                    min = (cal_cost(data, root[i - 1], root[i], ex_root[j]))
                    minNum[i] = ex_root[j]
            costratio[i] = cal_costratio(data, root[i - 1],root[i], minNum[i])

        ratiomin = 9999
        ratiominNum = 0

        for i in range (len(root)):
            if ratiomin > costratio[i]:
                ratiomin = costratio[i]
                ratiominNum = i

        root.insert(ratiominNum, minNum[ratiominNum])
        ex_root.remove(minNum[ratiominNum])

        if not ex_root:
            break

    return root


if __name__ == '__main__':
    assert len(sys.argv) > 1
    data, datalen, root, ex_root = init_data(read_input(sys.argv[1]))
    root = convex(data)
    root = insertion(data, root, ex_root)
    print_solution(root)