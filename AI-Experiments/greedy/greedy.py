# -*- coding: utf-8 -*-
# Author:   MD OHIDUL BARIK
# Student ID: SL1816013

import pandas as pd
import time
import random
import math
import numpy as np

data_path = 'TSP_data/TSP10cities.tsp'

def load_data(data_path):
    data = pd.read_csv(data_path, sep=' ', header=None)
    a = data.iloc[:, 1:].values.reshape(-1, 2, 1)
    b = a.T
    distance = np.sqrt(np.sum(np.square(a - b), axis=-2))
    city = data.iloc[:, 0].values
    n_city = a.shape[0]
    return distance,n_city




def find(city):
    min = 100000000
    nextcity = -1
    for i in range(n_city):
        if (i!=city)and(distance[city][i]<min)and(state[i]==0):
            min = distance[city][i]
            nextcity = i
    state[nextcity] = 1
    return nextcity


def TSP(start):
    sum = 0
    path = np.zeros(n_city).astype(int)
    path[0] = start
    state[start] = 1
    for i in range(1,n_city):
        path[i] = find(path[i-1])
        sum += distance[path[i-1]][path[i]]
    return sum,path


if __name__ == "__main__":
    start_time = time.time()
    distance, n_city = load_data(data_path)


    state = np.zeros(n_city).astype(int)
    start = random.randint(0,n_city)

    sum, path = TSP(start)
    sum += distance[path[0]][path[-1]]
    cost_time = time.time() - start_time
    print("Shortest Path Distance：",sum)
    print("total cost time：",cost_time)
    print("optimized path:",path)





