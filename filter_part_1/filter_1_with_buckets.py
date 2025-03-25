import math
import time
from collections import Counter

import mmh3

from static_data import StaticData


class Filter1:
    def __init__(self, bucket_count: int, entries_per_bucket: int, cols: int, max_counter=2 ** 7 - 1,min_counter=-2**7):
        self.bucket_count = bucket_count
        self.entries_per_bucket = entries_per_bucket
        self.cols = cols
        self.max_counter_size = max_counter
        self.min_counter_size = min_counter
        # 初始化桶结构，每个桶有entries_per_bucket个条目
        self.data = [[[0 for _ in range(cols)] for _ in range(entries_per_bucket)] for _ in range(bucket_count)]
        self.fplist = [["" for _ in range(entries_per_bucket)] for _ in range(bucket_count)]
        self.simi_list = [[0 for _ in range(entries_per_bucket)] for _ in range(bucket_count)]
        self.scan_times = 1
        self.threshold = 0.5  # 可调整的阈值
        self.staticdata = StaticData(col=self.cols)
        self.staticdata.update_data_for_filter1()
        self.abnormal_data_for_filter1 = self.staticdata.data_for_filter1
        self.abnormal_flow_ids = self.staticdata.fplist
        self.filter1_insert_time = 0
        self.filter1_scan_time = 0

    def update(self, item: list[str]):
        starttime = time.time()
        flow_id, element = item[0], item[1]
        # 计算哈希桶位置和列索引
        bucket = mmh3.hash(flow_id, seed=self.cols) % self.bucket_count  # 使用不同种子区分哈希函数
        index = mmh3.hash(element, seed=self.cols) % self.cols

        # 检查当前流是否已存在桶中
        for entry_idx in range(self.entries_per_bucket):
            if self.fplist[bucket][entry_idx] == flow_id:
                self.data[bucket][entry_idx][index] = min(self.max_counter_size,
                                                          self.data[bucket][entry_idx][index] + 1)
                self.filter1_insert_time += time.time() - starttime
                return

        # 查找空条目
        for entry_idx in range(self.entries_per_bucket):
            if self.fplist[bucket][entry_idx] == "":
                self.fplist[bucket][entry_idx] = flow_id
                self.data[bucket][entry_idx][index] = min(self.data[bucket][entry_idx][index] + 1,
                                                          self.max_counter_size)
                self.filter1_insert_time += time.time() - starttime
                return

        # 找到桶内相似度最小的条目进行替换或减计数
        min_simi = float('inf')
        min_entry_idx = 0
        for entry_idx in range(self.entries_per_bucket):
            if self.simi_list[bucket][entry_idx] < min_simi:
                min_simi = self.simi_list[bucket][entry_idx]
                min_entry_idx = entry_idx

        if min_simi < 0.1:
            self.fplist[bucket][min_entry_idx] = flow_id
            self.data[bucket][min_entry_idx] = [0] * self.cols
            self.data[bucket][min_entry_idx][index] = 1
            self.simi_list[bucket][min_entry_idx] = 0
        else:
            self.data[bucket][min_entry_idx][index] = max(self.min_counter_size, self.data[bucket][min_entry_idx][index] - 1)

        self.filter1_insert_time += time.time() - starttime

    def scan(self, times=10):
        if self.scan_times != 0:
            self.scan_times = (self.scan_times + 1) % times
            return None

        starttime = time.time()
        flow_to_next_filter = []
        flow_content = []

        for bucket_idx in range(self.bucket_count):
            for entry_idx in range(self.entries_per_bucket):
                if self.fplist[bucket_idx][entry_idx] == "":
                    continue

                maxsim = 0
                for j in self.abnormal_data_for_filter1:
                    vec = self.data[bucket_idx][entry_idx]
                    dot = sum(a * b for a, b in zip(vec, j))
                    norm1 = math.sqrt(sum(a ** 2 for a in vec))
                    norm2 = math.sqrt(sum(b ** 2 for b in j))
                    simi = dot / (norm1 * norm2) if norm1 * norm2 != 0 else 0
                    if simi > maxsim:
                        maxsim = simi

                self.simi_list[bucket_idx][entry_idx] = maxsim
                if maxsim > self.threshold:
                    flow_to_next_filter.append(self.fplist[bucket_idx][entry_idx])
                    flow_content.append(self.data[bucket_idx][entry_idx])
                    # 重置条目
                    self.fplist[bucket_idx][entry_idx] = ""
                    self.data[bucket_idx][entry_idx] = [0] * self.cols
                    self.simi_list[bucket_idx][entry_idx] = 0

        self.scan_times = (self.scan_times + 1) % times
        self.filter1_scan_time += time.time() - starttime
        return [flow_to_next_filter, flow_content] if flow_to_next_filter else None

    def display(self):
        """
        打印矩阵。
        """
        for row in range(self.bucket_count):
            for entry_num in range(self.entries_per_bucket):
                print(self.fplist[row][entry_num],end=" ")
                print(self.data[row][entry_num],end=" ")
                print(self.simi_list[row][entry_num])




if __name__=="__main__":
   pass