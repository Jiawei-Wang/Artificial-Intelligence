--------------------------------------
Solve Backpack Problem with Genetic Algorithm
Assignment 04 for 2020 Spring COMP 131 AI at Tufts University
Author: Jiawei Wang
Date: Mar 27, 2020

--------------------------------------
Part One: Solving process of Genetic Algorithm:

1. Define Genes and Gene types and initialize the first group
2. Allow random Mutation
3. Generate next generation with random Crossover
4. Fitness calculation
5. Nature Selection
6. Repeat 2-5
(The order can be modified based on requirement, for example, it is OK to calculate
Fitness on parents and allow only "strong" ones to reproduce)

--------------------------------------
Part Two: What is Backpack Problem:

Backpack Problem is a kind of popular NP problems, we want to fit the backpack with
items and achieve maximum of total value.

--------------------------------------
Part Three: Define Backpack Problem with Genetic Algorithm:

1. Every item is a gene (N items mean N genes), we define the gene is "1" if this items
is selected to put into the backpack and "0" if not selected
2. We initialize some random samples and each of them represents a selection of items in
the Backpack.
3. We allow them to mutate, that means we randomly change the gene (whether
an item is in the backpack or not) within a sample.
4. We calculate the Fitness of every sample and choose those "strong" samples to produce next
generation, which means we randomly crossover genes on 2 samples and make some new samples.
5. We repeat the process till one sample meets the minimum requirement of "best solution"
or till samples stop evolving.

--------------------------------------
Part Four: Potential problems before coding:

1. What if I stuck in a local maxima? (Use Steps and Diversity, but How?)
2. What if all children violate the rule (that means the weight of all items in the Backpack
excesses limit in all samples) ? Is there a way for me to retrieve back to the parent generation?
