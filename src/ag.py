#４６ぬこだよ～ (っ◕‿◕)っ

from matplotlib.pyplot import plot, show, clf, subplots, grid, savefig

import math
import numpy
import random
import struct
import sys

# size of chromossome in bits
L = 4 * 8

if len(sys.argv) >= 4:
	max_generations = int(sys.argv[1])
	population_max = int(sys.argv[2])
	mutation_rate = float(sys.argv[3])
else:
	max_generations = 650
	population_max = 100
	mutation_rate = 0.01

class chromossome:
	def __init__(self, value):
		self.value = value

	fitness_value = 0
	selection_chance = 0

def floatToBits(f):
	s = struct.pack('>f', f)
	return struct.unpack('>L', s)[0]

def bitsToFloat(b):
	s = struct.pack('>L', b)
	return struct.unpack('>f', s)[0]

def get_bits(x):
	x = floatToBits(x)
	N = 4 * 8
	bits = ''
	for bit in range(N):
		b = x & (2**bit)
		bits += '1' if b > 0 else '0'
	return bits

def get_float(bits):
	x = 0
	assert(len(bits) == L)
	for i, bit in enumerate (bits):
		bit = int(bit) # 0 or 1
		x += bit * (2**i)
	return bitsToFloat(x)

def fitness_function(value):
	return value + math.fabs(math.sin(32 * value))

def fitness_value_sum(population):
	fitness_sum = 0

	for i in range(len(population)):
		individual = population[i]
		fitness_sum += individual.fitness_value

	return fitness_sum

def roulette_chance_assign(population):
	fitness_sum = fitness_value_sum(population)
	for i in range(len(population)):
		individual = population[i]
		individual.selection_chance = individual.fitness_value / fitness_sum

def select_individuals_by_roulette(population):
	selection_chance_array = []
	for individual in population:
		selection_chance_array.append(individual.selection_chance)
	try:
		selected_individual = random.choices(population, selection_chance_array, k = 1)
	except ValueError:
		print("ERROR: At least one of your populations is entirely dead, boohoo... :(")
		print("Here's a tip: Don't abuse the mutation, it's dangerous! Haven't you heard about the dangers of radiation?")
		exit()
	return selected_individual

def generate_offspring(population):
	offsprings = []
	for i in range(0, population_max):
		mom = get_bits(select_individuals_by_roulette(population)[0].value)
		dad = get_bits(select_individuals_by_roulette(population)[0].value)

		while mom == 0 and dad == 0:
			mom = get_bits(select_individuals_by_roulette(population)[0].value)
			dad = get_bits(select_individuals_by_roulette(population)[0].value)

		while mom == dad:
			mom = get_bits(select_individuals_by_roulette(population)[0].value)

		slicing_point = 15
		child1 = dad[:slicing_point] + mom[slicing_point:]
		child2 = mom[:slicing_point] + dad[slicing_point:]
		offsprings.append(chromossome(get_float(child1)))
		offsprings.append(chromossome(get_float(child2)))
	return offsprings

def mutate(offsprings):
	for chromossome in offsprings:
		random_num = random.random()
		if random_num < mutation_rate:
			chromossome_bin = get_bits(chromossome.value)
			mutated_chromossome = random.randint(0, 31)
			mutated_chromossome_string = '0' if str(chromossome_bin[mutated_chromossome]) == '1' else '1'

			chromossome.value = get_float(chromossome_bin[:mutated_chromossome] + mutated_chromossome_string + chromossome_bin[mutated_chromossome+1:])

def remove_dead_offspring(offsprings):
	for offspring in offsprings:
		if offspring.value > math.pi:
			offspring.value = 0
			offspring.fitness_value = 0
			offspring.selection_chance = 0

