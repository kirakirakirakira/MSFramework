import json

# raw abnormal data:f:{e1,e2,e3,...}
# filter1 data
# filter2 data
# marked flow

with open("data.json", "r", encoding="utf-8") as file:
    loaded_data = json.load(file)


class StaticData:


    def __init__(self):
        self.abnormal_data=loaded_data



    @property
    def PI(self):
        return 3.14159


if __name__=="__main__":
    staticdata=StaticData()
    print(staticdata.PI)
    print(len(staticdata.test_ip))