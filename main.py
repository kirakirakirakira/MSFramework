# combine filter 1 and filter 2
import json
import os
import time
import pandas as pd
from filter_part_1.filter_1 import Filter1
from filter_part_1.filter_1_with_buckets import Filter1 as ft1
from filter_part_2.filter_2 import BucketArray, Bucket
from mathtest import precision_recall_f1_calculate
from filter_part_2.filter_2_maxlog import BucketArray as Bucket_Array_Maxlog
from filter_part_2.filter_2_minHash import BucketArray as Bucket_Array_minhash
from filter_part_2.filter_2_with_cells import BucketArray as Bucket_Array_with_cells
from static_data import StaticData
from write_in_data import write_in_data

def main_process(filter_1, filter2, filter1_scan_time=5000, filter2_scan_time=5000,file_path="../data1/02.txt"):
    start_time = time.time()
    abnormal_flow_id_from_filter1 = set()
    final_abnormal_flow_ids = set()
    start_read_time = time.time()
        # 一次性读取文件内容到内存
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
        #lines = file.readlines()[:10000000]# 将文件所有行读入列表
    print("file length:%d" % len(lines))
    end_read_time = time.time()
    read_time = end_read_time - start_read_time
    print("读取所有文件用时%.2f secs" % read_time)
    length = len(lines)
    ct = 0
    time1 = time.time()
    # 遍历读取的每一行
    for line in lines:
        # 去掉行尾换行符，并按空格分割
        parts = line.strip().split()
        if len(parts): #== 2:
            if parts[0] in final_abnormal_flow_ids:
                pass
            elif parts[0] in abnormal_flow_id_from_filter1:
                filter2.insert(parts)
                final_abnormal_flow_ids = (final_abnormal_flow_ids | filter2.find_and_swap(filter2_scan_time))
            else:
                filter_1.update(parts)
                scan_result = filter_1.scan(filter1_scan_time)
                if scan_result is not None:
                    abnormal_flow_id_from_filter1 = (set(scan_result[0]) | abnormal_flow_id_from_filter1)
                    filter2.first_update(scan_result)

            ct += 1
            if ct % 100000 == 0:
                temp_endtime = time.time()
                percent = ct / length
                print("%.2f complete. " % percent)
                print("%.2f sec. " % (temp_endtime - time1))

    end_time1 = time.time()
    execution_time = end_time1 - start_time
    print(f"代码执行时间: {execution_time:.2f} 秒")
    return final_abnormal_flow_ids



