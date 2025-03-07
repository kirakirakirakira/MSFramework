# combine filter 1 and filter 2
import json
import time

from filter_1 import Filter1
from filter_2 import BucketArray, Bucket

start_time = time.time()
abnormal_flow_id_from_filter1=set()
final_abnormal_flow_id=set()


filter1=Filter1(100,272)
bucketArray=BucketArray(50,25,272,1)


file_path = ["../data1/02.txt","../data1/00.txt","../data1/01.txt","../data1/03.txt","../data1/04.txt"]
start_read_time=time.time()
for path in file_path[:1]:
    # 一次性读取文件内容到内存
    with open(path, "r", encoding="utf-8") as file:
        lines = file.readlines()[:10000000]  # 将文件所有行读入列表
    print("file length:%d"%len(lines))
    end_read_time = time.time()
    read_time=end_read_time-start_read_time
    print("读取所有文件用时%.2f secs" % read_time)
    length=len(lines)
    ct=0
    time1=time.time()
    # 遍历读取的每一行
    for line in lines:
        # 去掉行尾换行符，并按空格分割
        parts = line.strip().split()
        if len(parts) == 2:
            if parts[0] in final_abnormal_flow_id:
                pass
            elif parts[0] not in final_abnormal_flow_id and parts[0] not in abnormal_flow_id_from_filter1:
                filter1.update(parts)
                scan_result=filter1.scan(5000)
                if scan_result is not None:
                    abnormal_flow_id_from_filter1 = (set(scan_result[0]) | abnormal_flow_id_from_filter1)
                    for k in range(len(scan_result[0])):
                        index =bucketArray.find_insert_index(scan_result[0][k])
                        if index is None:
                            minS=bucketArray.find_least_S()
                            bucketArray.buckets_array[1][minS]=Bucket(scan_result[0][k], bucketArray.col, bucketArray.row)
                            for i in range(bucketArray.row):
                                bucketArray.buckets_array[1][minS].feature_vector.table[i]=scan_result[1][k]

                        elif bucketArray.buckets_array[index[0]][index[1]] is None:
                            bucketArray.buckets_array[index[0]][index[1]] = Bucket(scan_result[0][k], bucketArray.col, bucketArray.row)
                            for i in range(bucketArray.row):
                                bucketArray.buckets_array[index[0]][index[1]].feature_vector.table[i]=scan_result[1][k]


            elif parts[0] in abnormal_flow_id_from_filter1:
                bucketArray.insert(parts)
                final_abnormal_flow_id = (final_abnormal_flow_id | bucketArray.find_and_swap(5000))
            ct+=1
            if ct%1000==0:
                temp_endtime=time.time()
                percent=ct/length
                print("%.2f complete. "%percent)
                print("%.2f sec. " % (temp_endtime-time1))


end_time1 = time.time()
execution_time = end_time1 - start_time
print(f"代码执行时间: {execution_time:.2f} 秒")



print("filter1 插入用时：%.2f sec(%d min)"%(filter1.filter1_insert_time,filter1.filter1_insert_time//60))
print("filter1 扫描用时：%.2f sec(%d min)"%(filter1.filter1_scan_time,filter1.filter1_scan_time//60))
print("bucketArray插入用时：%.2f sec(%d min)"%(bucketArray.filter2_insert_time,bucketArray.filter2_insert_time//60))
print("bucketArray扫描用时：%.2f sec(%d min)"%(bucketArray.filter2_scan_time,bucketArray.filter2_scan_time//60))
filter1.display()
bucketArray.display()
#pr rr calculate
abnormal_list=list(final_abnormal_flow_id)
print("abnormal_flow_id_from_filter1:",end=" ")
print(abnormal_flow_id_from_filter1)
print("final_abnormal_flow_id:",end=" ")
print(final_abnormal_flow_id)



with open("filtered_flows.json", "r") as f:
    ground_truth = json.load(f).keys()

detected=final_abnormal_flow_id
print("true abnormal flow id "+str(ground_truth))
# 读取实验检测出的异常流 IP 集合

# 计算 Precision、Recall 和 F1
tp = len(ground_truth & detected)  # True Positives
fp = len(detected - ground_truth)  # False Positives
fn = len(ground_truth - detected)  # False Negatives

precision = tp / (tp + fp) if (tp + fp) > 0 else 0
recall = tp / (tp + fn) if (tp + fn) > 0 else 0
f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

print(f"Precision: {precision:.4f}")
print(f"Recall: {recall:.4f}")
print(f"F1 Score: {f1:.4f}")
