# combine filter 1 and filter 2
import time

from filter_1 import Filter1
from filter_2 import BucketArray

abnormal_flow_id_from_filter1=set()
final_abnormal_flow_id=set()


filter1=Filter1(100,150)
bucketArray=BucketArray(100,500,200,100)
start_time = time.time()

file_path = ["../data1/02.txt","../data1/00.txt","../data1/01.txt","../data1/03.txt","../data1/04.txt"]

for path in file_path[:1]:
    # 一次性读取文件内容到内存
    with open(path, "r", encoding="utf-8") as file:
        lines = file.readlines()  # 将文件所有行读入列表

    # 遍历读取的每一行
    for line in lines:
        # 去掉行尾换行符，并按空格分割
        parts = line.strip().split()
        if len(parts) == 2:
            if parts[0] in final_abnormal_flow_id:
                pass
            elif parts[0] not in final_abnormal_flow_id and parts[0] not in abnormal_flow_id_from_filter1:
                filter1.update(parts)
                abnormal_flow_id_from_filter1 = (filter1.scan(10000) | abnormal_flow_id_from_filter1)
            elif parts[0] in final_abnormal_flow_id:
                bucketArray.insert(parts)
                final_abnormal_flow_id = (final_abnormal_flow_id | bucketArray.find_and_swap(10000))

end_time1 = time.time()
execution_time = end_time1 - start_time
print(f"代码执行时间: {execution_time:.2f} 秒")
print("abnormal_flow_id_from_filter1:",end=" ")
print(abnormal_flow_id_from_filter1)
print("final_abnormal_flow_id:",end=" ")
print(final_abnormal_flow_id)


#pr rr calculate
abnormal_list=list(abnormal_flow_id_from_filter1)
true_abnormal=filter1.abnormal_flow_ids
tp = len(set(abnormal_list) & set(true_abnormal))
fp = len(set(abnormal_list) - set(true_abnormal))
fn = len(set(true_abnormal) - set(abnormal_list))

# 计算准确率和召回率
precision = tp / (tp + fp) if (tp + fp) > 0 else 0
recall = tp / (tp + fn) if (tp + fn) > 0 else 0

print(f"准确率 (Precision): {precision:.2f}")
print(f"召回率 (Recall): {recall:.2f}")
