
# raw data:f:{e1,e2,e3,...}
# filter1 data
# filter2 data
# marked flow
class StaticData:


    def __init__(self):
        self.rawdata=[]


    @property
    def PI(self):
        return 3.14159


if __name__=="__main__":
    staticdata=StaticData()
    print(staticdata.PI)