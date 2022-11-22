# -*- coding: utf-8 -*-
# Author:   MD OHIDUL BARIK
# Student ID: SL1816013

import math
import random
import datetime
import copy
import matplotlib.pyplot as plt
import turtle
import time
import numpy as np

def distance(a, b):
	'''
	calculate distance between two point a, b
	:param a: coordinate of a shape like (x, y)
	:param b: coordinate of b shape like (x, y)
	:return: Euclid distance of a, b
	'''
	(x1, y1), (x2, y2) = a, b
	[x1, y1, x2, y2] = map(int, [x1, y1, x2, y2])
	return math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2))


def distance_in_index(lst, index1, index2):
	'''
	calculate distance between two point of index in list
	:param lst: point list, shape like [[x1, y1], [x2, y2], ...]
	:param index1: index of point a
	:param index2: index of point b
	:return: Euclid distance of index point
	'''
	a = (lst[index1][0], lst[index1][1])
	b = (lst[index2][0], lst[index2][1])
	return distance(a, b)


def data_loader(data_type):
	'''
	read data
	:param data_type: data type, 10 point or 100 point
	:return: data list shape like [[x1, y1], [x2, y2], ...]
	'''
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
			# x, y
			data_.append([line[1], line[2]])
	return data_



def distance_matrix(data):
	'''
	convert data list into distance matrix
	:param data: data list
	:return: distance matrix
	'''
	len_ = len(data)
	d_mtr = np.zeros((len_, len_), dtype=np.float)
	for i in range(len_):
		for j in range(len_):
			d_mtr[i][j] = distance_in_index(data, i, j)
	return d_mtr


class DynamicProgramming:
	def __init__(self, data_type):
		self.iter_num = []
		self.distance_path = []
		self.coordinates = data_loader(10)
		self.iteration = 200 * len(self.coordinates)
		self.data = data_loader(data_type)
		self.matrix = distance_matrix(self.data)
		self.start_node = 0
		self.cost = 0
		self.cost_list = []
		self.done_city = [0]
		self.array = [[0] * (2 ** len(self.matrix)) for i in range(len(self.matrix))]

	def transfer(self, sets):
		su = 0
		for s in sets:
			su = su + 2 ** s
		return su

	def tsp(self):
		num = len(self.matrix)
		cities = list(range(num))
		cities.pop(cities.index(self.start_node))
		self.cost = self.solve(self.start_node, cities)
		return self.cost

	def solve(self, node, future_sets):
		if len(future_sets) == 0:
			return self.matrix[node][self.start_node]
		distance = []
		for i in range(len(future_sets)):
			s_i = future_sets[i]
			copy = future_sets[:]
			copy.pop(i)
			distance.append(self.matrix[node][s_i] + self.solve(s_i, copy))
		d = min(distance)
		next_one = future_sets[distance.index(d)]
		c = self.transfer(future_sets)
		self.array[node][c] = next_one
		
		return d

	def print_result(self):
		lists = list(range(len(self.matrix)))
		start = self.start_node
		while len(lists) > 0:
			lists.pop(lists.index(start))
			m = self.transfer(lists)
			next_node = self.array[start][m]
			self.done_city.append(next_node)
			start = next_node
		print('TSP order:', [x+1 for x in self.done_city], 'Distance cost:', round(self.cost, 6))


	def plot_map(self):
		turtle.screensize(600, 800)
		turtle.speed(0)
		turtle.hideturtle()
		r_city = 8
		x_resize = 0.2
		y_resize = 0.18
		off_set = 300
		turtle.pensize(4)
		turtle.penup()
		(x, y) = (int(self.data[self.done_city[0]][0]), int(self.data[self.done_city[0]][1]))
		(x, y) = (x * x_resize - off_set, y * y_resize - off_set)
		turtle.goto(x, y)
		turtle.pendown()
		turtle.pencolor('green')
		turtle.circle(r_city)
		for i in range(1, len(self.done_city) - 1):
			(x, y) = (int(self.data[self.done_city[i]][0]), int(self.data[self.done_city[i]][1]))
			(x, y) = (x * x_resize - off_set, y * y_resize - off_set)
			turtle.pencolor('orange')
			turtle.goto(x, y)
			turtle.pencolor('blue')
			turtle.circle(r_city)
		turtle.done()


def main_dynamic(tp=10):
	tsp_ = DynamicProgramming(tp)
	tsp_.tsp()
	tsp_.print_result()
	tsp_.plot_graphic()
	if Plot_map:
		tsp_.plot_map()


if __name__ == "__main__":
	s_time = time.clock()

	Debug = False			
	Plot_map = True			
	tsp = 10				
	
	main_dynamic(tsp)

	e_time = time.clock()
	print('Time cost:', round(e_time - s_time, 6))
