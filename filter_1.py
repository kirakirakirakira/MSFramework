import mmh3

class Filter1:
    def __init__(self,rows:int,cols:int):
        self.rows = rows
        self.cols = cols
        self.data = [[0 for _ in range(cols)] for _ in range(rows)]
        self.fplist=["" for _ in range(rows)]
        self.simi_list=[0 for _ in range(rows)]

    def update(self,item:list[str]):
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

        if min_simi<0:
            self.fplist[index_of_minsimi]=item[0]
            self.data[index_of_minsimi]=[0 for i in range(self.cols)]
            self.data[index_of_minsimi][index] += 1
            self.simi_list[index_of_minsimi]=0
        else:
            self.data[index_of_minsimi][index] -= 1




    def display(self):
        """
        打印矩阵。
        """
        for row in range(self.rows):
            print(self.fplist[row],end=" ")
            print(self.data[row],end=" ")
            print(self.simi_list[row])




if __name__=="__main__":
    filter1=Filter1(3,3)
    filter1.update(["aaaa","11bbb"])
    filter1.update(["aaaa", "11b4b"])
    filter1.update(["aa11", "1160b"])
    filter1.update(["aa11", "119bb"])
    filter1.update(["aa2a", "1166b"])
    filter1.update(["aaaaca", "116bb"])
    filter1.update(["aaaaca", "112b"])
    filter1.update(["aaaaca", "1164b"])
    filter1.display()