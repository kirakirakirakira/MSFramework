import os
import pandas as pd

def write_in_data(filter_1, filter_2,precision,recall,f1,full_insert_time,file_path):
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
            file_path=file_path
            if os.path.exists(file_path):
                # 后续追加模式（无表头）
                df.to_csv(file_path, mode='a', header=False, index=False)
            else:
                # 初次写入模式（带表头）
                df.to_csv(file_path, mode='w', header=True, index=False)
            return

        elif hasattr(filter_2,'k_minhash'):
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
            file_path=file_path
            if os.path.exists(file_path):
                # 后续追加模式（无表头）
                df.to_csv(file_path, mode='a', header=False, index=False)
            else:
                # 初次写入模式（带表头）
                df.to_csv(file_path, mode='w', header=True, index=False)
            return

        elif hasattr(filter_2,'cell_per_bucket'):
            filter_1_rows = filter_1.entries_per_bucket * filter_1.bucket_count
            data = {
                "packet_size": 10000000,
                "entry_size": filter_1.entries_per_bucket,
                'filter1_d': filter_1_rows,
                'filter1_w': filter_1.cols,
                'filter1_ct': 8,
                'flow_id_size': 32,
                'simi_size': 32,
                'timestamp_size': 32,
                'filter2_main_num': filter_2.size*filter_2.cell_per_bucket,
                'filter2_alter_num': 0,
                'cm_depth': filter_2.row,
                'cm_width': filter_2.col,
                'cm_ct': 16,
                'precision': round(precision, 4),
                'recall': round(recall, 4),
                'f1-score': round(f1, 4),
                'insert-time': round(full_insert_time, 2),
                'space(KB)': int((filter_1_rows * filter_1.cols * 8 + filter_1_rows * (32 +32)
                                  + filter_2.size*filter_2.cell_per_bucket * (
                                          (filter_2.row * filter_2.col * 16) +
                                          (32 + 32 + 32))) / 8 // 1024),
                'filter1_threshold': filter_1.threshold,
                'filter2_threshold': filter_2.threshold
            }
            df = pd.DataFrame([data])
            file_path=file_path
            if os.path.exists(file_path):
                # 后续追加模式（无表头）
                df.to_csv(file_path, mode='a', header=False, index=False)
            else:
                # 初次写入模式（带表头）
                df.to_csv(file_path, mode='w', header=True, index=False)
        else:
            filter_1_rows=filter_1.entries_per_bucket*filter_1.bucket_count
            data = {
                "packet_size": 10000000,
                "entry_size": filter_1.entries_per_bucket,
                'filter1_d': filter_1_rows,
                'filter1_w': filter_1.cols,
                'filter1_ct': 8,
                'flow_id_size': 32,
                'simi_size': 32,
                'timestamp_size': 32,
                'filter2_main_num': len(filter_2.buckets_array[0]),
                'filter2_alter_num': len(filter_2.buckets_array[1]),
                'cm_depth': filter_2.row,
                'cm_width': filter_2.col,
                'cm_ct': 16,
                'precision': round(precision, 4),
                'recall': round(recall, 4),
                'f1-score': round(f1, 4),
                'insert-time': round(full_insert_time, 2),
                'space(KB)': int((filter_1_rows * filter_1.cols * 8 + filter_1_rows * 32 + filter_1_rows * 32
                                  + (len(filter_2.buckets_array[0]) + len(filter_2.buckets_array[1])) * (
                                          (filter_2.row * filter_2.col * 16) +
                                          (32 + 32 + 32 ))) / 8 // 1024),
                'filter1_threshold': filter_1.threshold,
                'filter2_threshold': filter_2.threshold
            }


            df = pd.DataFrame([data])
            file_path=file_path
            if os.path.exists(file_path):
                # 后续追加模式（无表头）
                df.to_csv(file_path, mode='a', header=False, index=False)
            else:
                # 初次写入模式（带表头）
                df.to_csv(file_path, mode='w', header=True, index=False)