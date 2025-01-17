import math
import time
from collections import Counter

import mmh3

from static_data import StaticData

class Filter1:
    def __init__(self,rows:int,cols:int):
        self.rows = rows
        self.cols = cols
        self.data = [[0 for _ in range(cols)] for _ in range(rows)]
        self.fplist=["" for _ in range(rows)]
        self.simi_list=[0 for _ in range(rows)]
        self.scan_times=1
        self.threshold=0.8 #to be modified
        self.staticdata=StaticData(self.cols)
        #abnormal flow
        self.abnormal_data_for_filter1=self.staticdata.data_for_filter1
        self.abnormal_flow_ids=self.staticdata.fplist
        self.filter1_insert_time=0
        self.filter1_scan_time=0
    def update(self,item:list[str]):
        starttime = time.time()
        index = mmh3.hash(item[1], seed=self.cols) % self.cols
        if item[0] in self.fplist:
            self.data[self.fplist.index(item[0])][index]+=1
            return
        if "" in self.fplist:
            temp_row=self.fplist.index("")
            self.fplist[temp_row]=item[0]
            self.data[temp_row][index] += 1
            return

        min_simi=2
        index_of_minsimi=0
        for i in range(self.rows):
            if self.simi_list[i]<min_simi:
                min_simi=self.simi_list[i]
                index_of_minsimi=i

        if sum(self.data[index_of_minsimi])<0 or min_simi<0:
            self.fplist[index_of_minsimi]=item[0]
            self.data[index_of_minsimi]=[0 for i in range(self.cols)]
            self.data[index_of_minsimi][index] += 1
            self.simi_list[index_of_minsimi]=0
        else:
            self.data[index_of_minsimi][index] -= 1

        endtime = time.time()
        exetime = endtime - starttime
        self.filter1_insert_time+=exetime
        # print("本次filter1插入用时%.2f sec" % exetime)

    def scan(self,times=10):

        flow_to_next_filter=set()
        if self.scan_times==0:
            starttime = time.time()
            for i in range(self.rows):
                maxsim=0
                for j in self.abnormal_data_for_filter1:
                    dot_product = sum(a * b for a, b in zip(self.data[i], j))
                    norm1 = math.sqrt(sum(a ** 2 for a in self.data[i]))
                    norm2 = math.sqrt(sum(b ** 2 for b in j))
                    simi=dot_product / (norm1 * norm2) if norm2*norm1!=0 else 0
                        # 计算余弦相似度
                    if simi>maxsim:
                        maxsim=simi
                self.simi_list[i]=maxsim
                #mark and clear potential abnormal flow id
                if maxsim>self.threshold:
                    flow_to_next_filter.add(self.fplist[i])
                    self.data[i]=[0 for _ in range(self.cols)]
                    self.fplist[i]=""
                    self.simi_list[i]=0
            endtime = time.time()
            exetime = endtime - starttime
            #print("本次filter1扫描用时%.2f sec" % exetime)
            self.filter1_scan_time += exetime
        self.scan_times=(self.scan_times+1 )%times

        return flow_to_next_filter

    def display(self):
        """
        打印矩阵。
        """
        for row in range(self.rows):
            print(self.fplist[row],end=" ")
            print(self.data[row],end=" ")
            print(self.simi_list[row])




if __name__=="__main__":
    filter1=Filter1(30,50)
    file_path = ["../data1/02.txt", "../data1/00.txt", "../data1/01.txt", "../data1/03.txt", "../data1/04.txt"]
    abnormal_list=[]
    # 用于存储源 IP 地址的计数器
    source_ip_count = Counter()
    start_time=time.time()
    # update counter return ip-frequency pairs
    for path in file_path[:1]:
        # 逐行读取文件并统计源 IP 地址
        with open(path, "r", encoding="utf-8") as file:
            for line in file:
                # 去掉行尾换行符，并按空格分割
                parts = line.strip().split()
                if len(parts) == 2:  # 确保格式正确
                    source_ip = parts[0]  # 第一个部分是源 IP 地址
                    destination_ip=parts[1]
                    filter1.update([source_ip,destination_ip])
                    abnormal_list+=filter1.scan(10000)
                    if filter1.scan_times==0:
                        end_time = time.time()
                        print("扫描累计用时%.2f秒" % (end_time - start_time))
                    #print(filter1.scan_times)
    end_time = time.time()
    print("用时%.2f秒"%(end_time-start_time))

    # for j in filter1.abnormal_data_for_filter1:
    #
    #     dot_product = sum(a * b for a, b in zip(filter1.data[28], j))
    #     norm1 = math.sqrt(sum(a ** 2 for a in filter1.data[28]))
    #     norm2 = math.sqrt(sum(b ** 2 for b in j))
    #     simi = dot_product / (norm1 * norm2) if norm2 * norm1 != 0 else 0
    #     if simi>0:
    #         print(j)
    #         print(filter1.data[28])
    #         print(simi)
    #         break
    abnormal_list=list(set(abnormal_list))
    true_abnormal=filter1.abnormal_flow_ids
    tp = len(set(abnormal_list) & set(true_abnormal))
    fp = len(set(abnormal_list) - set(true_abnormal))
    fn = len(set(true_abnormal) - set(abnormal_list))

    # 计算准确率和召回率
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0

    print(f"准确率 (Precision): {precision:.2f}")
    print(f"召回率 (Recall): {recall:.2f}")
    filter1.display()