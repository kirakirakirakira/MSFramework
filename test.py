import pandas as pd
from io import StringIO

data='''packet_size,entry_size,filter1_d,filter1_w,filter1_ct,flow_id_size,simi_size,timestamp_size,filter2_main_num,filter2_alter_num,cm_depth,cm_width,cm_ct,precision,recall,f1-score,insert-time,space(KB),filter1_threshold,filter2_threshold 
10000000,20,20,272,8,32,4,10,10,5,1,272,16,0.8571,0.2857,0.4285,19.3,13,0.5,0.5
10000000,20,40,272,8,32,4,10,20,10,1,272,16,0.9375,0.7143,0.8108,19.65,26,0.5,0.5
10000000,20,60,272,8,32,4,10,30,15,1,272,16,0.9474,0.8571,0.9,19.02,40,0.5,0.5
10000000,20,80,272,8,32,4,10,40,20,1,272,16,0.9048,0.9048,0.9048,19.36,53,0.5,0.5
10000000,20,100,272,8,32,4,10,50,25,1,272,16,0.9545,1.0,0.9767,18.94,67,0.5,0.5
10000000,20,120,272,8,32,4,10,60,30,1,272,16,0.9524,0.9524,0.9524,19.08,80,0.5,0.5
10000000,20,140,272,8,32,4,10,70,35,1,272,16,0.9545,1.0,0.9767,20.37,94,0.5,0.5
10000000,20,160,272,8,32,4,10,80,40,1,272,16,0.9524,0.9524,0.9524,19.23,107,0.5,0.5
10000000,20,180,272,8,32,4,10,90,45,1,272,16,0.9545,1.0,0.9767,19.58,121,0.5,0.5
10000000,20,200,272,8,32,4,10,100,50,1,272,16,0.9545,1.0,0.9767,19.86,134,0.5,0.5
10000000,20,220,272,8,32,4,10,110,55,1,272,16,0.9545,1.0,0.9767,19.58,147,0.5,0.5'''

# 读取数据到DataFrame
df = pd.read_csv(StringIO(data))

# 计算平均值
avg_precision = df['precision'].mean()
avg_recall = df['recall'].mean()
avg_f1 = df['f1-score'].mean()
avg_insert_time = df['insert-time'].mean()
print("以下是我们的方法：")
print(f"平均 precision: {avg_precision:.4f}")
print(f"平均 recall: {avg_recall:.4f}")
print(f"平均 f1-score: {avg_f1:.4f}")
print(f"平均 insert-time: {avg_insert_time:.4f}\n")


data='''
packet_size,entry_size,filter1_d,filter1_w,filter1_ct,flow_id_size,simi_size,timestamp_size,filter2_main_num,filter2_alter_num,k,precision,recall,f1-score,insert-time,space(KB),filter1_threshold,filter2_threshold
10000000,20,40,272,8,32,4,10,20,10,128,0.1382,1.0,0.2428,20.46,14,0.5,0.9
10000000,20,80,272,8,32,4,10,40,20,128,0.0837,1.0,0.1545,20.07,28,0.5,0.9
10000000,20,120,272,8,32,4,10,60,30,128,0.0614,1.0,0.1157,19.26,42,0.5,0.9
10000000,20,160,272,8,32,4,10,80,40,128,0.0494,1.0,0.0941,19.92,57,0.5,0.9
10000000,20,200,272,8,32,4,10,100,50,128,0.0431,1.0,0.0826,19.38,71,0.5,0.9
10000000,20,240,272,8,32,4,10,120,60,128,0.0378,1.0,0.0728,19.15,85,0.5,0.9
10000000,20,280,272,8,32,4,10,140,70,128,0.033,1.0,0.0639,19.25,99,0.5,0.9
10000000,20,320,272,8,32,4,10,160,80,128,0.0314,1.0,0.0609,18.89,114,0.5,0.9
10000000,20,360,272,8,32,4,10,180,90,128,0.0275,1.0,0.0535,20.55,128,0.5,0.9
10000000,20,400,272,8,32,4,10,200,100,128,0.0257,1.0,0.0501,21.11,142,0.5,0.9'''
df = pd.read_csv(StringIO(data))

# 计算平均值
avg_precision0 = df['precision'].mean()
avg_recall0 = df['recall'].mean()
avg_f10 = df['f1-score'].mean()
avg_insert_time0 = df['insert-time'].mean()

print("以下是maxloghash的方法：")
print(f"平均 precision: {avg_precision0:.4f}")
print(f"我们方法的指标是该方法的{avg_precision/avg_precision0:.4f}倍")
print(f"平均 recall: {avg_recall0:.4f}")
print(f"我们方法的指标是该方法的{avg_recall/avg_recall0:.4f}倍")
print(f"平均 f1-score: {avg_f10:.4f}")
print(avg_f1/avg_f10)
print(f"平均 insert-time: {avg_insert_time0:.4f}\n")
print(f"我们方法的吞吐量是该方法的{avg_insert_time0/avg_insert_time:.4f}倍")


data='''packet_size,entry_size,filter1_d,filter1_w,filter1_ct,flow_id_size,simi_size,timestamp_size,filter2_main_num,filter2_alter_num,k_minhash,precision,recall,f1-score,insert-time,space(KB),filter1_threshold,filter2_threshold
10000000,20,20,272,8,32,4,10,10,5,200,0.6667,0.9524,0.7843,23.9,11,0.5,0.9
10000000,20,40,272,8,32,4,10,20,10,200,0.625,0.9524,0.7547,23.85,22,0.5,0.9
10000000,20,60,272,8,32,4,10,30,15,200,0.625,0.9524,0.7547,24.5,34,0.5,0.9
10000000,20,80,272,8,32,4,10,40,20,200,0.5882,0.9524,0.7273,24.9,45,0.5,0.9
10000000,20,100,272,8,32,4,10,50,25,200,0.5556,0.9524,0.7018,24.09,56,0.5,0.9
10000000,20,120,272,8,32,4,10,60,30,200,0.5556,0.9524,0.7018,25.33,68,0.5,0.9
10000000,20,140,272,8,32,4,10,70,35,200,0.5278,0.9048,0.6667,25.63,79,0.5,0.9
10000000,20,160,272,8,32,4,10,80,40,200,0.4878,0.9524,0.6452,25.31,90,0.5,0.9
10000000,20,180,272,8,32,4,10,90,45,200,0.5263,0.9524,0.678,26.92,102,0.5,0.9
10000000,20,200,272,8,32,4,10,100,50,200,0.5882,0.9524,0.7273,26.11,113,0.5,0.9
10000000,20,220,272,8,32,4,10,110,55,200,0.5556,0.9524,0.7018,26.76,124,0.5,0.9
10000000,20,240,272,8,32,4,10,120,60,200,0.5405,0.9524,0.6896,27.46,136,0.5,0.9'''
df = pd.read_csv(StringIO(data))

# 计算平均值
avg_precision1 = df['precision'].mean()
avg_recall1 = df['recall'].mean()
avg_f11 = df['f1-score'].mean()
avg_insert_time1 = df['insert-time'].mean()

print("以下是minhash的方法：")
print(f"平均 precision: {avg_precision1:.4f}")
print(avg_precision/avg_precision1)
print(f"平均 recall: {avg_recall1:.4f}")
print(avg_recall/avg_recall1)
print(f"平均 f1-score: {avg_f11:.4f}")
print(avg_f1/avg_f11)
print(f"平均 insert-time: {avg_insert_time1:.4f}")
print(avg_insert_time1/avg_insert_time)