import math
import random
from collections import Counter
import sys
from matplotlib import pyplot as plt
import time
import json
from simiSketch import jaccard_similarity

def random_pick_ips(counter, n):
    """

    :param counter:
    :param n:
    :return: random n ip from counter
    """

    # 获取所有IP地址
    ip_list = [key for key, val in counter]
    # 从中随机挑选n个，不放回
    return random.sample(ip_list, min(n, len(ip_list)))

def data_analyze():

    # 记录开始时间
    start_time = time.time()
    # 文件路径
    file_path = ["../data1/02.txt","../data1/00.txt","../data1/01.txt","../data1/03.txt","../data1/04.txt"]

    # 用于存储源 IP 地址的计数器

    flow_dict={}

    #update counter return ip-frequency pairs
    for path in file_path[:1]:
    # 逐行读取文件并统计源 IP 地址
        with open(path, "r", encoding="utf-8") as file:
            lines = file.readlines()
            for line in lines:
                # 去掉行尾换行符，并按空格分割
                parts = line.strip().split()
                if len(parts) == 2:  # 确保格式正确
                    source_ip = parts[0]  # 第一个部分是源 IP 地址
                    destination_ip=parts[1]
                    if source_ip not in flow_dict:
                        flow_dict[source_ip] = {}
                    if destination_ip not in flow_dict[source_ip]:
                        flow_dict[source_ip][destination_ip] = 0
                        # 增加计数
                    flow_dict[source_ip][destination_ip] += 1

    end_time1 = time.time()

    # 计算并打印执行时间
    execution_time = end_time1 - start_time
    print(f"统计部分代码执行时间: {execution_time:.2f} 秒")
    return flow_dict

def load_json():
    with open("abnormal_data.json", "r", encoding="utf-8") as file:
        original_data = json.load(file)
    flow_dict = {}
    # 遍历原始数据，统计每个 destination_ip 的出现次数
    for source_ip, destinations in original_data.items():
        # 确保 source_ip 在 flow_dict 中有对应的字典
        if source_ip not in flow_dict:
            flow_dict[source_ip] = {}

        # 遍历目标 IP 列表，统计频次
        for destination_ip in destinations:
            if destination_ip not in flow_dict[source_ip]:
                flow_dict[source_ip][destination_ip] = 0

            # 增加计数
            flow_dict[source_ip][destination_ip] += 1
    return flow_dict
if __name__ == "__main__":
    all_data_dict=data_analyze()
    ab_data_dict=load_json()
    print("length of all_data_dict is %d"%len(all_data_dict.keys()))
    print("length of ab_data_dict is %d" % len(ab_data_dict.keys()))
    ct=1
    for key1, value1 in all_data_dict.items():
        for key2, value2 in ab_data_dict.items():
            simi=jaccard_similarity(value1,value2)
            if simi>0.6:
                print("flow %s is similar to abnormal flow %s with rate %.2f"%(key1,key2,simi))
        if ct%10000==0:
            print("round %d complete."%(ct/10000))
        ct+=1





