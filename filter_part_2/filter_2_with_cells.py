import time
import math
import mmh3
from typing import List

from BasicFunctions.CMSketch import CountMinSketch
from BasicFunctions.simiSketch import jaccard_est_of_simiSketch_CM
from static_data import StaticData
class Cell:
    def __init__(self, fp, width, height):
        self.col = width
        self.row = height
        self.fp = fp
        self.feature_vector = CountMinSketch(width, height)
        self.similarity_score = 0
        self.timestamp = time.time()

    def update(self, packet):
        self.feature_vector.add(packet[1])
        self.timestamp = time.time()

    def query_S(self, alpha):
        T_now = time.time()
        quantity = math.exp(-alpha * (T_now - self.timestamp))
        return quantity * self.similarity_score

class Bucket:
    def __init__(self, cell_num, width, height):
        self.cells: List[Cell] = []
        self.capacity = cell_num
        self.width = width
        self.height = height

    def find_cell_index(self, fp):
        for i, cell in enumerate(self.cells):
            if cell.fp == fp:
                return i
        return None

    def update_or_insert(self, packet, alpha):
        fp = packet[0]
        idx = self.find_cell_index(fp)
        if idx is not None:
            self.cells[idx].update(packet)
            return

        # 若未命中，找空位插入
        if len(self.cells) < self.capacity:
            new_cell = Cell(fp, self.width, self.height)
            new_cell.update(packet)
            self.cells.append(new_cell)
            return

        # 无空位，替换 S 值最小的
        min_idx = min(range(len(self.cells)), key=lambda i: self.cells[i].query_S(alpha))
        self.cells[min_idx] = Cell(fp, self.width, self.height)
        self.cells[min_idx].update(packet)

class BucketArray:
    def __init__(self, array_size, cell_per_bucket, col=272, row=1, threshold=0.4, alpha=0.1):
        self.col = col
        self.row = row
        self.size = array_size
        self.cell_per_bucket = cell_per_bucket
        self.threshold = threshold
        self.alpha = alpha
        self.buckets = [Bucket(cell_per_bucket, col, row) for _ in range(array_size)]
        self.scan_times=1
        self.staticdata = StaticData(CM_col=self.col, CM_row=self.row)
        self.staticdata.update_data_for_filter2()
        self.abnormal_data_for_filter2 = self.staticdata.data_for_filter2

        self.filter2_insert_time = 0
        self.filter2_scan_time = 0
    def _hash(self, fp):
        return mmh3.hash(fp) % self.size

    def insert(self, packet: List[str]):
        starttime = time.time()
        idx = self._hash(packet[0])
        self.buckets[idx].update_or_insert(packet, self.alpha)
        endtime = time.time()
        self.filter2_insert_time += (endtime - starttime)

    def first_update(self, scan_result):
        for k in range(len(scan_result[0])):
            fp = scan_result[0][k]
            packet_vector = scan_result[1][k]
            idx = self._hash(fp)
            bucket = self.buckets[idx]
            cell_idx = bucket.find_cell_index(fp)

            if cell_idx is not None:
                cell = bucket.cells[cell_idx]
            elif len(bucket.cells) < bucket.capacity:
                cell = Cell(fp, self.col, self.row)
                bucket.cells.append(cell)
            else:
                # 替换 S 最小的 cell
                min_idx = min(range(len(bucket.cells)), key=lambda i: bucket.cells[i].query_S(self.alpha))
                cell = Cell(fp, self.col, self.row)
                bucket.cells[min_idx] = cell

            # 初始化 feature_vector
            if self.row == 1:
                cell.feature_vector.table[0] = [max(x, 0) for x in packet_vector]
            else:
                for i in range(self.row):
                    cell.feature_vector.table[i] = [0 for _ in range(self.col)]

    def find_and_swap(self, alltimes):
        final_list = set()

        if self.scan_times == 0:
            starttime = time.time()

            for bucket in self.buckets:
                retained_cells = []
                for cell in bucket.cells:
                    maxsimi = max(
                        jaccard_est_of_simiSketch_CM(cell.feature_vector, cms)
                        for cms in self.abnormal_data_for_filter2
                    )
                    cell.similarity_score = maxsimi

                    if cell.similarity_score > self.threshold:
                        final_list.add(cell.fp)
                        # 不加入 retained_cells，相当于删除该 cell
                    else:
                        retained_cells.append(cell)

                bucket.cells = retained_cells  # 执行删除逻辑

            endtime = time.time()
            self.filter2_scan_time += (endtime - starttime)

        self.scan_times = (self.scan_times + 1) % alltimes
        return final_list

