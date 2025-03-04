from CMSketch import CountMinSketch

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
        jaccard_est=min(numerator/denominator if denominator>0 else 0,jaccard_est)
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



if __name__ == "__main__":
    cms1 = CountMinSketch(1000, 10)
    cms2 = CountMinSketch(1000, 10)