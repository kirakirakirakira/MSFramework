import math
import random
from collections import Counter
import sys
from matplotlib import pyplot as plt
import time
import json
from simiSketch import jaccard_similarity,jaccard_est_of_simiSketch_CM

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
    print(f"构建<f,e>字典执行时间: {execution_time:.2f} 秒")
    return flow_dict

def load_json():
    starttime=time.time()
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
    endtime = time.time()
    execution_time=endtime-starttime
    print(f"导入异常流并构建字典执行时间: {execution_time:.2f} 秒")
    return flow_dict
if __name__ == "__main__":
    starttime=time.time()
    all_data_dict=data_analyze()
    ab_data_dict=load_json()
    print("length of all_data_dict is %d"%len(all_data_dict.keys()))
    print("length of ab_data_dict is %d" % len(ab_data_dict.keys()))
    rounds=len(all_data_dict.items())*len(ab_data_dict.items())
    print("rounds: %d"%rounds)

    onetenthrounds=rounds//10000
    ct=0
    abnormal_flow_larger_than_0_5=set()
    abnormal_flow_larger_than_0_6 = set()
    for key1, value1 in all_data_dict.items():
        for key2, value2 in ab_data_dict.items():
            simi=jaccard_similarity(value1,value2)
            if simi>0.6:
                print("flow %s is similar to abnormal flow %s with rate %.2f"%(key1,key2,simi))
                abnormal_flow_larger_than_0_6.add(key1)
            if simi>0.5:
                print("flow %s is similar to abnormal flow %s with rate %.2f"%(key1,key2,simi))
                abnormal_flow_larger_than_0_5.add(key1)
            ct += 1
        if ct%onetenthrounds==0:
            print("%d/10000 complete."%(ct//onetenthrounds))
            endtime=time.time()

            print("%.2f seconds has passed."%(endtime-starttime))




    # 转换为列表并存入 JSON 文件
    with open("abnormal_flow_larger_than_0_5.json", "w", encoding="utf-8") as file:
        json.dump(list(abnormal_flow_larger_than_0_5), file, indent=4)
    with open("abnormal_flow_larger_than_0_6.json", "w", encoding="utf-8") as file:
        json.dump(list(abnormal_flow_larger_than_0_6), file, indent=4)

    endtime = time.time()
    fulltime=endtime-starttime
    print("总执行时间 %.2f seconds (%d minutes)" % (fulltime,fulltime//60))


