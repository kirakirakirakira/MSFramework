# combine filter 1 and filter 2
import time

from filter_1 import Filter1
from filter_2 import BucketArray

abnormal_flow_id_from_filter1=set()
final_abnormal_flow_id=set()


filter1=Filter1(100,150)
bucketArray=BucketArray(100,50,1000,100)
start_time = time.time()

file_path = ["../data1/02.txt","../data1/00.txt","../data1/01.txt","../data1/03.txt","../data1/04.txt"]

for path in file_path[:1]:
# 逐行读取文件并统计源 IP 地址
    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            # 去掉行尾换行符，并按空格分割
            parts = line.strip().split()
            if len(parts) == 2:
                if parts[0] in final_abnormal_flow_id:
                    pass
                elif parts[0] not in final_abnormal_flow_id and parts[0] not in abnormal_flow_id_from_filter1:
                    filter1.update(parts)
                    abnormal_flow_id_from_filter1=(filter1.scan(10000)|abnormal_flow_id_from_filter1)
                elif parts[0] in final_abnormal_flow_id:
                    bucketArray.insert(parts)
                    final_abnormal_flow_id=(final_abnormal_flow_id|bucketArray.find_and_swap(10000))

end_time1 = time.time()
execution_time = end_time1 - start_time
print(f"代码执行时间: {execution_time:.2f} 秒")
print(abnormal_flow_id_from_filter1)
print(final_abnormal_flow_id)