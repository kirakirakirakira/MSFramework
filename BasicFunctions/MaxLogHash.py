import random
import math
import time
import mmh3
import numpy as np
import json
import pandas as pd
# define the ceil
totalShingles = (1 << 32) - 1


class MaxLog:
    def __init__(self, k, seed, randomNoA, randomNoB):
        """
        初始化MaxLog类
        :param k: 哈希函数的数量
        :param seed: 随机种子，用于哈希函数
        :param randomNoA: 随机数数组A，长度为k
        :param randomNoB: 随机数数组B，长度为k
        """
        self.k = k
        self.seed = seed
        self.randomNoA = randomNoA
        self.randomNoB = randomNoB
        self.maxShingleID = [[-1] * self.k, [0] * self.k] # 存储流的MaxLog状态，结构： [[Mu列表], [Su列表]]

    def process_item(self, item_value):
        """
        处理单个数据项，更新对应的MaxLog状态
        :param item_value: 流中的元素值（如目标IP）
        """
        # 如果流不存在，初始化其Mu和Su数组

        # 遍历每个哈希函数
        for x in range(self.k):
            # 计算哈希值
            hash_val = mmh3.hash(str(item_value), self.seed)
            # 应用线性变换并取模
            temp = (self.randomNoA[x] * hash_val + self.randomNoB[x]) % totalShingles
            temp_val = temp / float(totalShingles)

            # 处理temp_val为0的特殊情况，避免计算log(0)
            if temp_val == 0:
                temp_val = 1.0 / (totalShingles + 1)

            # 计算哈希层级
            hash_level = math.ceil(-math.log(temp_val, 2))

            # 更新Mu和Su
            current_mu = self.maxShingleID[0][x]
            current_su = self.maxShingleID[1][x]

            if hash_level > current_mu:
                self.maxShingleID[0][x] = hash_level
                self.maxShingleID[1][x] = 1
            elif hash_level == current_mu:
                self.maxShingleID[1][x] = 0
    def get_max_shingle_id(self):
        """
        获取当前存储的MaxLog状态
        :return: 字典格式的MaxLog状态
        """
        return self.maxShingleID






def get_filtered_flow_maxlog(k,seed,randomNoA, randomNoB):
    maxShingleID = {}
    with open("../processed_data/caida_ab_flow.json", "r", encoding="utf-8") as file:
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


def MaxLog_stream(k, seed, stream, randomNoA, randomNoB):
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


def hash_parameter(k, seed):
    """
    生成可复现的确定性参数数组
    :param k: 需要生成的参数数量
    :param seed: 基础种子值（确保可复现性）
    :return: 包含k个唯一参数的列表
    """
    parameters = []
    for x in range(k):
        # 为每个参数生成唯一哈希种子
        hash_seed = mmh3.hash(f"param_{x}", seed) & 0xFFFFFFFF  # 添加索引确保唯一性

        # 生成参数并确保在有效范围内
        param = mmh3.hash(str(x), hash_seed) % totalShingles

        # 处理哈希冲突（概率极低，但为了健壮性保留）
        while param in parameters:
            hash_seed += 1
            param = mmh3.hash(str(x), hash_seed) % totalShingles

        parameters.append(param)
    return parameters


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


def estimate_maxlog_jaccard_similarity(maxlog1:MaxLog,maxlog2:MaxLog,k):
    """

    :param maxlog1:
    :param maxlog2:
    :param k:
    :return:
    """
    con=1
    for x in range(k):
        if maxlog1.maxShingleID[0][x]>maxlog2.maxShingleID[0][x] and maxlog1.maxShingleID[1][x]==1:
            con+=1
        elif maxlog1.maxShingleID[0][x]<maxlog2.maxShingleID[0][x] and maxlog2.maxShingleID[1][x]==1:
            con+=1
    jaccard_sim = 1.0 - con * (1 / k) * (1 / 0.7213)
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
        randomNoA = hash_parameter(k,k)
        #print(randomNoA)
        randomNoB = hash_parameter(k,k+1)
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
        maxShingleID = MaxLog_stream(k, random_seed, stream, randomNoA, randomNoB)
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
        df.to_csv('processed_data/maxlog_experiment_result.csv', mode='a', header=False, index=False)