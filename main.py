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


def main_process(filter_1, filter2, filter1_scan_time=5000, filter2_scan_time=5000):
    start_time = time.time()
    abnormal_flow_id_from_filter1 = set()
    final_abnormal_flow_ids = set()
    file_path = ["../data1/02.txt", "../data1/00.txt", "../data1/01.txt", "../data1/03.txt", "../data1/04.txt"]
    start_read_time = time.time()
    for path in file_path[:1]:
        # 一次性读取文件内容到内存
        with open(path, "r", encoding="utf-8") as file:
            lines = file.readlines()[:10000000]  # 将文件所有行读入列表
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
            if len(parts) == 2:
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

def write_in_data(filter_1, filter_2):
    data={}
    if hasattr(filter_1,'rows'):
        data = {

            "packet_size": 10000000,
            "entry_size": filter_1.rows,
            'filter1_d': filter_1.rows,
            'filter1_w': filter_1.cols,
            'filter1_ct': 8,
            'flow_id_size': 32,
            'simi_size': 4,
            'timestamp_size': 10,
            'filter2_main_num': len(filter_2.buckets_array[0]),
            'filter2_alter_num': len(filter_2.buckets_array[1]),
            'cm_depth': filter_2.row,
            'cm_width': filter_2.col,
            'cm_ct': 16,
            'precision': round(precision, 4),
            'recall': round(recall, 4),
            'f1-score': round(f1, 4),
            'insert-time': round(full_insert_time, 2),
            'space(KB)': int((filter_1.rows * filter_1.cols * 8 + filter_1.rows * 32 + filter_1.rows *4
                              + (len(filter_2.buckets_array[0]) + len(filter_2.buckets_array[1])) * (
                                      (filter_2.row * filter_2.col * 16) +
                                      (32+ 4+ 10 ))) / 8 // 1024),
            'filter1_threshold': filter_1.threshold,
            'filter2_threshold': filter_2.threshold
        }
    elif hasattr(filter_1,'entries_per_bucket'):
        if hasattr(filter_2,'k'):
            filter_1_rows = filter_1.entries_per_bucket * filter_1.bucket_count
            data = {
                "packet_size": 10000000,
                "entry_size": filter_1.entries_per_bucket,
                'filter1_d': filter_1_rows,
                'filter1_w': filter_1.cols,
                'filter1_ct': 8,
                'flow_id_size': 32,
                'simi_size': 4,
                'timestamp_size': 10,
                'filter2_main_num': len(filter_2.buckets_array[0]),
                'filter2_alter_num': len(filter_2.buckets_array[1]),
                'k':filter_2.k,
                'precision': round(precision, 4),
                'recall': round(recall, 4),
                'f1-score': round(f1, 4),
                'insert-time': round(full_insert_time, 2),
                'space(KB)': int((filter_1_rows * filter_1.cols * 8 + filter_1_rows * 32 + filter_1_rows * 4
                                  + (len(filter_2.buckets_array[0]) + len(filter_2.buckets_array[1])) * (
                                          (filter_2.k* (6+1)) +
                                          (32 + 4 + 10))) / 8 // 1024),
                'filter1_threshold': filter_1.threshold,
                'filter2_threshold': filter_2.threshold
            }
            df = pd.DataFrame([data])
            #
            df.to_csv('processed_data/maxlog_experiment_result_new.csv', mode='a', header=False,index=False)
            return

        if hasattr(filter_2,'k_minhash'):
            filter_1_rows = filter_1.entries_per_bucket * filter_1.bucket_count
            data = {
                "packet_size": 10000000,
                "entry_size": filter_1.entries_per_bucket,
                'filter1_d': filter_1_rows,
                'filter1_w': filter_1.cols,
                'filter1_ct': 8,
                'flow_id_size': 32,
                'simi_size': 4,
                'timestamp_size': 10,
                'filter2_main_num': len(filter_2.buckets_array[0]),
                'filter2_alter_num': len(filter_2.buckets_array[1]),
                'k_minhash': filter_2.k_minhash,
                'precision': round(precision, 4),
                'recall': round(recall, 4),
                'f1-score': round(f1, 4),
                'insert-time': round(full_insert_time, 2),
                'space(KB)': int((filter_1_rows * filter_1.cols * 8 + filter_1_rows * 32 + filter_1_rows * 4
                                  + (len(filter_2.buckets_array[0]) + len(filter_2.buckets_array[1])) * (
                                          (filter_2.k_minhash * 16) +
                                          (32 + 4 + 10))) / 8 // 1024),
                'filter1_threshold': filter_1.threshold,
                'filter2_threshold': filter_2.threshold
            }
            df = pd.DataFrame([data])
            file_path='processed_data/minhash_experiment_result_new.csv'
            if os.path.exists(file_path):
                # 后续追加模式（无表头）
                df.to_csv(file_path, mode='a', header=False, index=False)
            else:
                # 初次写入模式（带表头）
                df.to_csv(file_path, mode='w', header=True, index=False)
            return
        else:
            filter_1_rows=filter_1.entries_per_bucket*filter_1.bucket_count
            data = {
                "packet_size": 10000000,
                "entry_size": filter_1.entries_per_bucket,
                'filter1_d': filter_1_rows,
                'filter1_w': filter_1.cols,
                'filter1_ct': 8,
                'flow_id_size': 32,
                'simi_size': 4,
                'timestamp_size': 10,
                'filter2_main_num': len(filter_2.buckets_array[0]),
                'filter2_alter_num': len(filter_2.buckets_array[1]),
                'cm_depth': filter_2.row,
                'cm_width': filter_2.col,
                'cm_ct': 16,
                'precision': round(precision, 4),
                'recall': round(recall, 4),
                'f1-score': round(f1, 4),
                'insert-time': round(full_insert_time, 2),
                'space(KB)': int((filter_1_rows * filter_1.cols * 8 + filter_1_rows * 32 + filter_1_rows * 4
                                  + (len(filter_2.buckets_array[0]) + len(filter_2.buckets_array[1])) * (
                                          (filter_2.row * filter_2.col * 16) +
                                          (32 + 4 + 10 ))) / 8 // 1024),
                'filter1_threshold': filter_1.threshold,
                'filter2_threshold': filter_2.threshold
            }


    df = pd.DataFrame([data])
    df.to_csv('processed_data/experiment_result.csv', mode='a', header=False, index=False)

if __name__=="__main__":
    for j in range(1,4):
        for i in range(1,11):
    #filter1 = Filter1(100, 272)
            filter1 = ft1(i, 20, 272)
            bucketArray = BucketArray(i*10, i*5, 272, j,threshold=0.5)
            #bucketArray=Bucket_Array_minhash(i*10, i*5,200,threshold=0.9)
            #bucketArray=Bucket_Array_Maxlog(i*10,i*5,k=128,threshold=0.9)
            final_abnormal_flow_id = main_process(filter1, bucketArray,2000,2000)
            print("filter1 插入用时：%.2f sec(%d min)" % (filter1.filter1_insert_time, filter1.filter1_insert_time // 60))
            print("filter1 扫描用时：%.2f sec(%d min)" % (filter1.filter1_scan_time, filter1.filter1_scan_time // 60))
            print("bucketArray插入用时：%.2f sec(%d min)" % (bucketArray.filter2_insert_time, bucketArray.filter2_insert_time // 60))
            print("bucketArray扫描用时：%.2f sec(%d min)" % (bucketArray.filter2_scan_time, bucketArray.filter2_scan_time // 60))
            full_insert_time = filter1.filter1_insert_time + bucketArray.filter2_insert_time
            print("总插入用时:%.2f sec(%d min) " % (full_insert_time, full_insert_time // 60))

            abnormal_list = list(final_abnormal_flow_id)
            print("final_abnormal_flow_id:", end=" ")
            print(final_abnormal_flow_id)

            with open("proces   sed_data/filtered_flows.json", "r") as f:
                ground_truth = json.load(f).keys()

            detected = final_abnormal_flow_id
            print("true abnormal flow id " + str(ground_truth))
            # 读取实验检测出的异常流 IP 集合

            # 计算 Precision、Recall 和 F1
            temp=precision_recall_f1_calculate(ground_truth, detected)
            precision, recall, f1 = temp[0],temp[1],temp[2]
            write_in_data(filter1,bucketArray)
