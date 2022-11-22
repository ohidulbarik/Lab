# -*- coding: utf-8 -*-
# Author:   MD OHIDUL BARIK
# Student ID: SL1816013

import numpy as np
import pandas as pd
import time
import json
import math
from util import *
from args import parse_args

def main():
    # Get arguments
    start = time.time()
    args = parse_args()
    filename = ''
    # Use the corresponding data file
    if args.file:
        filename = args.file
    elif args.data == 'nctu':
        filename = "data/nctu.csv"
    elif args.data == 'tsp':
        filename = 'TSP_data/TSP100cities.tsp'
    else:
        print("ERROR: undefined data file")
    tsp10 = pd.read_csv(filename,sep=' ',header=None)
    coordinates = tsp10.iloc[:,1:].values
    NUM_NEW_SOLUTION_METHODS = 3
    SWAP, REVERSE, TRANSPOSE = 0, 1, 2


    num_location = coordinates.shape[0]
    markov_step = args.markov_coefficient * num_location
    T_0, T, T_MIN = args.init_temperature, args.init_temperature, 1
    T_NUM_CYCLE = 1
    # Build distance matrix to accelerate cost computing
    distmat = get_distmat(coordinates)

    sol_new, sol_current, sol_best = (np.arange(num_location), ) * 3
    cost_new, cost_current, cost_best = (float('inf'), ) * 3

    # Record costs during the process
    costs = []

    # previous cost_best
    prev_cost_best = cost_best

    # counter for detecting how stable the cost_best currently is
    cost_best_counter = 0

    while T > T_MIN and cost_best_counter < args.halt:
        for i in range(markov_step):
            # Use three different methods to generate new solution
            # Swap, Reverse, and Transpose
            choice = np.random.randint(NUM_NEW_SOLUTION_METHODS)
            if choice == SWAP:
                sol_new = swap(sol_new)
            elif choice == REVERSE:
                sol_new = reverse(sol_new)
            elif choice == TRANSPOSE:
                sol_new = transpose(sol_new)
            else:
                print("ERROR: new solution method %d is not defined" % choice)

            # Get the total distance of new route
            cost_new = sum_distmat(sol_new, distmat)

            if accept(cost_new, cost_current, T):
                # Update sol_current
                sol_current = sol_new.copy()
                cost_current = cost_new

                if cost_new < cost_best:
                    sol_best = sol_new.copy()
                    cost_best = cost_new
            else:
                sol_new = sol_current.copy()

        # Lower the temperature
        alpha = 1 + math.log(1 + T_NUM_CYCLE)
        T = T_0 / alpha
        costs.append(cost_best)

        # Increment T_NUM_CYCLE
        T_NUM_CYCLE += 1

        # Detect stability of cost_best
        if isclose(cost_best, prev_cost_best, abs_tol=1e-12):
          cost_best_counter += 1
        else:
          # Not stable yet, reset
          cost_best_counter = 0

        # Update prev_cost_best
        prev_cost_best = cost_best

        # Monitor the temperature & cost
        print("Temperature:", "%.2f°C" % round(T, 2),
              " Distance:", "%.2fm" % round(cost_best, 2),
              " Optimization Threshold:", "%d" % cost_best_counter)

    # Show final cost & route
    print("shortest distance：", round(costs[-1], 2))
    print("total time：",time.time()-start)
    print("optimized path:", sol_best)

    # Plot cost function and TSP-route
    plot(sol_best.tolist(), coordinates, costs)

if __name__ == "__main__":
    main()
