'''
geneticAlgorithm.py

Genetic Algorithm Implementation

Implement genetic algorithm in Python for creating a list of N numbers that 
equal X when squared and summed together.

@author: Rajesh Sakhamuru
@version: 10/3/2019
'''
from random import randint
from random import random
from math import sqrt
from math import ceil


def newList(length, goal):
    """
    This function creates a single list of specified length with random numbers
    between 0 and the sqrt(goal) value.
    """
    lst = []
    while length > 0:
        lst.append(randint(0, ceil(sqrt(goal))))
        length -= 1
    return lst


def populationList(popSize, length, goal):
    """
    A list of lists each of specified length.
    """
    popList = []

    while popSize > 0:
        popList.append(newList(length, goal))
        popSize -= 1
    return popList


def fitness(individual, goal):
    """
    A fitness value of 0 is ideal. The higher the fitness value, the further the
    list is from the goal state.
    """
    squaredSum = 0

    for num in individual:
        squaredSum += num * num

    return abs(goal - squaredSum)


def evolve(popList, goal, retain=0.2, random_select=0.05, mutate=0.01):
    """
    Evolves the entire population of lists, selecting for lists which have the 
    best fitness (lowest value). Random mutation and random selection of some 
    members of the population prevent getting stuck at local maxima.
    """
    popGrades = []
    parents = []
    for lst in popList:
        popGrades.append(fitness(lst, goal))

    # deep copy of population List
    population = list(popList)

    parentPopSize = round(len(popList) * retain)

    # adds the percentage specified of the population to the parents list
    while parentPopSize > 0:

        fit = popGrades[0]
        count = 0
        fittest = 0
        for g in popGrades:
            if g < fit:
                fit = g
                fittest = count
            count += 1

        parents.append(population[fittest])
        population.pop(fittest)
        popGrades.pop(fittest)
        parentPopSize -= 1

    # selects some random individuals and adds them to the population as well
    for lst in population:
        if random_select > random():
            parents.append(lst)

    # random muatations for more genetic diversity
    for parent in parents:
        if mutate > random():
            randPosition = randint(0, len(parent) - 1)
            parent[randPosition] = randint(0, ceil(sqrt(goal)))

    # crossing over
    parentsLength = len(parents)
    desiredLength = len(popList) - parentsLength

    children = []

    while len(children) < desiredLength:
        par1 = randint(0, parentsLength - 1)
        par2 = randint(0, parentsLength - 1)

        if par1 != par2:
            par1 = parents[par1]
            par2 = parents[par2]
            # each parentis weighed a random amount rather than a 50/50 split
            split = randint(0, len(par1))
            child = par1[:split] + par2[split:]
            children.append(child)

    children.extend(parents)

    return children


def listOfSquaredSums(length, goal, retain=0.25, random_select=0.1, mutate=0.05):
    """
    Creates the population list and then evolves it to meat the fitness criteria
    as many times as necessary until it gets an individual list with maximum 
    fitness (fitness = 0)
    """
    popSize = 200

    popList = populationList(popSize, length, goal)

    solved = False
    count = 0

    while not solved:
        popList = (evolve(popList, goal, retain, random_select, mutate))
        print(popList)  # for troubleshooting
        for i in popList:
            if (fitness(i, goal) == 0):
                print(i)
                solved = True
                break
        if solved is True:
            break

        # will modify mutation, random_select and retain values to help leave a
        # local maxima. More randomness the longer it takes.
        if count % 20 == 0:
            if mutate < 0.5:
                mutate += 0.01
            if random_select < 0.5:
                random_select += 0.01
            if retain > 0.15:
                retain -= 0.01

        count += 1
    return


def main():
    """
    Testing three different calls to the listOfSquaredSums function which uses
    a genetic algorithm to create a list of N numbers that equal X when squared
    and summed together.
    """

    print("List of 5 numbers that equal 200 when squared and summed together:")
    listOfSquaredSums(5, 200)
    print("List of 8 numbers that equal 723 when squared and summed together:")
    listOfSquaredSums(8, 723)
    print("List of 3 numbers that equal 50 when squared and summed together:")
    listOfSquaredSums(3, 50)
    print("List of 15 numbers that equal 58976 when squared and summed together:")
    listOfSquaredSums(15, 58976)

    return


main()

