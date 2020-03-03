"""
# Comp 131 AI
# HW2
# Jiawei Wang
# 02/23/2020
"""

"""
# Please read the attached document 'HW2-pancake-readme' before executing this program
# A random stack will be generated each time you run this program so no input is needed
# Just click 'RUN' and enjoy!
# PS: the initial and goal pancake stacks are set to have 10 layers, if this program takes too long to run, 
# you can change the layer on line 17 just below 
"""

# How many layers should this pancake stack be?
pancakeLen = 10

from random import shuffle

# Define the backward cost function
def backwardCost(path):
    return len(path)


# Successor function
def flipStack(flipPos, pancakeStack):
    pancakeList = list(pancakeStack)
    notFlippedSide = pancakeList[0:flipPos]
    flippedSide = pancakeList[flipPos:]
    flippedSide.reverse()
    flippedStack = notFlippedSide + flippedSide
    return tuple(flippedStack)


# Print path in the result
def printPath(path):
    currVal = ()
    nodesPrinted = 0
    step = 0
    while nodesPrinted < len(path):
        for child, parent in path.items():
            if parent == currVal:
                print("Step No.", step, ":", child)
                step += 1
                currVal = child
                nodesPrinted += 1


# Initialize the pancake stack
def startSearch():
    frontier = {}
    path = {}
    visited = []

    # Randomize the initial stack
    start = [i for i in range(2, pancakeLen+1)]
    shuffle(start)
    start.insert(0,1)
    initial = tuple(start)
    goal = tuple([i+1 for i in range(pancakeLen)])
    UCS(initial, goal, frontier, path, visited)


# Implement A* search algorithm
def UCS(initial, goal, frontier, path, visited):
    # initialize all the data structures
    frontier[initial] = 0
    path[initial] = ()
    visited.append(initial)

    while frontier:
        # Find the minimum cost
        current = min(frontier.keys(), key=(lambda k: frontier[k]))
        frontier.pop(current)

        # Goal test
        if current == goal:
            print("---------------------------------")
            print("Pancake Flipper Pro 3000 Activated")
            print("Mode: UCS")
            print("Initial State: ", initial)
            print("Goal State: ", goal)
            print("More State to expand: ", printPath(path))
            print("Number of Flips (cost): ", (len(path) - 1))
            print("Number of Nodes Visited: ", len(visited))
            print("MISSION COMPLETE!")
            print("---------------------------------")
            break

        for i in range(1, len(current) - 1):
            flipped = flipStack(i, current)
            if flipped not in visited:
                curCost = len(path) - 1
                frontier[flipped] = curCost

        # Keep track of the current node in the path
        minNewChild = min(frontier.keys(), key=(lambda k: frontier[k]))
        path[minNewChild] = current
        visited.append(current)


startSearch()