import math
import time
from CMSketch import CountMinSketch
from simiSketch import jaccard_est_of_simiSketch_CM
from static_data import StaticData


class Bucket:
    def __init__(self, fp=None, width=10, height=10):
        self.col = width
        self.row = height
        self.fp = fp
        self.feature_vector = CountMinSketch(width, height)
        self.similarity_score = 0
        self.timestamp=time.time()

    def update(self, alpha,packet):
        self.feature_vector.add(packet[1])
        self.timestamp = time.time()

    def query_S(self,alpha):
        T_now = time.time()
        quantity = math.exp(-alpha * (T_now - self.timestamp))
        return quantity*self.similarity_score

class BucketArray:
    def __init__(self, sizeA, sizeB, col=10, row=10):
        self.col = col
        self.row = row
        #main buckets array and alter buckets array
        self.buckets_array = [[None] * sizeA, [None] * sizeB]
        self.alpha = 0.01  #to be defined
        self.t_window = 1000  #time window for measurement
        self.t_entry = time.time()  #start time static
        self.scan_times = 1
        self.abnormal_data_for_filter2 = StaticData(CM_col=self.col, CM_row=self.row).data_for_filter2
        self.threshold = 0.3

    def find_insert_index(self, fp):
        empty_index0, empty_index1 = None, None
        for i, (bucket0, bucket1) in enumerate(zip(self.buckets_array[0], self.buckets_array[1])):
            if bucket0 is not None:
                if bucket0.fp == fp:
                    return [0, i]
            elif empty_index0 is None:
                empty_index0 = i

            if bucket1 is not None:
                if bucket1.fp == fp:
                    return [1, i]
            elif empty_index1 is None:
                empty_index1 = i

        return [0, empty_index0] if empty_index0 is not None else (
            [1, empty_index1] if empty_index1 is not None else None)

    def insert(self, packet: list[str]):
        index = self.find_insert_index(packet[0])
        if index is None:
            self.replace_least_S(packet)
            return
        if self.buckets_array[index[0]][index[1]] is None:
            self.buckets_array[index[0]][index[1]] = Bucket(packet[0], self.col, self.row)
            self.buckets_array[index[0]][index[1]].update(self.alpha,packet)

        else:
            self.buckets_array[index[0]][index[1]].update(self.alpha,packet)
        return

    def replace_least_S(self, packet:list[str]):
        min_S_index = min(
            range(len(self.buckets_array[1])),
            key=lambda i: self.buckets_array[1][i].query_S(self.alpha) if self.buckets_array[1][i] is not None else float('inf')
        )
        self.buckets_array[1][min_S_index] = Bucket(packet[0], self.col, self.row)
        self.buckets_array[1][min_S_index].update(self.alpha,packet)

    def find_and_swap(self,alltimes):
        final_list=set()
        if self.scan_times == 0:
            #first calculate similarity
            for j in range(len(self.buckets_array[0])):
                if self.buckets_array[0][j]:
                    maxsimi=0
                    for cms in self.abnormal_data_for_filter2:
                        temp=jaccard_est_of_simiSketch_CM(self.buckets_array[0][j].feature_vector,cms)
                        if temp>maxsimi:
                            maxsimi=temp
                    self.buckets_array[0][j].similarity_score=maxsimi
                    if self.buckets_array[0][j].similarity_score>self.threshold:
                        final_list.add(self.buckets_array[0][j].fp)
                        self.buckets_array[0][j] = None


            for j in range(len(self.buckets_array[1])):
                if self.buckets_array[1][j]:
                    maxsimi=0
                    for cms in self.abnormal_data_for_filter2:
                        temp=jaccard_est_of_simiSketch_CM(self.buckets_array[1][j].feature_vector,cms)
                        if temp>maxsimi:
                            maxsimi=temp
                    self.buckets_array[1][j].similarity_score=maxsimi

            # Find the bucket with the smallest S in self.buckets_array[0]
            min_S_index_A = None
            min_S_value = float('inf')
            for i, bucket in enumerate(self.buckets_array[0]):
                if bucket is not None and bucket.query_S(self.alpha) < min_S_value:
                    min_S_index_A = i
                    min_S_value = bucket.query_S(self.alpha)

            # Find the bucket with the largest S in self.buckets_array[1]
            max_S_index_B = None
            max_S_value = float('-inf')
            for i, bucket in enumerate(self.buckets_array[1]):
                if bucket is not None and bucket.query_S(self.alpha) > max_S_value:
                    max_S_index_B = i
                    max_S_value = bucket.query_S(self.alpha)
            if min_S_index_A is not None and max_S_index_B is not None and max_S_value > min_S_value:
                self.buckets_array[0][min_S_index_A], self.buckets_array[1][max_S_index_B] = (
                    self.buckets_array[1][max_S_index_B],
                    self.buckets_array[0][min_S_index_A],
                )
            else:
                print("No valid buckets to swap or swap condition not met.")

        self.scan_times=(1+self.scan_times)%alltimes
        return final_list

    def display(self):
        print("main buckets:")
        for i, item in enumerate(self.buckets_array[0]):
            print("No.%d: " % i, end=" ")
            if item is None:
                print("None")
            else:
                print("flow id:%s, similarity score:%.2f, S:%.2f" % (item.fp, item.similarity_score, item.query_S(self.alpha)))
                #item.feature_vector.display()

        print("alter buckets:")
        for i, item in enumerate(self.buckets_array[1]):
            print("No.%d: " % i, end=" ")
            if item is None:
                print("None")
            else:
                print("flow id:%s, similarity score:%.2f, S:%.2f" % (item.fp, item.similarity_score, item.query_S(self.alpha)))
            #item.feature_vector.display()



if __name__ == "__main__":
    bucketArray = BucketArray(10, 4, col=10, row=100)
    ct=0
    file_path = ["../data1/02.txt", "../data1/00.txt", "../data1/01.txt", "../data1/03.txt", "../data1/04.txt"]
    starttime = time.time()
    for path in file_path[:1]:
        # 逐行读取文件并统计源 IP 地址
        with open(path, "r", encoding="utf-8") as file:
            for line in file:
                # 去掉行尾换行符，并按空格分割
                parts = line.strip().split()
                if len(parts) == 2:  # 确保格式正确
                    bucketArray.insert(parts)
                    bucketArray.find_and_swap(100000)


    endtime = time.time()
    print("%.2f s" % (endtime - starttime))
    bucketArray.display()
