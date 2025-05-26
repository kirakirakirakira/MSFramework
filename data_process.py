import os
import random
import time
import json

from scapy.layers.inet import IP  # 新版本导入方式
from scapy.all import PcapReader


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


def data_analyze(filename,data_num=None, file_path=None):
    """
    :param filename:
    :param file_path: 文件地址
    :param data_num: 输入的数据包的数量
    :return: {flow_id:{e_id:count}}字典
    """
    # 记录开始时间

    start_time = time.time()
    # 文件路径
    # 用于存储源 IP 地址的计数器

    flow_dict = {}
    if file_path is None:
        file_path = "../data1/02.txt"

    # 逐行读取文件并统计源 IP 地址
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
        if data_num is None:
            data_num = len(lines)
        for line in lines[:data_num]:
            # 去掉行尾换行符，并按空格分割
            parts = line.strip().split()
            if len(parts): #== 2:  # 确保格式正确
                source_ip = parts[0]  # 第一个部分是源 IP 地址
                destination_ip = parts[1]
                if source_ip not in flow_dict:
                    flow_dict[source_ip] = {}
                if destination_ip not in flow_dict[source_ip]:
                    flow_dict[source_ip][destination_ip] = 0
                    # 增加计数
                flow_dict[source_ip][destination_ip] += 1

    end_time1 = time.time()

    # 计算并打印执行时间
    execution_time = end_time1 - start_time
    filename = f"{filename}.json"
    filepath=os.path.join("processed_data",filename)
    print(f"构建<f,e>字典执行时间: {execution_time:.2f} 秒")
    with open(filepath, "w") as f:
        json.dump(flow_dict, f, indent=4)

    print(f"筛选后的字典已保存到{file_path}.json")
    return flow_dict


def load_json(json_path):
    with open(json_path, "r", encoding="utf-8") as file:
        original_data = json.load(file)
    return original_data


def get_abnormal_data(data, card, freq,output):
    """

    :param output: 输出文件名
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
    filename = f"{output}.json"
    filepath = os.path.join("processed_data", filename)
    with open(filepath, "w") as f:
        json.dump(filtered_flows, f, indent=4)

    print(f"筛选后的字典已保存到{output}.json")


def extract_ips(input_pcap, output_txt):
    """

    :param input_pcap:
    :param output_txt:
    :return:
    """
    with open(output_txt, 'w') as f:
        with PcapReader(input_pcap) as pcap_reader:
            for pkt in pcap_reader:
                if pkt.haslayer(IP):
                    ip_layer = pkt[IP]
                    f.write(f"{ip_layer.src} {ip_layer.dst}\n")


def merge_univ_parts(output_file='IMCdata\\merged_univ1.txt', encoding='utf-8'):
    # 生成有序文件名列表
    file_list = [f"IMCdata\\univ1_pt{i}.txt" for i in range(1, 12)]

    # 验证所有文件存在
    missing_files = [f for f in file_list if not os.path.exists(f)]
    if missing_files:
        raise FileNotFoundError(f"缺失文件：{', '.join(missing_files)}")

    with open(output_file, 'w', encoding=encoding) as outfile:
        for filename in file_list:
            try:
                with open(filename, 'r', encoding=encoding) as infile:

                    # 直接复制文件内容（比逐行读取更快）
                    outfile.write(infile.read())

            except UnicodeDecodeError as e:
                print(f"编码错误跳过文件：{filename} ({str(e)})")
                continue
            except Exception as e:
                print(f"处理文件 {filename} 时发生错误：{str(e)}")
                raise

if __name__ == "__main__":

    #all_data_dict = data_analyze(data_num=10000000, file_path="datasets\stackoverflow\sx-stackoverflow-a2q.txt",filename="stackoverflow_dict")
    ab_data_dict=load_json("processed_data\\IMC_ab_flow.json")
    all_data_dict = load_json("processed_data\\IMC_dict.json")
    #get_abnormal_data(all_data_dict,5000,10000,"stackoverflow_ab_flow")
    print(len(ab_data_dict))

    print(len(all_data_dict))
