'''
1. 初始化10个样本（每个是12位的binary，输出为10个字符串的一维list）                     finished
2. Print：初代样本为。。。                                                        finished
3. 以下步骤loop 100次除非提前达到目标：                                             finished
4. 计算适应度（输入10个样本的list，输出为10个样本的重量和价值的二维list）                 finished
5. 判断是否达到停止loop的标准（输入为二维list，输出为true/false）                      finished
6. 如果达到标准，输出最优解，如果没有，进入步骤7
7. 找到进行繁殖的5个样本（输入为一维list和二维list，输出为符合要求的样本中的前五名）        finished
8. 对这五个样本进行繁殖（输入为5个样本，输出为10个后代）
9. 对10个后代进行突变（输入为10个后代，输出为随机突变后的10个后代）
10. 返回步骤4
'''

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
max_last = 0

# change of max value between parent and grandparent generation, initialized as inf for first generation
diff_last = float("inf")

# minimum improvement of current generation over parent generation for program to continue looping
finish_limit = 2

# maximum number of samples that can reproduce off-springs
selected_number = 5

# Randomly initialize 10 samples, each sample is a string consists of 12 random '0's and '1's
def init():
    init_states = []
    for i in range(10):
        x = random.randint(1, 4095)  # 4095 is 12 '1's in binary
        binary = str(bin(x)[2:])
        while len(binary) < 12:
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
    print("Max value for current generation is: ", max_current)
    diff = max_current - max_last  # change of max value between current generation and parent generation
    if diff < finish_limit:
        return True
    else:
        diff_last = diff  # record max value difference between current generation and parent generation
        max_last = max_current  # record max value for current generation
        return False


# Select the 5 best samples for reproduction
def selection(chromosome_states, fitness_list):
    legit_sample = []  # store legit samples of current generation
    selected_list = {}
    for index in range(len(chromosome_states)):
        if fitness_list[index][0] <= weight_limit:
            # [value, weight, genes]
            legit_sample.append([fitness_list[index][1], fitness_list[index][0], chromosome_states[index]])
    if len(legit_sample) <= selected_number: # if legit samples are less than or equal to 5, all are selected
        for i in range(len(legit_sample)):
            selected_list[legit_sample[i][2]] = [legit_sample[i][1], legit_sample[i][0]]
    else:  # if legit samples are more than 5, we choose the first 5 with highest value
        selection = sorted(legit_sample, key=lambda x: x[0])
        for i in range(selected_number):
            selected_list[selection[i][2]] = [selection[i][1], selection[i][0]]
    return selected_list  # genes : [weight, value] (caution: selected list may not always contain 5 selected samples)


# Reproduce next generation
def reproduce(selected_list):



# Let's run this program
print("Nature Selection Pro 3000 started!")
chromosome_states = init()  # get 10 random samples
print("The 10 samples of first generation are: ")
print(chromosome_states)
generation_loop = 100
while generation_loop > 0:  # reproduce 100 generations until the requirement is met
    generation_loop -= 1
    fitness_list = fitness(chromosome_states)
    print("Fitness of current generation samples are [weight, value]:")
    print(fitness_list)
    if is_finished(fitness_list):  # if samples of current generation meet the requirement
        print("This generation meets the requirement, program terminated")
        break
    print("This generation does not meet the requirement, reproduction continues")
    selected_list = selection(chromosome_states, fitness_list)  # choose which samples can reproduce
    next_generation = reproduce(selected_list)







