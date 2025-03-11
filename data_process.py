import math
import random
from collections import Counter
import sys
from matplotlib import pyplot as plt
import time
import json
from simiSketch import jaccard_similarity,jaccard_est_of_simiSketch_CM
from pprint import pprint
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




def data_analyze(data_num):
    """
    :param data_num: 输入的数据包的数量
    :return: {flow_id:{e_id:count}}字典
    """
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
            for line in lines[:data_num]:
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
    with open("filtered_flows.json", "r", encoding="utf-8") as file:
        original_data = json.load(file)
    endtime = time.time()
    execution_time=endtime-starttime
    print(f"导入异常流并构建字典执行时间: {execution_time:.2f} 秒")
    return original_data

def get_abnormal_data(data,card,freq):
    """

    :param card: 基数范围
    :param freq: 频率范围
    :param data: 经过统计的源数据
    :return: 按规则筛选过的数据，保存为json
    """
    filtered_flows = {
        flow_id: e_dict
        for flow_id, e_dict in data.items()
        if len(e_dict) > card or sum(e_dict.values()) > freq
    }
    with open("filtered_flows.json", "w") as f:
        json.dump(filtered_flows, f, indent=4)

    print("筛选后的字典已保存到 filtered_flows.json")


if __name__ == "__main__":



    starttime=time.time()
    all_data_dict=data_analyze(10000000)
    # ab_data_dict=load_json()
    print("length of all_data_dict is %d"%len(all_data_dict.keys()))
    #pprint(all_data_dict)
    # transformed_data = {
    #     flow_id: {
    #         "flow cardinality": len(e_counts),  # e_id 的唯一数量
    #         "flow size": sum(e_counts.values())  # 计数总和
    #     }
    #     for flow_id, e_counts in all_data_dict.items()
    # }
    #
    # # 保存到 JSON 文件
    # with open("transformed_output.json", "w", encoding="utf-8") as f:
    #     json.dump(transformed_data, f, indent=4, ensure_ascii=False)
    #
    # print("数据已保存到 transformed_output.json")
    #
    # get_abnormal_data(all_data_dict,10000,20000)
    #
    # with open("filtered_flows.json", "r") as f:
    #     ground_truth = json.load(f).keys()
    # print(len(ground_truth))
    # print("length of ab_data_dict is %d" % len(ab_data_dict.keys()))


