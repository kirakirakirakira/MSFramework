import random

from collections import Counter
import sys


from matplotlib import pyplot as plt
import time
import json

def random_pick_ips(counter, n):
    # 获取所有IP地址
    ip_list = [key for key, val in counter]
    # 从中随机挑选n个，不放回
    return random.sample(ip_list, min(n, len(ip_list)))



test_ip=['113.90.31.202', '171.252.197.65', '55.20.57.32', '137.214.79.231', '52.96.189.153', '55.2.13.98', '35.83.41.117', '23.134.2.147', '34.211.34.23', '217.63.235.217', '178.42.92.44', '52.106.146.126', '145.103.117.168', '16.25.141.189', '2a43:10fe:fff:7e0f::', '169.250.123.156', '169.221.13.169', '25.111.119.19', '221.175.73.177', '211.238.194.69', '84.115.157.113', '61.57.118.74', '212.21.71.233', '197.110.15.113', '45.125.179.205', '154.130.175.60', '157.44.47.131', '171.144.38.94', '45.169.196.51', '119.101.67.61', '85.216.139.79', '163.126.44.37', '77.127.122.175', '186.57.117.95', '170.229.255.204', '172.16.129.30', '195.92.23.114', '119.234.184.213', '178.49.243.140', '63.141.94.31', '195.219.108.120', '161.212.152.126', '55.37.205.144', '35.8.94.156', '218.183.129.45', '51.140.45.72', '66.132.107.199', '30.220.161.78', '6.110.25.138', '79.88.142.83', '192.54.198.195', '93.105.24.112', '119.237.89.205', '212.72.41.111', '190.202.145.204', '66.83.4.55', '79.67.90.103', '182.255.68.24', '75.9.17.110', '50.252.104.156', '93.173.255.141', '80.234.142.140', '203.108.170.30', '169.25.181.155', '26.120.96.103', '205.177.45.220', '42.27.129.60', '199.202.6.106', '66.132.244.247', '189.57.38.108', '128.55.247.145', '79.66.101.100', '84.240.63.79', '30.96.133.130', '146.55.120.10', '34.246.205.66', '114.193.26.194', '37.9.21.162', '126.247.192.154', '88.240.197.34', '195.159.148.9', '86.84.76.156', '164.249.120.231', '169.57.239.103', '198.193.71.129', '77.133.208.164', '52.193.172.76', '2.231.98.181', '169.250.86.90', '119.230.231.229', '71.255.89.219', '195.26.122.26', '52.219.64.46', '190.202.145.246', '119.6.26.118', '172.31.16.120', '173.180.168.60', '181.184.95.139', '210.75.61.108', '55.15.75.141']
test_pair = {ip: [] for ip in test_ip}
# 记录开始时间
start_time = time.time()
# 文件路径
file_path = ["../data1/02.txt","../data1/00.txt","../data1/01.txt","../data1/03.txt","../data1/04.txt"]

# 用于存储源 IP 地址的计数器
source_ip_count = Counter()

for path in file_path:
# 逐行读取文件并统计源 IP 地址
    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            # 去掉行尾换行符，并按空格分割
            parts = line.strip().split()
            if len(parts) == 2:  # 确保格式正确
                source_ip = parts[0]  # 第一个部分是源 IP 地址
                source_ip_count[source_ip] += 1
                if source_ip in test_pair:
                    test_pair[source_ip].append(parts[1])

end_time1 = time.time()

# 计算并打印执行时间
execution_time = end_time1 - start_time
print(f"统计部分代码执行时间: {execution_time:.2f} 秒")



sorted_ip_count = sorted(source_ip_count.items(), key=lambda x: x[1], reverse=True)

# 打印统计结果
print("源 IP 地址出现的次数（降序）：")
for ip, count in sorted_ip_count[:10:]:
    print(f"{ip}: {count}")

print("不同源ip个数：%d"%len(sorted_ip_count))
ct=[count for _, count in sorted_ip_count]
print("数据包数：%d"%sum(ct))

end_time = time.time()

# 计算并打印执行时间
execution_time = end_time - start_time
print(f"代码执行时间: {execution_time:.2f} 秒")


# 测试代码
final_test_ip={}
if __name__ == "__main__":
    for i in range(100):
        if len(set(test_pair[test_ip[i]]))>1:
            final_test_ip[test_ip[i]]=test_pair[test_ip[i]]

    with open("abnormal_data.json", "w", encoding="utf-8") as file:
        json.dump(final_test_ip, file)



