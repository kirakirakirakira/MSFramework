import pandas as pd
from io import StringIO

csv_data = """packet_size,entry_size,filter1_d,filter1_w,filter1_ct,flow_id_size,simi_size,timestamp_size,filter2_main_num,filter2_alter_num,cm_depth,cm_width,cm_ct,precision,recall,f1-score,insert-time,space(KB),filter1_threshold,filter2_threshold
10000000,20,20,272,8,32,32,32,10,5,1,272,16,0.8571,0.2857,0.4285,19.3,13,0.5,0.5
10000000,20,40,272,8,32,32,32,20,10,1,272,16,0.9375,0.7143,0.8108,19.65,26,0.5,0.5
10000000,20,60,272,8,32,32,32,30,15,1,272,16,0.9474,0.8571,0.9,19.02,40,0.5,0.5
10000000,20,80,272,8,32,32,32,40,20,1,272,16,0.9048,0.9048,0.9048,19.36,53,0.5,0.5
10000000,20,100,272,8,32,32,32,50,25,1,272,16,0.9545,1.0,0.9767,18.94,67,0.5,0.5
10000000,20,120,272,8,32,32,32,60,30,1,272,16,0.9524,0.9524,0.9524,19.08,80,0.5,0.5
10000000,20,140,272,8,32,32,32,70,35,1,272,16,0.9545,1.0,0.9767,20.37,94,0.5,0.5
10000000,20,160,272,8,32,32,32,80,40,1,272,16,0.9524,0.9524,0.9524,19.23,107,0.5,0.5
10000000,20,180,272,8,32,32,32,90,45,1,272,16,0.9545,1.0,0.9767,19.58,121,0.5,0.5
10000000,20,200,272,8,32,32,32,100,50,1,272,16,0.9545,1.0,0.9767,19.86,134,0.5,0.5
10000000,20,220,272,8,32,32,32,110,55,1,272,16,0.9545,1.0,0.9767,19.58,147,0.5,0.5
"""

df = pd.read_csv(StringIO(csv_data))

def compute_space_kb(row):
    f1_bits = row['filter1_d'] * row['filter1_w'] * row['filter1_ct'] + row['filter1_d'] * (row['flow_id_size'] + row['simi_size'])
    f2_count = row['filter2_main_num'] + row['filter2_alter_num']
    f2_bits = f2_count * (row['cm_depth'] * row['cm_width'] * row['cm_ct'] + row['flow_id_size'] + row['simi_size'] + row['timestamp_size'])
    return int((f1_bits + f2_bits) / 8 // 1024)

df["recomputed_space(KB)"] = df.apply(compute_space_kb, axis=1)
print(df[["space(KB)", "recomputed_space(KB)"]])