from collections import Counter
import sys
from matplotlib import pyplot as plt
import time

# 记录开始时间
start_time = time.time()
# 文件路径
file_path = "../data1/02.txt"
file_path2 = "../data1/00.txt"
file_path3 = "../data1/01.txt"
file_path4 = "../data1/03.txt"
file_path5 = "../data1/04.txt"
# 用于存储源 IP 地址的计数器
source_ip_count = Counter()

# 逐行读取文件并统计源 IP 地址
with open(file_path, "r", encoding="utf-8") as file:
    for line in file:
        # 去掉行尾换行符，并按空格分割
        parts = line.strip().split()
        if len(parts) == 2:  # 确保格式正确
            source_ip = parts[0]  # 第一个部分是源 IP 地址
            source_ip_count[source_ip] += 1

end_time1 = time.time()

# 计算并打印执行时间
execution_time = end_time1 - start_time
print(f"part1代码执行时间: {execution_time:.2f} 秒")

with open(file_path2, "r", encoding="utf-8") as file:
    for line in file:
        # 去掉行尾换行符，并按空格分割
        parts = line.strip().split()
        if len(parts) == 2:  # 确保格式正确
            source_ip = parts[0]  # 第一个部分是源 IP 地址
            source_ip_count[source_ip] += 1

end_time2 = time.time()

# 计算并打印执行时间
execution_time = end_time2 - end_time1
print(f"part2代码执行时间: {execution_time:.2f} 秒")

with open(file_path3, "r", encoding="utf-8") as file:
    for line in file:
        # 去掉行尾换行符，并按空格分割
        parts = line.strip().split()
        if len(parts) == 2:  # 确保格式正确
            source_ip = parts[0]  # 第一个部分是源 IP 地址
            source_ip_count[source_ip] += 1

with open(file_path4, "r", encoding="utf-8") as file:
    for line in file:
        # 去掉行尾换行符，并按空格分割
        parts = line.strip().split()
        if len(parts) == 2:  # 确保格式正确
            source_ip = parts[0]  # 第一个部分是源 IP 地址
            source_ip_count[source_ip] += 1

with open(file_path5, "r", encoding="utf-8") as file:
    for line in file:
        # 去掉行尾换行符，并按空格分割
        parts = line.strip().split()
        if len(parts) == 2:  # 确保格式正确
            source_ip = parts[0]  # 第一个部分是源 IP 地址
            source_ip_count[source_ip] += 1

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



# 计算 sorted_ip_count 本身占用的内存
sorted_ip_count_size = sys.getsizeof(sorted_ip_count)

# 计算 sorted_ip_count 中每个元素的内存占用
elements_size = sum(sys.getsizeof(item) for item in sorted_ip_count)

# 计算 sorted_ip_count 中每个元素内的内容（IP 地址和计数）的内存占用
content_size = sum(sys.getsizeof(ip) + sys.getsizeof(count) for ip, count in sorted_ip_count)

# 总内存大小
total_size = sorted_ip_count_size + elements_size + content_size

print(f"sorted_ip_count 本身占用的内存: {sorted_ip_count_size} 字节")
print(f"sorted_ip_count 中每个元素占用的内存: {elements_size} 字节")
print(f"sorted_ip_count 中内容占用的内存: {content_size} 字节")
print(f"sorted_ip_count 总共占用的内存: {total_size} 字节")


# 测试代码
if __name__ == "__main__":
    pass
