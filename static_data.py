import json
import random
import time

import mmh3

from CMSketch import CountMinSketch

# raw abnormal data:f:{e1,e2,e3,...}
# filter1 data
# filter2 data
# marked flow

# load abnormal data
with open("filtered_flows.json", "r", encoding="utf-8") as file:
    loaded_data = json.load(file)


class StaticData:
    def __init__(self,col=272,CM_col=272,CM_row=1):
        self.abnormal_data=loaded_data
        # cols=filter1.cols
        self.CM_col=CM_col
        self.CM_row = CM_row
        self.col=col
        self.fplist=list(self.abnormal_data.keys())
        self.data_for_filter1=[[0 for _ in range(col)] for _ in range(len(self.fplist))]

        self.data_for_filter2 = [CountMinSketch(CM_col,CM_row) for _ in range(len(self.fplist))]
        # 需要时调用
        # self.update_data_for_filter1()
        # self.update_data_for_filter2()
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
        for j in self.data_for_filter1:
            print(j)
        return

    def update_data_for_filter2(self):
        starttime = time.time()
        for i in range(len(self.fplist)):
            fid = self.fplist[i]
            eids = self.abnormal_data[fid]
            for key,value in eids.items():
                print(key)
                print(value)
                for j in range(value):
                    self.data_for_filter2[i].add(key)
        endtime = time.time()
        exetime = endtime - starttime
        print("构建异常CM结构用时：%.2f seconds" % exetime)
        for cm in self.data_for_filter2:
            cm.display()
        return


    @property
    def PI(self):
        return 3.14159


if __name__=="__main__":
    staticdata=StaticData(100,272,7)
    for j in staticdata.data_for_filter2:
        j.display()
