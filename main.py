# combine filter 1 and filter 2
import json
import time
import pandas as pd
from filter_1 import Filter1
from filter_1_with_buckets import Filter1 as Filter1_with_buckets
from filter_2 import BucketArray, Bucket
from mathtest import precision_recall_f1_calculate

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
            elif parts[0] in abnormal_flow_id_from_filter1:
                bucketArray.insert(parts)
                final_abnormal_flow_id = (final_abnormal_flow_id | bucketArray.find_and_swap(2000))
            else:
                filter1.update(parts)
                scan_result=filter1.scan(2000)
                if scan_result is not None:
                    abnormal_flow_id_from_filter1 = (set(scan_result[0]) | abnormal_flow_id_from_filter1)
                    for k in range(len(scan_result[0])):
                        index =bucketArray.find_insert_index(scan_result[0][k])
                        if index is None:
                            minS=bucketArray.find_least_S()
                            bucketArray.buckets_array[1][minS]=Bucket(scan_result[0][k], bucketArray.col, bucketArray.row)
                            for i in range(bucketArray.row):
                                if i==0:
                                    bucketArray.buckets_array[1][minS].feature_vector.table[i]=scan_result[1][k]
                                else:
                                    bucketArray.buckets_array[1][minS].feature_vector.table[i]=[0 for _ in range(bucketArray.col)]

                        elif bucketArray.buckets_array[index[0]][index[1]] is None:
                            bucketArray.buckets_array[index[0]][index[1]] = Bucket(scan_result[0][k], bucketArray.col, bucketArray.row)
                            for i in range(bucketArray.row):
                                if i==0:
                                    bucketArray.buckets_array[index[0]][index[1]].feature_vector.table[i]=scan_result[1][k]
                                else:
                                    bucketArray.buckets_array[index[0]][index[1]].feature_vector.table[i]=[0 for _ in range(bucketArray.col)]



            ct+=1
            if ct%100000==0:
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
full_insert_time=filter1.filter1_insert_time+bucketArray.filter2_insert_time
print("总插入用时:%.2f sec(%d min) "%(full_insert_time,full_insert_time//60))
# filter1.display()
# bucketArray.display()
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
precision,recall,f1=precision_recall_f1_calculate(ground_truth,detected)[1],precision_recall_f1_calculate(ground_truth,detected)[0],precision_recall_f1_calculate(ground_truth,detected)[2]

data={
    "packet_size":10000000,
    'filter1_d': filter1.rows,
    'filter1_w': filter1.cols,
    'filter1_ct': 8,
    'flow_id_size': 32,
    'simi_size': 4,
    'timestamp_size': 10,
    'filter2_main_num': len(bucketArray.buckets_array[0]),
    'filter2_alter_num': len(bucketArray.buckets_array[1]),
    'cm_depth': bucketArray.row,
    'cm_width': bucketArray.col,
    'cm_ct': 16,
    'precision':round(precision,4),
    'recall':round(recall,4),
    'f1-score':round(f1,4),
    'insert-time':round(full_insert_time,2),
    'space(KB)':int((filter1.rows*filter1.cols*8+filter1.rows*32+filter1.rows*4
                +(len(bucketArray.buckets_array[0])+len(bucketArray.buckets_array[1]))*((bucketArray.row*bucketArray.col*16)+
                                                                                        (32+4+10)))/8//1024),
    'filter1_threshold':filter1.threshold,
    'filter2_threshold':bucketArray.threshold
    }
df = pd.DataFrame([data])
df.to_csv('experiment_result.csv',mode='a', header=False, index=False)