if __name__=="__main__":
    staticdata = StaticData(col=272,CM_col=272,CM_row=1,k_minhash=200)
    staticdata.update_data_for_filter1()
    staticdata.update_data_for_minhash()
    for k in range(2):
        for i in range(1,14,2):
            filter1 = ft1(i, 20, 272)
            filter1.staticdata=staticdata
            filter1.abnormal_data_for_filter1=staticdata.data_for_filter1
            #bucketArray = BucketArray(10,5, 272, 1,threshold=0.7)
            bucketArray=Bucket_Array_minhash(i*10, i*5,200,threshold=0.9)
            #bucketArray=Bucket_Array_Maxlog(i*10,i*5,k=128,threshold=0.9)
            bucketArray.staticdata=staticdata
            bucketArray.abnormal_data_for_minhash=staticdata.data_for_minhash
            final_abnormal_flow_id = main_process(filter1, bucketArray, 5000, 5000, file_path="datasets\\cicids17\\cicids17.txt")
            print("filter1 插入用时：%.2f sec(%d min)" % (filter1.filter1_insert_time, filter1.filter1_insert_time // 60))
            print("filter1 扫描用时：%.2f sec(%d min)" % (filter1.filter1_scan_time, filter1.filter1_scan_time // 60))
            print("bucketArray插入用时：%.2f sec(%d min)" % (bucketArray.filter2_insert_time, bucketArray.filter2_insert_time // 60))
            print("bucketArray扫描用时：%.2f sec(%d min)" % (bucketArray.filter2_scan_time, bucketArray.filter2_scan_time // 60))
            full_insert_time = filter1.filter1_insert_time + bucketArray.filter2_insert_time
            print("总插入用时:%.2f sec(%d min) " % (full_insert_time, full_insert_time // 60))

            abnormal_list = list(final_abnormal_flow_id)
            print("final_abnormal_flow_id:", end=" ")
            print(final_abnormal_flow_id)

            with open("processed_data/cicids2017_ab_flow.json", "r") as f:
                ground_truth = json.load(f).keys()

            detected = final_abnormal_flow_id
            print("true abnormal flow id " + str(ground_truth))
            # 读取实验检测出的异常流 IP 集合

            # 计算 Precision、Recall 和 F1
            temp=precision_recall_f1_calculate(ground_truth, detected)
            precision, recall, f1 = temp[0],temp[1],temp[2]
            print("precision:", precision, "recall:", recall, "f1:", f1)
            write_in_data(filter1,bucketArray,precision,recall,f1,full_insert_time,"processed_data/minhash_experiment_result_cicids17.csv")



    # for i in range(2,21,2):
    #     filter1 = ft1(i, 20, 272)
    #     #bucketArray = BucketArray(10*i, 5*i, 272, 1,threshold=0.5)
    #     #bucketArray=Bucket_Array_minhash(i*10, i*5,200,threshold=0.9)
    #     bucketArray=Bucket_Array_Maxlog(i*10,i*5,k=128,threshold=0.9)
    #     final_abnormal_flow_id = main_process(filter1, bucketArray, 5000, 5000, file_path="datasets\\stackoverflow\\sx-stackoverflow-a2q.txt")
    #     print("filter1 插入用时：%.2f sec(%d min)" % (filter1.filter1_insert_time, filter1.filter1_insert_time // 60))
    #     print("filter1 扫描用时：%.2f sec(%d min)" % (filter1.filter1_scan_time, filter1.filter1_scan_time // 60))
    #     print("bucketArray插入用时：%.2f sec(%d min)" % (bucketArray.filter2_insert_time, bucketArray.filter2_insert_time // 60))
    #     print("bucketArray扫描用时：%.2f sec(%d min)" % (bucketArray.filter2_scan_time, bucketArray.filter2_scan_time // 60))
    #     full_insert_time = filter1.filter1_insert_time + bucketArray.filter2_insert_time
    #     print("总插入用时:%.2f sec(%d min) " % (full_insert_time, full_insert_time // 60))
    #
    #     abnormal_list = list(final_abnormal_flow_id)
    #     print("final_abnormal_flow_id:", end=" ")
    #     print(final_abnormal_flow_id)
    #
    #     with open("processed_data/stackoverflow_ab_flow.json", "r") as f:
    #         ground_truth = json.load(f).keys()
    #
    #     detected = final_abnormal_flow_id
    #     print("true abnormal flow id " + str(ground_truth))
    #     # 读取实验检测出的异常流 IP 集合
    #
    #     # 计算 Precision、Recall 和 F1
    #     temp=precision_recall_f1_calculate(ground_truth, detected)
    #     precision, recall, f1 = temp[0],temp[1],temp[2]
    #     write_in_data(filter1,bucketArray)
    #
    # for i in range(1,13):
    #     filter1 = ft1(i, 20, 272)
    #     #bucketArray = BucketArray(10*i, 5*i, 272, 1,threshold=0.5)
    #     bucketArray=Bucket_Array_minhash(i*10, i*5,200,threshold=0.9)
    #     #bucketArray=Bucket_Array_Maxlog(i*10,i*5,k=128,threshold=0.9)
    #     final_abnormal_flow_id = main_process(filter1, bucketArray,5000,5000,file_path="datasets\\stackoverflow\\sx-stackoverflow-a2q.txt")
    #     print("filter1 插入用时：%.2f sec(%d min)" % (filter1.filter1_insert_time, filter1.filter1_insert_time // 60))
    #     print("filter1 扫描用时：%.2f sec(%d min)" % (filter1.filter1_scan_time, filter1.filter1_scan_time // 60))
    #     print("bucketArray插入用时：%.2f sec(%d min)" % (bucketArray.filter2_insert_time, bucketArray.filter2_insert_time // 60))
    #     print("bucketArray扫描用时：%.2f sec(%d min)" % (bucketArray.filter2_scan_time, bucketArray.filter2_scan_time // 60))
    #     full_insert_time = filter1.filter1_insert_time + bucketArray.filter2_insert_time
    #     print("总插入用时:%.2f sec(%d min) " % (full_insert_time, full_insert_time // 60))
    #
    #     abnormal_list = list(final_abnormal_flow_id)
    #     print("final_abnormal_flow_id:", end=" ")
    #     print(final_abnormal_flow_id)
    #
    #     with open("processed_data/stackoverflow_ab_flow.json", "r") as f:
    #         ground_truth = json.load(f).keys()
    #
    #     detected = final_abnormal_flow_id
    #     print("true abnormal flow id " + str(ground_truth))
    #     # 读取实验检测出的异常流 IP 集合
    #
    #     # 计算 Precision、Recall 和 F1
    #     temp=precision_recall_f1_calculate(ground_truth, detected)
    #     precision, recall, f1 = temp[0],temp[1],temp[2]
    #     write_in_data(filter1,bucketArray)