# -*- coding: utf-8 -*-
# Author:   MD OHIDUL BARIK
# Student ID: SL1816013


import math
import random
import datetime
import copy
import matplotlib.pyplot as plt
import turtle
import datetime
import time

def data_loader(data_type):
    d_10 = "TSP_data/TSP10cities.tsp"
    d_100 = "TSP_data/TSP100cities.tsp"
    if data_type == 10:
        open_dir = d_10
    elif data_type == 100:
        open_dir = d_100
    else:
        open_dir = ''
        print("Open wrong file type!")
    data_ = []
    with open(open_dir, 'r') as f:
        for line in (f.readlines()):
            line = line.split()
            data_.append([int(line[1]), int(line[2])])
    return data_


class SaTSP(object):
    def __init__(self, tp=10, tf=0.01, alpha=0.9):
        self.tf = tf
        self.alpha = alpha
        self.iter_num = []
        self.distance_path = []
        self.ultimate_path = []
        self.coordinates = data_loader(tp)
        self.iteration = 200 * len(self.coordinates)

    def initial_temperature(self):
        dist_list = []
        for i in range(100):
            path = random.sample(self.coordinates[1:], len(self.coordinates)-1)
            head = self.coordinates[0:1]
            head.extend(path)
            dist_list.append(self.all_dist(head))
        t0 = -(max(dist_list) - min(dist_list)) / math.log(0.9)
        print('initial temp:', t0)
        return t0

    def D_value(self, current_path, update_path):
        current_distance = self.all_dist(current_path)
        update_distance = self.all_dist(update_path)
        d_value = update_distance - current_distance
        return d_value

    def first_path(self):
        length = len(self.coordinates)-1
        head = self.coordinates[0:1]
        path = random.sample(self.coordinates[1:], length)
        head.extend(path)
        return head

    def swap(self, path):
        city_1 = random.randint(1, len(self.coordinates) - 1)
        while True:
            city_2 = random.randint(1, len(self.coordinates) - 1)
            if city_2 != city_1:
                break
            else:
                continue
        path[city_1], path[city_2] = path[city_2], path[city_1]
        return path

    def two_point_dist(self, point1, point2):
        dist_x = point1[0] - point2[0]
        dist_y = point1[1] - point2[1]
        dist = dist_x ** 2 + dist_y ** 2
        dist = math.sqrt(dist)
        return dist

    def all_dist(self, path):
        sum_cities = 0
        n = len(path)
        for i in range(n - 1):
            sum_cities += self.two_point_dist(path[i], path[i + 1])
        sum_cities += self.two_point_dist(path[n - 1], path[0])
        return sum_cities

    def plot_graphic(self):  
        plt.plot(self.iter_num, self.distance_path)
        plt.show()

    def main(self):
        start_time = datetime.datetime.now()
        t = self.initial_temperature()
        current_path = self.first_path()
        i = 0
        while t > self.tf:
            iteration_number = 0
            while iteration_number < self.iteration:
                temple_path = copy.deepcopy(current_path)
                update_path = self.swap(temple_path)
                de2 = self.D_value(current_path, update_path)
                if de2 < 0:
                    current_path = update_path
                else:
                    p = math.exp(-de2 / t)
                    if random.random() <= p:
                        current_path = update_path
                    else:
                        current_path = current_path
                iteration_number += 1
            t = self.alpha * t
            i = i + 1
            self.iter_num.append(i)
            self.ultimate_path = current_path
            distance = self.all_dist(current_path)
            self.distance_path.append(distance)
        end_time = datetime.datetime.now()
        this_time = end_time - start_time
        print('total time：', this_time, 'number of iteration：', max(self.iter_num))
        print('Order:', [self.coordinates.index(d) for d in self.ultimate_path], 'Coat:', round(self.distance_path[-1], 6))

    def plot_map(self):
        # set base attribute
        turtle.screensize(600, 800)
        turtle.speed(0)
        turtle.hideturtle()
        r_city = 8
        x_resize = 0.2
        y_resize = 0.18
        off_set = 300
        turtle.pensize(4)
        # start node
        turtle.penup()
        [x, y] = self.ultimate_path[0]
        (x, y) = (x * x_resize - off_set, y * y_resize - off_set)
        turtle.goto(x, y)
        turtle.pendown()
        turtle.pencolor('red')
        turtle.circle(r_city)
        for i in range(1, len(self.ultimate_path)):
            [x, y] = self.ultimate_path[i]
            (x, y) = (x * x_resize - off_set, y * y_resize - off_set)
            turtle.pencolor('blue')
            turtle.goto(x, y)
            turtle.pencolor('green')
            turtle.circle(r_city)
        turtle.done()


s1 = SaTSP(tp=100)
s1.main()
s1.plot_map()
s1.plot_graphic()
