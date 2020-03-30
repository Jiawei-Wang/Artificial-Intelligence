"""
COMP 131 AI Assignment 04
Genetic Algorithm for Backpack Problem
Author: Jiawei Wang
Date: Mar 30, 2020


Please read README.txt before running this program


!!!NOTICE!!!:  (PLEASE READ)

In order to implement as many functions as possible in this algorithm (Fitness Calculation, Crossing, Mutation, etc), I
enforced every generation to go through all these functions, which in nature do not happen all the time.

So the major consequence of this decision is: Even though sometimes the algorithm gets some prefect samples (with weight
close to 250 and relative high value), it still enforces these sample to cross and randomly mutate, which can mostly
damage the genes and lead to a worse generation (that is to say the best sample in offspring generation even has lower
weight and value compared to parent generation).

Because in every generation I only have 10 samples and select no more than 5 of them (otherwise it is impossible to
output every generation on the screen and the program consumes too much time to run), so the genes in this small group
is very unstable, Crossing and Mutation can be disastrous (Similar in Biology, if the size of one species is small,
then most of the time they extinct after several generations).

So when you finish running this program, sometimes you will get bad results (for example: weight 100, value 8), in order
to solve this problem, you need to run this program several times and read through the "evolution record"
"""


import random

# Initialize the items dictionary
items = {  # number : [weight, value]
    1:  [20, 6],
    2:  [30, 5],
    3:  [60, 8],
    4:  [90, 7],
    5:  [50, 6],
    6:  [70, 9],
    7:  [30, 4],
    8:  [30, 5],
    9:  [70, 4],
    10: [20, 9],
    11: [20, 2],
    12: [60, 1]}

# Maximum weight for backpack
weight_limit = 250

# max value in last generation (parent generation), initialized as 0 for first generation
max_last = 1

# change of max value between parent and grandparent generation, initialized as inf for first generation
diff_last = float("inf")

# minimum improvement of current generation over parent generation for program to continue looping
finish_limit = 2

# maximum number of samples that can reproduce off-springs
selected_number = 5

# Number of genes on a sample
chromosome = len(items)


# Randomly initialize 10 samples, each sample is a string consists of 12 random '0's and '1's
def init():
    init_states = []
    for i in range(10):
        x = random.randint(1, 4095)  # 4095 is 12 '1's in binary
        binary = str(bin(x)[2:])
        while len(binary) < chromosome:
            binary = "0"+binary
        init_states.append(binary)
    return init_states  # pack 10 string into a 1-D list


# Fitness function
def fitness(chromosome_states):
    fitness_list = []
    for sample in chromosome_states:
        value = 0
        weight = 0
        for index, gene in enumerate(sample):
            if gene == '1':  # if an item is selected to be put into the backpack
                weight += items[index+1][0]
                value += items[index+1][1]
        fitness_list.append([weight, value])
    return fitness_list  # fitness list is a 2-D list with [weight, value] for all 10 samples


# Check the requirement
def is_finished(fitness_list):
    global max_last
    global diff_last
    max_current = 0  # store max value
    for element in fitness_list:
        if element[1] > max_current:
            max_current = element[1]
    diff = max_current - max_last  # change of max value between current generation and parent generation
    if 0 <= diff < finish_limit:
        return True
    else:
        diff_last = diff  # record max value difference between current generation and parent generation
        max_last = max_current  # record max value for current generation
        return False


# Select the 5 best samples for reproduction
def selection(chromosome_states, fitness_list):
    legit_sample = []  # store legit samples of current generation
    selected_list = []
    for index in range(len(chromosome_states)):
        if fitness_list[index][0] <= weight_limit:
            # [value, weight, genes]
            legit_sample.append([fitness_list[index][1], fitness_list[index][0], chromosome_states[index]])
    if len(legit_sample) <= selected_number: # if legit samples are less than or equal to 5, all are selected
        for i in range(len(legit_sample)):
            selected_list.append(str(legit_sample[i][2]))
    else:  # if legit samples are more than 5, we choose the first 5 with highest value
        selection = sorted(legit_sample, key=lambda x: x[0])
        for i in range(selected_number):
            selected_list.append(str(selection[i][2]))
    return selected_list  # 1-D list of samples (caution: selected list may contain less than 5 samples)


# Reproduce next generation
def reproduce(selected_list):
    offspring = []
    while len(offspring) < 10:
        mom, dad = random.sample(selected_list, 2)  # randomly select 2 different samples from the strong samples
        index = random.randint(1, chromosome-2)  # [1, 10], which means we keep at least 1 gene from each parent
        baby = mom[:index] + dad[index:]
        offspring.append(baby)
    return offspring  # 1-D list with 10 new next-generation samples


# Randomly mutate offsprings
def mutation(offspring):
    chromosome_states = []
    for sample in offspring:
        mutate = random.choice([True, False])
        if mutate:
            index = random.randint(0, chromosome - 1)
            temp = list(sample)
            temp[index] = str(abs(1-int(temp[index])))  # if the original gene is 1, change to 0 (if 0, change to 1)
            sample = "".join(temp)
        chromosome_states.append(sample)
    return chromosome_states


# Let's run this program
print("---------------------------------------------------------------------")
print("Nature Selection Pro 3000 started!")
chromosome_states = init()  # get 10 random samples
print("The 10 samples of first generation are: ")
print(chromosome_states)
print("---------------------------------------------------------------------")

generation_loop = 100
while generation_loop > 0:  # reproduce 100 generations until the requirement is met
    generation_loop -= 1
    print("Generation No.", 100-generation_loop)
    fitness_list = fitness(chromosome_states)
    print("Fitness [weight, value] of current generation samples are:")
    print(fitness_list)
    if is_finished(fitness_list):  # if samples of current generation meet the requirement
        print("This generation meets the requirement, program terminated")
        print("---------------------------------------------------------------------")
        break
    print("This generation does not meet the requirement, reproduction continues")
    print("---------------------------------------------------------------------")
    selected_list = selection(chromosome_states, fitness_list)  # choose which samples can reproduce
    offspring = reproduce(selected_list)  # reproduce next generation
    chromosome_states = mutation(offspring)  # mutation within next generation and repeat whole process

selected_list = selection(chromosome_states, fitness_list)
print("The fittest samples for the last generation are:")
print(selected_list)
result = fitness(selected_list)
print("Their weight and value are:")
print(result)