def main_loop(average_fitness):
	print("Generating generations and offsprings...")
	population = []
	offsprings = []
	all_populations = []
	for gen in range(max_generations):
		fitness_array = []
		for i in range(population_max):
			if gen == 0:
				population.append(chromossome(random.uniform(0, math.pi)))
			individual = population[i]
			individual.fitness_value = fitness_function(individual.value)
			fitness_array.append(individual.fitness_value)
		
		average_fitness.append(numpy.mean(fitness_array))
		roulette_chance_assign(population)
		all_populations.append(population)
		offsprings = generate_offspring(population)
		mutate(offsprings)
		remove_dead_offspring(offsprings)
		population = offsprings
	return all_populations

def plot_mean_graph(average_fitness):
	print("Generating mean graph...")
	fig, mean_plot = subplots()

	mean_plot.plot(average_fitness)
	mean_plot.set_title('Genetic Algorithm for maximizing the function f(y) = y + |(sin(32 * value)|')
	mean_plot.set_xlabel('Generations')
	mean_plot.set_ylabel('f(y) = y + |(sin(32 * value)|')
	mean_plot.grid()

	fig.savefig("mean.png")
	show()

def plot_distribution_graph(all_populations):
	print("Generating distribution graphs...")

	xs = numpy.linspace(0, math.pi, num = 200)
	ys = [fitness_function(x) for x in xs.tolist()]

	plot_distribution_of_first_gen(xs, ys, all_populations)
	plot_distribution_of_tenth_gen(xs, ys, all_populations)
	plot_distribution_of_last_gen(xs, ys, all_populations)

def plot_distribution_of_first_gen(xs, ys, all_populations):
	fig, _plot = subplots()

	_plot.plot(xs, ys)
	xcand, ycand = [], []
	for individual in all_populations[0]:
		x = individual.value
		y = individual.fitness_value
		xcand.append(x)
		ycand.append(y)

	_plot.plot(xcand, ycand, '.')
	_plot.set_title('Distribution of Individuals from the first population on the Fitness values.')
	_plot.set_xlabel('Values From 0 to Pi')
	_plot.set_ylabel('Fitness Value')
	_plot.annotate("A fitness value of 0 means a dead individual", xy = (1, 1))
	_plot.annotate("(won't participate in the selection)", xy = (1, 0.7))
	_plot.grid()

	fig.savefig("individual_distribution_gen_0.png")
	show()

def plot_distribution_of_tenth_gen(xs, ys, all_populations):
	fig, _plot = subplots()

	_plot.plot(xs, ys)
	xcand, ycand = [], []
	for individual in all_populations[9]:
		x = individual.value
		y = individual.fitness_value
		xcand.append(x)
		ycand.append(y)

	_plot.plot(xcand, ycand, '.')
	_plot.set_title('Distribution of Individuals from the tenth population on the Fitness values.')
	_plot.set_xlabel('Values From 0 to Pi')
	_plot.set_ylabel('Fitness Value')
	_plot.annotate("A fitness value of 0 means a dead individual", xy = (1, 1))
	_plot.annotate("(won't participate in the selection)", xy = (1, 0.7))
	_plot.grid()

	fig.savefig("individual_distribution_gen_10.png")
	show()

def plot_distribution_of_last_gen(xs, ys, all_populations):
	fig, _plot = subplots()

	_plot.plot(xs, ys)
	xcand, ycand = [], []
	for chromossome in all_populations[-1]:
		x = chromossome.value
		y = chromossome.fitness_value
		xcand.append(x)
		ycand.append(y)

	_plot.plot(xcand, ycand, '.')
	_plot.set_title('Distribution of Individuals from the last population on the Fitness values.')
	_plot.set_xlabel('Values From 0 to Pi')
	_plot.set_ylabel('Fitness Value')
	_plot.annotate("A fitness value of 0 means a dead individual", xy = (1, 1))
	_plot.annotate("(won't participate in the selection)", xy = (1, 0.7))
	_plot.grid()

	fig.savefig("individual_distribution_gen_last.png")
	show()

average_fitness = []

all_populations = main_loop(average_fitness)

plot_mean_graph(average_fitness)
plot_distribution_graph(all_populations)
