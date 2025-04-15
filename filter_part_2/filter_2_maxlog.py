import math
import time

from static_data import StaticData
from BasicFunctions.MaxLogHash import hash_parameter, MaxLog, estimate_maxlog_jaccard_similarity


class Bucket:
    def __init__(self, fp, k):
        self.k=k
        self.fp = fp
        self.feature_vector = MaxLog(k,k+2,hash_parameter(k,k),hash_parameter(k,k+1))
        self.similarity_score = 0
        self.timestamp=time.time()


    def update(self,packet):
        self.feature_vector.process_item(packet[1])
        self.timestamp = time.time()

    def query_S(self,alpha):
        T_now = time.time()
        quantity = math.exp(-alpha * (T_now - self.timestamp))
        return quantity*self.similarity_score

class BucketArray:
    def __init__(self, sizeA, sizeB,k,threshold=0.5,alpha=0.1):
        #main buckets array and alter buckets array
        self.k=k
        self.buckets_array = [[None] * sizeA, [None] * sizeB]
        self.alpha = alpha  #to be defined
        self.scan_times = 1
        self.staticdata= StaticData(k=self.k)
        #self.staticdata.update_data_for_maxlog()
        self.abnormal_data_for_maxlog=self.staticdata.data_for_maxlog
        self.threshold = threshold
        #记录总扫描时间
        self.filter2_scan_time=0
        # 记录总插入时间
        self.filter2_insert_time = 0

    def find_insert_index(self, fp):
        empty_index0, empty_index1 = None, None
        for i in range(len(self.buckets_array[0])):
            if self.buckets_array[0][i] is not None:
                if self.buckets_array[0][i].fp == fp:
                    return [0, i]
            elif empty_index0 is None:
                empty_index0 = i

        # **只有当 buckets_array[0] 完全满时，才考虑 buckets_array[1]**
        if empty_index0 is not None:
            return [0, empty_index0]

        for i in range(len(self.buckets_array[1])):
            if self.buckets_array[1][i] is not None:
                if self.buckets_array[1][i].fp == fp:
                    return [1, i]
            elif empty_index1 is None:
                empty_index1 = i

        return [1, empty_index1] if empty_index1 is not None else None

    def insert(self, packet: list[str]):
        starttime = time.time()
        index = self.find_insert_index(packet[0])
        if index is None:
            self.replace_least_S(packet)
            return
        if self.buckets_array[index[0]][index[1]] is None:
            self.buckets_array[index[0]][index[1]] = Bucket(packet[0], self.k)
            self.buckets_array[index[0]][index[1]].update(packet)

        else:
            self.buckets_array[index[0]][index[1]].update(packet)
        endtime=time.time()
        exetime = endtime - starttime
        self.filter2_insert_time+=exetime
        #print("本次bucket array插入用时%.2f" % exetime)
        return

    def first_update(self,scan_result):
        for k in range(len(scan_result[0])):
            index = self.find_insert_index(scan_result[0][k])
            if index is None:
                minS = self.find_least_S()
                self.buckets_array[1][minS] = Bucket(scan_result[0][k], self.k)
            elif self.buckets_array[index[0]][index[1]] is None:
                self.buckets_array[index[0]][index[1]] = Bucket(scan_result[0][k], self.k)
        return


    def find_least_S(self):
        min_S_index = min(
            range(len(self.buckets_array[1])),
            key=lambda i: self.buckets_array[1][i].query_S(self.alpha) if self.buckets_array[1][i] is not None else float('inf')
        )
        return min_S_index
    def replace_least_S(self, packet:list[str]):
        min_S_index = self.find_least_S()
        self.buckets_array[1][min_S_index] = Bucket(packet[0], self.k)
        self.buckets_array[1][min_S_index].update(packet)

    def find_and_swap(self,alltimes):
        total_size_A = len(self.buckets_array[0])
        total_size_B = len(self.buckets_array[1])
        final_list=set()
        if self.scan_times == 0:

            starttime = time.time()
            # **确定扫描范围**
            # scan_range_A = range(self.scan_offsetA, min(self.scan_offsetA + self.scan_stepA, total_size_A))
            # scan_range_B = range(self.scan_offsetB, min(self.scan_offsetB + self.scan_stepB, total_size_B))


            #first calculate similarity
            min_S_index_A, min_S_value = None, float('inf')
            for j in range(total_size_A):
                bucket = self.buckets_array[0][j]
                if bucket:

                    maxsimi = max(estimate_maxlog_jaccard_similarity(bucket.feature_vector, mxl,self.k)
                                  for mxl in self.abnormal_data_for_maxlog)

                    bucket.similarity_score = maxsimi

                    if bucket.similarity_score > self.threshold:
                        final_list.add(bucket.fp)
                        self.buckets_array[0][j] = None
                    else:
                        S_value = bucket.query_S(self.alpha)
                        if S_value < min_S_value:
                            min_S_index_A, min_S_value = j, S_value

            # **遍历备用存 buckets_array[1]**
            max_S_index_B, max_S_value = None, float('-inf')
            for j in range(total_size_B):
                bucket = self.buckets_array[1][j]
                if bucket:
                    maxsimi = max(estimate_maxlog_jaccard_similarity(bucket.feature_vector, mxl,self.k)
                                  for mxl in self.abnormal_data_for_maxlog)
                    bucket.similarity_score = maxsimi

                    S_value = bucket.query_S(self.alpha)
                    if S_value > max_S_value:
                        max_S_index_B, max_S_value = j, S_value

            # **执行交换**
            if min_S_index_A is not None and max_S_index_B is not None and max_S_value > min_S_value:
                self.buckets_array[0][min_S_index_A], self.buckets_array[1][max_S_index_B] = (
                    self.buckets_array[1][max_S_index_B],
                    self.buckets_array[0][min_S_index_A],
                )

            endtime = time.time()
            self.filter2_scan_time += (endtime - starttime)

        self.scan_times = (self.scan_times + 1) % alltimes
        return final_list

if __name__ == "__main__":
    pass