import json
import random
import mmh3

from CMSketch import CountMinSketch

# raw abnormal data:f:{e1,e2,e3,...}
# filter1 data
# filter2 data
# marked flow

# load abnormal data
with open("abnormal_data.json", "r", encoding="utf-8") as file:
    loaded_data = json.load(file)


class StaticData:
    def __init__(self,col=10,CM_col=10,CM_row=10):
        self.abnormal_data=loaded_data
        # cols=filter1.cols
        self.CM_col=CM_col
        self.CM_row = CM_row
        self.col=col
        self.fplist=list(self.abnormal_data.keys())
        self.data_for_filter1=[[0 for _ in range(col)] for _ in range(len(self.fplist))]
        self.update_data_for_filter1()
        self.data_for_filter2 = [CountMinSketch(CM_col,CM_row) for _ in range(len(self.fplist))]
        self.update_data_for_filter2()
    def mmhash(self,eid):
        index = mmh3.hash(eid, seed=self.col) % self.col
        return index

    def update_data_for_filter1(self):
        for i in range(len(self.fplist)):
            fid=self.fplist[i]
            eids=self.abnormal_data[fid]
            for j in eids:
                self.data_for_filter1[i][self.mmhash(j)]+=1
        return

    def update_data_for_filter2(self):
        for i in range(len(self.fplist)):
            fid = self.fplist[i]
            eids = self.abnormal_data[fid]
            for j in eids:
                self.data_for_filter2[i].add(j)
        return


    @property
    def PI(self):
        return 3.14159


if __name__=="__main__":
    staticdata=StaticData()

    print(len(staticdata.abnormal_data))
    random_key, random_value = random.choice(list(staticdata.abnormal_data.items()))
    print(f"随机选择的 key: {random_key}, value: {len(random_value)}")
    print(staticdata.fplist[:10])
    print(staticdata.data_for_filter1[:10])