# -*- coding: utf-8 -*-
# Author:   MD OHIDUL BARIK
# Student ID: SL1816013

import pandas as pd
import time
import random
from queue import Queue
import numpy as np

data_path = 'TSP_data/TSP100cities.tsp'

def load_data(data_path):
    data = pd.read_csv(data_path, sep=' ', header=None)
    a = data.iloc[:, 1:].values.reshape(-1, 2, 1)
    b = a.T
    distance = np.sqrt(np.sum(np.square(a - b), axis=-2))
    city = data.iloc[:, 0].values
    n_city = a.shape[0]
    return distance,n_city

distance,n_city = load_data(data_path)

INF = 10000000


class Node:
    def __init__(self):
        self.visited = [False] * n_city
        self.s = 1
        self.e = 1
        self.k = 1
        self.sumv = 0
        self.lb = 0
        self.listc = []


pq = Queue()  
low = 0 
up = 0  
dfs_visited = np.zeros(n_city).astype(bool)
dfs_visited[0] = True


def dfs(u, k, l):
    if k == n_city - 1:
        return (l + distance[u][0])
    minlen = INF
    p = 0
    for i in range(n_city):
        if dfs_visited[i] == False and minlen > distance[u][i]:
            minlen = distance[u][i]
            p = i
    dfs_visited[p] = True
    return dfs(p, k + 1, l + minlen)


def get_up():
    global up
    up = dfs(0, 0, 0)


def get_low():
    global low
    for i in range(n_city):
        temp = distance[i].copy()
        temp.sort()
        low = low + temp[0] + temp[1]
    low = low / 2


def get_lb(p):
    ret = p.sumv * 2
    min1 = INF 
    min2 = INF
    
    for i in range(n_city):
        if p.visited[i] == False and min1 > distance[i][p.s]:
            min1 = distance[i][p.s]
    ret = ret + min1

    
    for j in range(n_city):
        if p.visited[j] == False and min2 > distance[p.e][j]:
            min2 = distance[p.e][j]
    
    for i in range(n_city):
        if p.visited[i] == False:
            min1 = min2 = INF
            for j in range(n_city):
                min1 = distance[i][j] if min1 > distance[i][j] else min1
            for m in range(n_city):
                min2 = distance[i][m] if min2 > distance[m][i] else min2
            ret = ret + min1 + min2
    return (ret + 1) / 2


def solve():
    global up
    get_up()
    get_low()  
    node = Node()
    node.s = 0  
    node.e = 0  
    node.k = 1  
    node.visited = [False] * n_city  
    node.listc.append(0)
    node.visited[0] = True
    node.sumv = 0  
    node.lb = low 
    ret = INF 
    pq.put(node) 
    while pq.qsize() != 0:
        tmp = pq.get()
        if tmp.k == n_city - 1:
            p = 0 
            for i in range(n_city):
                if tmp.visited[i] == False:
                    p = i
                    break
            ans = tmp.sumv + distance[tmp.s][p] + distance[p][tmp.e] 
            if ans <= tmp.lb:
                ret = min(ans, ret)
                break
            else:
                up = min(ans, up) 
                ret = min(ret, ans)
                continue
   
        for i in range(n_city):
            if tmp.visited[i] == False:
                next_node = Node()
                next_node.s = tmp.s  
                next_node.sumv = tmp.sumv + distance[tmp.e][i]
                next_node.e = i 
                next_node.k = tmp.k + 1
                next_node.listc = tmp.listc.copy()
                next_node.listc.append(i)
                next_node.visited = tmp.visited.copy()
                next_node.visited[i] = True
                next_node.lb = get_lb(next_node) 
                if next_node.lb >= up:
                    continue
                pq.put(next_node)
    tmp.listc.append(4)
    return ret, tmp


if __name__ == "__main__":
    for i in range(n_city):
        distance[i][i] = INF
    start = time.time()
    sumpath, node = solve()
    end = time.clock()
    print("shortest path distance：",sumpath)
    list1 = node.listc.copy()
    print("optimized path：",list1)
    print("total time cost：",time.time()-start)
