import mmh3

class Filter1:
    def __init__(self,rows:int,cols:int):
        self.rows = rows
        self.cols = cols
        self.data = [[0 for _ in range(cols)] for _ in range(rows)]
        self.fplist=["0" for _ in range(rows)]

    def update(self,item:list[str]):
        if item[0] in self.fplist:
            index=mmh3.hash(item[1],seed=self.cols)%self.cols
            self.data[self.fplist.index(item[0])][index]+=1
            return
        if "0" in self.fplist:
            temp_row=self.fplist.index("0")
            self.fplist[temp_row]=item[0]
            index = mmh3.hash(item[1], seed=self.cols) % self.cols
            self.data[temp_row][index] += 1
            return




    def display(self):
        """
        打印矩阵。
        """
        for row in range(self.rows):
            print(self.fplist[row],end=" ")
            print(self.data[row])




if __name__=="__main__":
    filter1=Filter1(12,13)
    filter1.update(["aaaa","11bbb"])
    filter1.update(["aaaa", "11b4b"])
    filter1.update(["aaaa", "116bb"])
    filter1.display()