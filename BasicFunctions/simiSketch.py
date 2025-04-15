import json
import time

from BasicFunctions.CMSketch import CountMinSketch

#methods for calculating similarity

def jaccard_est_of_simiSketch_CM(cms1,cms2):
    if not cms1 or not cms2:
        return 0

    if cms1.depth!=cms2.depth:
        print("can't estimate")
        return 0
    if cms1.width!=cms2.width:
        print("can't estimate")
        return 0
    depth=cms1.depth
    width=cms1.width
    jaccard_est = 1
    for i in range(depth):
        numerator=0
        denominator=0

        for j in range(width):
            numerator+=min(cms1.table[i][j],cms2.table[i][j])
            denominator+=max(cms1.table[i][j],cms2.table[i][j])
        jaccard_est=min(numerator/denominator if denominator>0 and numerator>0 else 0,jaccard_est)
    return jaccard_est

def jaccard_est_of_simiSketch_C(cs1,cs2):
    if cs1.depth!=cs2.depth:
        print("can't estimate")
        return
    if cs1.width!=cs2.width:
        print("can't estimate")
        return
    depth=cs1.depth
    width=cs1.width
    jaccard_est=0
    for i in range(depth):
        for j in range(width):
            jaccard_est+=min(abs(cs1.table[i][j]),abs(cs2.table[i][j]))/max(abs(cs1.table[i][j]),abs(cs2.table[i][j])) if cs1.table[i][j]*cs2.table[i][j]>0 else 0


    return jaccard_est/depth/width






def jaccard_similarity(frequency_dict_a, frequency_dict_b):
    """
    计算两个多重集合的Jaccard相似度
    :param frequency_dict_a: 数据集A的频率字典
    :param frequency_dict_b: 数据集B的频率字典
    :return: Jaccard相似度
    """
    # 计算交集部分
    intersection_sum = 0
    for i in frequency_dict_a:
        if i in frequency_dict_b:
            intersection_sum += min(frequency_dict_a[i], frequency_dict_b[i])

    # 计算并集部分
    union_sum = 0
    all_items = set(frequency_dict_a.keys()).union(set(frequency_dict_b.keys()))
    for item in all_items:
        union_sum += max(frequency_dict_a.get(item, 0), frequency_dict_b.get(item, 0))

    # Jaccard相似度
    if union_sum == 0:  # 防止除以0
        return 0.0
    return intersection_sum / union_sum

def abnormal_CM(width,depth):
    abnormal_flow={}
    with open("../processed_data/caida_ab_flow.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    for source_ip,des_ips in data.items():
        abnormal_flow[source_ip]=CountMinSketch(width,depth)
        for des_ip,num in des_ips.items():
            for i in range(num):
                abnormal_flow[source_ip].add(des_ip)
    return abnormal_flow

def all_flow_CM(width,depth):
    all_flow={}
    file_path = ["../data1/02.txt", "../data1/00.txt", "../data1/01.txt", "../data1/03.txt", "../data1/04.txt"]
    for path in file_path[:1]:
        # 一次性读取文件内容到内存
        with open(path, "r", encoding="utf-8") as file:
            lines = file.readlines()[:10000000]  # 将文件所有行读入列表
    for line in lines:
        item = line.strip().split()
        if item[0] not in all_flow.keys():
            all_flow[item[0]]=CountMinSketch(width,depth)
        all_flow[item[0]].add(item[1])
    return all_flow

def memory_calculate_KB(card,width,depth,counter=16):
    return int(card*width*depth*counter/8/1024/1024)

if __name__ == "__main__":
    print(memory_calculate_KB(167000,272,1,16))
    abnormal_flow=abnormal_CM(272,1)
    abnormal_flow_id=set(abnormal_flow.keys())
    starttime=time.time()
    all_flow=all_flow_CM(272,1)
    print("card：%d"%len(all_flow))
    print(all_flow.get("82.96.243.186").display())
    endtime=time.time()
    alltime=round(endtime-starttime,2)
    print("用时%.2f s"%alltime)
    est_ab_flow=set()
    for ab_ip,ab_CM in abnormal_flow.items():
        for ip,CM in all_flow.items():
            if jaccard_est_of_simiSketch_CM(ab_CM,CM)>0.9:
                est_ab_flow.add(ip)
    tp = len(abnormal_flow_id & est_ab_flow)  # True Positives
    fp = len(est_ab_flow - abnormal_flow_id)  # False Positives
    fn = len(abnormal_flow_id - est_ab_flow)  # False Negatives

    precision = round(tp / (tp + fp) if (tp + fp) > 0 else 0, 4)
    recall = round(tp / (tp + fn) if (tp + fn) > 0 else 0, 4)
    f1 = round(2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0, 4)
    endtime=time.time()
    real_alltime=round(endtime-starttime,2)
    print("实际用时%.2f s"%real_alltime)
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"F1 Score: {f1:.4f}")