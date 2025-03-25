import json
import random
import time

import mmh3

from CMSketch import CountMinSketch
from MaxLogHash import MaxLog, hash_parameter
from MinHash import MinHash16, generate_hash_params

# raw abnormal data:f:{e1,e2,e3,...}
# filter1 data
# filter2 data
# marked flow

# load abnormal data
with open("processed_data/filtered_flows.json", "r", encoding="utf-8") as file:
    loaded_data = json.load(file)


class StaticData:
    def __init__(self,seed="minhash_seed",col=1,CM_col=1,CM_row=1,k=2,k_minhash=1,p=65521):
        self.abnormal_data=loaded_data
        # cols=filter1.cols
        self.CM_col=CM_col
        self.CM_row = CM_row
        self.col=col
        self.k=k
        self.p=p
        self.k_minhash=k_minhash
        self.fplist=list(self.abnormal_data.keys())
        self.data_for_filter1=[[0 for _ in range(col)] for _ in range(len(self.fplist))]

        self.data_for_filter2 = [CountMinSketch(CM_col,CM_row) for _ in range(len(self.fplist))]
        self.data_for_maxlog=[MaxLog(k,k+2,hash_parameter(k,k),hash_parameter(k,k+1)) for _ in range(len(self.fplist))]
        self.data_for_minhash=[MinHash16(self.k_minhash,(*generate_hash_params(seed,self.k_minhash),self.p)) for _ in range(len(self.fplist))]
        # 需要时调用
        # self.update_data_for_filter1()
        # self.update_data_for_filter2()
        #self.update_data_for_maxlog()
        #update_data_for_minhash()
    def mmhash(self,eid):
        index = mmh3.hash(eid, seed=self.col) % self.col
        return index

    def update_data_for_filter1(self):
        starttime=time.time()
        for i in range(len(self.fplist)):
            fid=self.fplist[i]
            # print("fid:",end=" ")
            # print(fid)
            eids=self.abnormal_data[fid]
            # print("eid:",end=" ")
            # print(eids)
            for key,value in eids.items():
                # print(key)
                # print(value)
                # print(self.mmhash(key))
                self.data_for_filter1[i][self.mmhash(key)]+=value
        endtime=time.time()
        exetime=endtime-starttime
        print("构建异常向量组用时：%.2f seconds"%exetime)
        # for j in self.data_for_filter1:
        #     print(j)
        return

    def update_data_for_filter2(self):
        starttime = time.time()
        for i in range(len(self.fplist)):
            fid = self.fplist[i]
            eids = self.abnormal_data[fid]
            for key,value in eids.items():
                # print(key)
                # print(value)
                for j in range(value):
                    self.data_for_filter2[i].add(key)
        endtime = time.time()
        exetime = endtime - starttime
        print("构建异常CM结构用时：%.2f seconds" % exetime)
        # for cm in self.data_for_filter2:
        #     cm.display()
        return


    def update_data_for_maxlog(self):
        starttime = time.time()
        for i in range(len(self.fplist)):
            fid=self.fplist[i]
            eids = self.abnormal_data[fid]
            for key,value in eids.items():
                for j in range(value):
                    self.data_for_maxlog[i].process_item(key)
        endtime = time.time()
        exetime = endtime - starttime
        print("构建异常Maxlog结构用时：%.2f seconds" % exetime)
        return


    def update_data_for_minhash(self):
        starttime = time.time()
        for i in range(len(self.fplist)):
            fid = self.fplist[i]
            eids = self.abnormal_data[fid]
            for key, value in eids.items():
                for j in range(value):
                    self.data_for_minhash[i].update(key)
        endtime = time.time()
        exetime = endtime - starttime
        print("构建异常minhash结构用时：%.2f seconds" % exetime)
        return
if __name__=="__main__":
    st1=StaticData(k_minhash=128)
    st1.update_data_for_minhash()
