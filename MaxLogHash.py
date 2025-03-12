import random
import math
import time
import mmh3
import numpy as np
import json
import pandas as pd
# define the ceil
totalShingles = (1 << 32) - 1
def get_filtered_flow_maxlog(k,seed,randomNoA, randomNoB):
    maxShingleID = {}
    with open("filtered_flows.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    for source_ip,des_ips in data.items():
        if source_ip not in maxShingleID.keys():
            maxShingleID[source_ip] = [[-1] * k, [0] * k]
        for des_ip in des_ips.keys():
            for x in range(0, k):
                # uniform(0,1)?
                temp = ((randomNoA[x] * mmh3.hash(str(des_ip), seed) + randomNoB[x]) % totalShingles)
                # print("temp1:"+str(temp))
                #map temp to (0,1)
                temp = temp / float(totalShingles)
                # print("temp2:" + str(temp))
                # ceil(-log2(temp))
                hash_val = math.ceil(- math.log(temp, 2))

                # update Mu[x],Su[x]
                if hash_val > maxShingleID[source_ip][0][x]:
                    maxShingleID[source_ip][0][x] = hash_val
                    maxShingleID[source_ip][1][x] = 1
                elif hash_val == maxShingleID[source_ip][0][x]:
                    maxShingleID[source_ip][1][x] = 0
    return maxShingleID


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

        if item[0] not in maxShingleID.keys():
            maxShingleID[item[0]] = [[-1] * k, [0] * k]
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

def estimate(k, maxShingleID, abnormal_maxlog,set1, set2):
    """

    :param k:
    :param maxShingleID: a dictionary like {'setA':[[Mu list],[Su list]],'setB':[[Mu list],[Su list]],...}
    :param abnormal_maxlog: a dictionary like {'setA':[[Mu list],[Su list]],'setB':[[Mu list],[Su list]],...}
    :param set1: id of set1 in maxShingleID
    :param set2: id of set2 in abnormal_maxlog
    :return:
    """
    con = 0
    for x in range(0, k):
        if maxShingleID[set1][0][x] > abnormal_maxlog[set2][0][x] and maxShingleID[set1][1][x] == 1:
            con = con + 1
        elif maxShingleID[set1][0][x] < abnormal_maxlog[set2][0][x] and abnormal_maxlog[set2][1][x] == 1:
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

def memory_calculate(k,maxlog):
    total_len=len(maxlog.keys())
    mem_KB=total_len*(32+k*(1+6))/8//1024
    print("空间占用：%d KB"%mem_KB)
    return mem_KB

def memory_calculate_card_known(k,card):
    mem_MB=card*(32+k*(1+6))/8/1024//1024
    print("空间占用：%d MB"%mem_MB)
    return mem_MB

if __name__ == "__main__":
    #seed
    random_seed = 1
    #
    #size of maxloghash
    k = int(128)
    for k in {8,24,40,56,78}:
        # two seed arrays for generating k hash functions
        randomNoA = hash_parameter(k)
        #print(randomNoA)
        randomNoB = hash_parameter(k)
        #print(randomNoB)

        memory_calculate_card_known(k, 170000)

        true_abnormal_maxlog=get_filtered_flow_maxlog(k, random_seed, randomNoA, randomNoB)
        true_abnormal_flow_id=set(true_abnormal_maxlog.keys())
        #print(true_abnormal_flow_id)
        file_path = ["../data1/02.txt", "../data1/00.txt", "../data1/01.txt", "../data1/03.txt", "../data1/04.txt"]
        for path in file_path[:1]:
            # 一次性读取文件内容到内存
            with open(path, "r", encoding="utf-8") as file:
                lines = file.readlines()[:10000000]  # 将文件所有行读入列表\
        stream=[]
        for line in lines:
            parts = line.strip().split()
            stream.append(parts)
        #print(lines)
        # stream = generate_synthetic_stream(10000, jaccard_true)
        starttime=time.time()
        maxShingleID = MaxLog(k, random_seed, stream, randomNoA, randomNoB)
        mem=int(memory_calculate(k,maxShingleID))
        endtime=time.time()
        alltime=round(endtime-starttime,2)
        print("总用时：%s 秒"%str(alltime))
        est_abnormal_flow=set()
        for true_source_ip,true_maxlog in true_abnormal_maxlog.items():
            for source_ip,maxlog in maxShingleID.items():
                if estimate(k, maxShingleID, true_abnormal_maxlog, source_ip,true_source_ip)>0.9:
                    est_abnormal_flow.add(source_ip)

        tp = len(true_abnormal_flow_id & est_abnormal_flow)  # True Positives
        fp = len(est_abnormal_flow - true_abnormal_flow_id)  # False Positives
        fn = len(true_abnormal_flow_id - est_abnormal_flow)  # False Negatives

        precision = round(tp / (tp + fp) if (tp + fp) > 0 else 0,4)
        recall = round(tp / (tp + fn) if (tp + fn) > 0 else 0,4)
        f1 = round(2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0,4)

        print(f"Precision: {precision:.4f}")
        print(f"Recall: {recall:.4f}")
        print(f"F1 Score: {f1:.4f}")
        data={
            "k":k,
            "space(KB)":mem,
            "time":alltime,
            "precision":precision,
            "recall":recall,
            "f1-score":f1,
        }
        df = pd.DataFrame([data])
        #mode='a', header=False,
        df.to_csv('maxlog_experiment_result.csv', mode='a', header=False, index=False)