import math
import time
from CMSketch import CountMinSketch
from simiSketch import jaccard_est_of_simiSketch_CM
from static_data import StaticData


class Bucket:
    def __init__(self, fp, width, height):
        self.col = width
        self.row = height
        self.fp = fp
        self.feature_vector = CountMinSketch(width, height)
        self.similarity_score = 0
        self.timestamp=time.time()


    def update(self,packet):
        self.feature_vector.add(packet[1])
        self.timestamp = time.time()

    def query_S(self,alpha):
        T_now = time.time()
        quantity = math.exp(-alpha * (T_now - self.timestamp))
        return quantity*self.similarity_score

class BucketArray:
    def __init__(self, sizeA, sizeB, col=272, row=1,threshold=0.4,alpha=0.1):
        self.col = col
        self.row = row
        #main buckets array and alter buckets array
        self.buckets_array = [[None] * sizeA, [None] * sizeB]
        self.alpha = alpha  #to be defined
        self.scan_times = 1
        self.staticdata= StaticData(CM_col=self.col, CM_row=self.row)
        self.staticdata.update_data_for_filter2()
        self.abnormal_data_for_filter2 = self.staticdata.data_for_filter2
        self.threshold = threshold
        #记录总扫描时间
        self.filter2_scan_time=0
        # 记录总插入时间
        self.filter2_insert_time = 0

    def find_insert_index(self, fp):
        # 检查所有桶中是否存在相同 fp
        for array_idx in [0, 1]:
            for i in range(len(self.buckets_array[array_idx])):
                if self.buckets_array[array_idx][i] and self.buckets_array[array_idx][i].fp == fp:
                    return [array_idx, i]
        # 寻找主桶空位
        for i in range(len(self.buckets_array[0])):
            if self.buckets_array[0][i] is None:
                return [0, i]
        # 主桶满，寻找备用桶空位
        for i in range(len(self.buckets_array[1])):
            if self.buckets_array[1][i] is None:
                return [1, i]
        return None

    def insert(self, packet: list[str]):
        starttime = time.time()
        index = self.find_insert_index(packet[0])
        if index is None:
            self.replace_least_S(packet)
            return
        if self.buckets_array[index[0]][index[1]] is None:
            self.buckets_array[index[0]][index[1]] = Bucket(packet[0], self.col, self.row)
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
                self.buckets_array[1][minS] = Bucket(scan_result[0][k], self.col, self.row)
                if self.row==1:
                    self.buckets_array[1][minS].feature_vector.table[0] = [
                        max(x, 0) for x in scan_result[1][k]
                    ]
                else:
                    for i in range(self.row):
                        self.buckets_array[1][minS].feature_vector.table[i] = [0 for _ in
                                                                                  range(self.col)]

            elif self.buckets_array[index[0]][index[1]] is None:
                self.buckets_array[index[0]][index[1]] = Bucket(scan_result[0][k], self.col,
                                                                   self.row)
                if self.row == 1:
                    self.buckets_array[index[0]][index[1]].feature_vector.table[0] = [
                        max(x, 0) for x in scan_result[1][k]
                    ]
                else:
                    for i in range(self.row):
                        self.buckets_array[index[0]][index[1]].feature_vector.table[i] = [0 for _ in
                                                                               range(self.col)]
        return


    def find_least_S(self):
        min_S_index = min(
            range(len(self.buckets_array[1])),
            key=lambda i: self.buckets_array[1][i].query_S(self.alpha) if self.buckets_array[1][i] is not None else float('inf')
        )
        return min_S_index
    def replace_least_S(self, packet:list[str]):
        min_S_index = self.find_least_S()
        self.buckets_array[1][min_S_index] = Bucket(packet[0], self.col, self.row)
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

                    maxsimi = max(jaccard_est_of_simiSketch_CM(bucket.feature_vector, cms)
                                  for cms in self.abnormal_data_for_filter2)
                    # if bucket.fp == "205.190.20.171":
                    #     print(maxsimi)
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
                    maxsimi = max(jaccard_est_of_simiSketch_CM(bucket.feature_vector, cms)
                                  for cms in self.abnormal_data_for_filter2)
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
        #print("scan_offset:%d"%self.scan_offset)
            # **更新 scan_offset，保证轮转遍历**
        # if self.scan_offsetA + self.scan_stepA>=total_size_A:
        #     self.scan_offsetA=0
        # else:
        #     self.scan_offsetA = (self.scan_offsetA + self.scan_stepA) % total_size_A
        #
        # if self.scan_offsetB + self.scan_stepB>=total_size_B:
        #     self.scan_offsetB=0
        # else:
        #     self.scan_offsetB = (self.scan_offsetB + self.scan_stepB) % total_size_B

        self.scan_times = (self.scan_times + 1) % alltimes
        return final_list

    def display(self):
        print("main buckets:")
        for i, item in enumerate(self.buckets_array[0]):
            print("No.%d: " % i, end=" ")
            if item is None:
                print("None")
            else:
                print("flow id:%s, similarity score:%.2f, S:%.2f" % (item.fp, item.similarity_score, item.query_S(self.alpha)))
                item.feature_vector.display()

        print("alter buckets:")
        for i, item in enumerate(self.buckets_array[1]):
            print("No.%d: " % i, end=" ")
            if item is None:
                print("None")
            else:
                print("flow id:%s, similarity score:%.2f, S:%.2f" % (item.fp, item.similarity_score, item.query_S(self.alpha)))
                item.feature_vector.display()



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
