import math
import time
from CMSketch import CountMinSketch
from simiSketch import jaccard_est_of_simiSketch_CM
class Bucket:
    def __init__(self, fp=None,width=10,height=10):
        self.fp = fp
        self.feature_vector = CountMinSketch(width,height)
        self.similarity_score=0
        self.S = 0  # 综合指标 S

    def update_S(self, alpha,t_entry,t_window):
        T_now=time.time()
        age = T_now - t_entry
        normalized_age = math.exp(-age / t_window)
        self.S = alpha * self.similarity_score + (1 - alpha) * (1 - normalized_age)

class BucketArray:
    def __init__(self, sizeA,sizeB):
        #main buckets array and alter buckets array
        self.buckets_array=[[None] * sizeA,[None] * sizeB]
        self.alpha=0.8 #to be defined
        self.t_window=1000 #time window for measurement
        self.t_entry = time.time() #start time static
        self.scan_times=1

    def is_full(self):
        return all(bucket is not None for bucket in self.buckets_array[0]) and all(bucket is not None for bucket in self.buckets_array[1])

    def find_insert_index(self,fp):
        ct0,ct1=0,0
        empty_index0=None
        empty_index1=None
        for i, bucket in enumerate(self.buckets_array[0]):
            if bucket is not None:
                if bucket.fp is fp:
                    return [0,i]
            else:
                if ct0==0:
                    empty_index0=i
                    ct0=1
        for i, bucket in enumerate(self.buckets_array[1]):
            if bucket is not None:
                if bucket.fp is fp:
                    return [1,i]
            else:
                if ct1==0:
                    empty_index1=i
                    ct1=1

        if empty_index0 is not None:
            return [0,empty_index0]
        if empty_index1 is not None:
            return [1,empty_index1]
        return None

    def insert(self, packet:list[str]):
        index = self.find_insert_index(packet[0])
        if index is None:
            self.replace_least_S(packet[0])
            return
        if self.buckets_array[index[0]][index[1]] is None:
            self.buckets_array[index[0]][index[1]] = Bucket(packet[0], 10,10)
            self.buckets_array[index[0]][index[1]].feature_vector.add(packet[1])
            self.buckets_array[index[0]][index[1]].update_S(self.alpha, self.t_entry, self.t_window)

        else:
            self.buckets_array[index[0]][index[1]].feature_vector.add(packet[1])
            self.buckets_array[index[0]][index[1]].update_S(self.alpha, self.t_entry, self.t_window)
        return

    def replace_least_S(self, fp):
        min_S_index = min(
            range(len(self.buckets_array[1])),
            key=lambda i: self.buckets_array[1][i].S if self.buckets_array[1][i] is not None else float('inf')
        )
        self.buckets_array[1][min_S_index] = Bucket(fp,width=10,height=10)
        self.buckets_array[1][min_S_index].update_S(self.alpha, self.t_entry, self.t_window)

    def scan_and_swap(self, other_array, alpha, T_now, T_window):
        self.buckets = [
            bucket for bucket in self.buckets if bucket is not None  # 清理None值
        ]
        other_array.buckets = [
            bucket for bucket in other_array.buckets if bucket is not None
        ]

        if self.buckets and other_array.buckets:
            min_bucket = min(self.buckets, key=lambda b: b.S)
            max_bucket = max(other_array.buckets, key=lambda b: b.S)

            # 交换
            min_index = self.buckets.index(min_bucket)
            max_index = other_array.buckets.index(max_bucket)

            self.buckets[min_index], other_array.buckets[max_index] = (
                other_array.buckets[max_index], self.buckets[min_index]
            )


    def display(self):
        print("main buckets:")
        for i,item in enumerate(self.buckets_array[0]):
            print("No.%d: "%i,end=" ")
            if item is None:
                print("None")
            else:
                print("flow id:%s, similarity score:%.2f, S:%.2f"%(item.fp,item.similarity_score,item.S))
                #item.feature_vector.display()

        print("alter buckets:")
        for i, item in enumerate(self.buckets_array[1]):
            print("No.%d: " % i, end=" ")
            if item is None:
                print("None")
            else:
                print("flow id:%s, similarity score:%.2f, S:%.2f" % (item.fp, item.similarity_score, item.S))
               #item.feature_vector.display()



class TrafficMonitor:
    def __init__(self, main_size, alternative_size, alpha, T_window):
        self.main_buckets = BucketArray(main_size)
        self.alternative_buckets = BucketArray(alternative_size)
        self.alpha = alpha
        self.T_window = T_window

    def process_packet(self, fp, feature_vector, similarity_score):
        T_now = time.time()

        if not self.main_buckets.is_full():
            self.main_buckets.insert(fp, feature_vector, similarity_score, self.alpha, T_now, self.T_window)
        elif not self.alternative_buckets.is_full():
            self.alternative_buckets.insert(fp, feature_vector, similarity_score, self.alpha, T_now, self.T_window)
        else:
            self.alternative_buckets.replace_least_S(fp, feature_vector, similarity_score, self.alpha, T_now, self.T_window)

    def periodic_scan(self):
        T_now = time.time()
        self.main_buckets.scan_and_swap(self.alternative_buckets, self.alpha, T_now, self.T_window)

if __name__=="__main__":
    bucketArray=BucketArray(10,4)
    file_path = ["../data1/02.txt", "../data1/00.txt", "../data1/01.txt", "../data1/03.txt", "../data1/04.txt"]
    starttime=time.time()
    for path in file_path[:1]:
        # 逐行读取文件并统计源 IP 地址
        with open(path, "r", encoding="utf-8") as file:
            for line in file:
                # 去掉行尾换行符，并按空格分割
                parts = line.strip().split()
                if len(parts) == 2:  # 确保格式正确
                    bucketArray.insert(parts)

    endtime=time.time()
    print("%.2f s"%(endtime-starttime))
    bucketArray.display()