"""
Genetic Algorithm
Author: Jiawei Wang
Date: Mar 27, 2020

Please read README before running this program

Notice: the default number of loops is set to be 100, you can change to whatever you like
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
    12: [60, 1]
}

# Minimum change in max value for program to continue looping
finish_limit = 5

# Backpack weight limit
weight_limit = 250

# Number of samples that can reproduce
selected_number = 5

# Number of genes
chromosome_size = 12

max_last = 0
diff_last = float("inf")

# Initialize 10 samples
def init():
    init_states = []
    for i in range(12):  # 12 genes in total
        x = random.randint(1, 4095)  # 4095 is 12 '1's in binary
        init_states.append(bin(x)[2:])
    return init_states


# Fitness function
def fitness(chromosome_states):
    fitnesses = []
    for state in chromosome_states:
        value = 0
        weight = 0
        for i, v in enumerate(state):
            if v == '1':
                weight += items[i+1][0]
                value += items[i+1][1]
        fitnesses.append([value, weight])
    return fitnesses


# Check the requirement
def is_finished(fitnesses):
    global max_last  # max value in last generation (parent generation)
    global diff_last  # change of max value between  parent and grandparent
    max_current = 0  # store max value
    for v in fitnesses:
        if v[1] > max_current:
            max_current = v[1]
    print("Current max value is: ", max_current)
    diff = max_current - max_last  # change of max value between this generation and parent
    if diff < finish_limit:
        return True
    else:
        diff_last = diff
        max_last = max_current
        return False


# Select "strong" samples
def filter(chromosome_states, fitnesses):
    index = len(fitnesses) - 1
    while index >= 0:
        index -= 1
        if fitnesses[index][1] > weight_limit:
            chromosome_states.pop(index)
            fitnesses.pop(index)
    selected_index = [0] * len(chromosome_states)
    for i in range(selected_number):
        j = chromosome_states.index(random.choice(chromosome_states))
        selected_index[j] += 1
    return selected_index


# Reproduce
def crossover(chromosome_states, selected_index):
    chromosome_states_new = []
    index = len(chromosome_states) - 1
    # print 'index:',index
    while index >= 0:  # 遍历完所有的染色体组的染色体（其中下标-1代表最后一个染色体的索引）
        print('index:', index)
        index -= 1
        chromosome_state = chromosome_states.pop(index)
        print('chromosome_states_3:', chromosome_states)  # 弹出后的染色体组
        print('chromosome_state:', chromosome_state)  # 弹出的染色体
        for i in range(selected_index[index]):
            chromosome_state_x = random.choice(chromosome_states)  # 随机选择一个染色体
            print('chromosome_state_x:', chromosome_state_x)
            pos = random.choice(range(1, chromosome_size - 1))  # 随机[1, 2, 3, 4]其中的一个数
            print('pos:', pos)
            chromosome_states_new.append(chromosome_state[:pos] + chromosome_state_x[pos:])
            print('chromosome_states_new:', chromosome_states_new)
        chromosome_states.insert(index, chromosome_state)  # 恢复原染色体组
        print('chromosome_states_4:', chromosome_states)
    return chromosome_states_new  # 返回得到的新的染色体组


# Let's run this program
print("Program started")
chromosome_states = init()  # get 10 random samples
print("First generation: ")
print(chromosome_states)

loop = 100  # total number of generations
while loop > 0:
    loop -= 1
    fitnesses = fitness(chromosome_states)  # Calculate Fitness
    if is_finished(fitnesses):  # check if we get the desired sample
        break
    print("Fitnesses are: ")
    print(fitnesses)
    selected_index = filter(chromosome_states, fitnesses)
    print("Index of selected samples for reproduce: ", selected_index)
    print("Genes of selected samples: ", chromosome_states)
    chromosome_states = crossover(chromosome_states, selected_index)  # reproduce
    print("After reproduce: ", chromosome_states)
fitnesses = fitness(chromosome_states)
print("------------------------------------------------")
print("Genetic Algorithm finished, here are the results:")
print("Samples are: ", chromosome_states)
print("Fitnesses are:", fitnesses)




