import random
import math
import argparse
import time
import sys
import mmh3
import numpy as np
from heapq import heapify, heappop, heappush

# define the ceil
totalShingles = (1 << 32) - 1


def MaxLog(k, seed, stream, randomNoA, randomNoB):
    """
    :param k
    :param seed: a random seed
    :param stream:
    :param randomNoA: a seed array
    :param randomNoB: also a seed array
    :return: maxShingleID, a dictionary like {'setA':[[Mu list],[Su list]],'setB':[[Mu list],[Su list]],...}
    """
    maxShingleID = {}

    for item in stream:
        # item:[id, val]

        if item[0] in maxShingleID.keys():
            # Mu: maxShingleID[item[0]][0]
            # Su: maxShingleID[item[0]][1]

            for x in range(0, k):
                # uniform(0,1)?
                temp = ((randomNoA[x] * mmh3.hash(str(item[1]), seed) + randomNoB[x]) % totalShingles)
                # print("temp1:"+str(temp))
                #map temp to (0,1)
                temp = temp / float(totalShingles)
                # print("temp2:" + str(temp))
                # ceil(-log2(temp))
                hash_val = math.ceil(- math.log(temp, 2))

                # update Mu[x],Su[x]
                if hash_val > maxShingleID[item[0]][0][x]:
                    maxShingleID[item[0]][0][x] = hash_val
                    maxShingleID[item[0]][1][x] = 1
                elif hash_val == maxShingleID[item[0]][0][x]:
                    maxShingleID[item[0]][1][x] = 0
        else:
            maxShingleID[item[0]] = [[-1] * k, [0] * k]
    return maxShingleID


def hash_parameter(k):
    """
    return a list of k distinct numbers between 0 and  (1 << 32) - 1
    """
    randList = []
    randIndex = random.randint(0, totalShingles - 1)
    randList.append(randIndex)
    while k > 0:
        while randIndex in randList:
            randIndex = random.randint(0, totalShingles - 1)
        randList.append(randIndex)
        k = k - 1

    return randList


def estimate(k, maxShingleID, set1, set2):
    """

    :param k:
    :param maxShingleID: a dictionary like {'setA':[[Mu list],[Su list]],'setB':[[Mu list],[Su list]],...}
    :param set1: id of set1
    :param set2: id of set2
    :return:
    """
    con = 0
    for x in range(0, k):
        if maxShingleID[set1][0][x] > maxShingleID[set2][0][x] and maxShingleID[set1][1][x] == 1:
            con = con + 1
        elif maxShingleID[set1][0][x] < maxShingleID[set2][0][x] and maxShingleID[set2][1][x] == 1:
            con = con + 1
    # print con
    num = float(k)
    # print num
    jaccard_sim = 1.0 - con * (1 / num) * (1 / 0.7213)
    return jaccard_sim


def generate_synthetic_stream(card, jaccard_true):
    """
    to generate a stream with two flows
    :param card: cardinality of each flow. cardinalities of two flows are the same.
    :param jaccard_true:
    :return: stream like [[setA,1],[setB,1],.....]
    """
    stream=[]
    total_num = card * 2
    sim = (2 * jaccard_true) / (1 + jaccard_true)
    the_same_index = total_num / 2 * sim
    setA_uni_index = total_num / 2 * 1
    setB_uni_index = total_num / 2 * (2 - sim)
    for num in range(total_num):
        if num <= the_same_index:
            stream.append(['setA', num])
            stream.append(['setB', num])
        elif num <= setA_uni_index:
            stream.append(['setA', num])
        elif num <= setB_uni_index:
            stream.append(['setB', num])
        else:
            break
    return stream

if __name__ == "__main__":
    # # seed
    random_seed = 1
    #
    # # size of maxloghash
    k = int(128)
    #
    jaccard_true = 0.5
    #
    # # two seed arrays for generating k hash functions
    randomNoA = hash_parameter(k)
    print(randomNoA)
    randomNoB = hash_parameter(k)
    print(randomNoB)
    #
    stream = generate_synthetic_stream(10000, jaccard_true)
    print(stream)
    maxShingleID = MaxLog(k, random_seed, stream, randomNoA, randomNoB)
    print(maxShingleID)
    jaccard_est = estimate(k, maxShingleID, 'setA', 'setB')
    print(jaccard_true, jaccard_est)

    print(math.ceil(- math.log(0.000000000001, 2)))