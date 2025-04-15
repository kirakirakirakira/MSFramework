import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams.update({
    'font.size': 20,
    'axes.titlesize': 20,
    'axes.labelsize': 20,
    'xtick.labelsize': 20,
    'ytick.labelsize': 20,
    'legend.fontsize': 20,
    'font.family': 'serif',
    'pdf.fonttype': 42
})

# 定义列名
columns_minhash = [
    'packet_size', 'entry_size', 'filter1_d', 'filter1_w', 'filter1_ct', 'flow_id_size', 'simi_size', 'timestamp_size',
    'filter2_main_num', 'filter2_alter_num', 'k_minhash', 'precision', 'recall', 'f1-score', 'insert-time', 'space(KB)',
    'filter1_threshold', 'filter2_threshold'
]

columns_maxloghash = [
    'packet_size', 'entry_size', 'filter1_d', 'filter1_w', 'filter1_ct', 'flow_id_size', 'simi_size', 'timestamp_size',
    'filter2_main_num', 'filter2_alter_num', 'k', 'precision', 'recall', 'f1-score', 'insert-time', 'space(KB)',
    'filter1_threshold', 'filter2_threshold'
]

columns_user = [
    'packet_size', 'entry_size', 'filter1_d', 'filter1_w', 'filter1_ct', 'flow_id_size', 'simi_size', 'timestamp_size',
    'filter2_main_num', 'filter2_alter_num', 'cm_depth', 'cm_width', 'cm_ct', 'precision', 'recall', 'f1-score',
    'insert-time', 'space(KB)', 'filter1_threshold', 'filter2_threshold'
]

# 解析minhash数据
minhash_data = """
10000000,20,20,272,8,32,4,10,10,5,200,0.2252,0.7576,0.3472,74.23,11,0.5,0.8
10000000,20,40,272,8,32,4,10,20,10,200,0.1849,0.8182,0.3016,73.82,22,0.5,0.8
10000000,20,60,272,8,32,4,10,30,15,200,0.1504,0.8636,0.2562,72.3,34,0.5,0.8
10000000,20,80,272,8,32,4,10,40,20,200,0.1477,0.9242,0.2547,75.48,45,0.5,0.8
10000000,20,100,272,8,32,4,10,50,25,200,0.1452,0.9545,0.2521,75.78,56,0.5,0.8
10000000,20,120,272,8,32,4,10,60,30,200,0.1484,0.9848,0.2579,76.79,68,0.5,0.8
10000000,20,140,272,8,32,4,10,70,35,200,0.1425,0.9848,0.249,78.9,79,0.5,0.8
10000000,20,160,272,8,32,4,10,80,40,200,0.1371,0.9848,0.2407,78.85,90,0.5,0.8
10000000,20,180,272,8,32,4,10,90,45,200,0.131,0.9848,0.2312,79.35,102,0.5,0.8
10000000,20,200,272,8,32,4,10,100,50,200,0.1346,0.9848,0.2368,81.31,113,0.5,0.8
10000000,20,220,272,8,32,4,10,110,55,200,0.1318,0.9848,0.2325,81.54,124,0.5,0.8
10000000,20,240,272,8,32,4,10,120,60,200,0.1265,0.9848,0.2242,79.99,136,0.5,0.8
10000000,20,260,272,8,32,4,10,130,65,200,0.1277,0.9848,0.2261,83.94,147,0.5,0.8
"""
df_minhash = pd.DataFrame([line.split(',') for line in minhash_data.strip().split('\n')], columns=columns_minhash)
df_minhash['method'] = 'minhash'

# 解析maxloghash数据
maxloghash_data = """
10000000,20,20,272,8,32,4,10,10,5,128,0.1121,0.9848,0.2013,8.55,7,0.5,0.9
10000000,20,20,272,8,32,4,10,10,5,128,0.1121,0.9848,0.2013,8.84,7,0.5,0.9
10000000,20,20,272,8,32,4,10,10,5,128,0.1121,0.9848,0.2013,8.76,7,0.5,0.9
10000000,20,40,272,8,32,4,10,20,10,128,0.081,0.9697,0.1495,8.11,14,0.5,0.9
10000000,20,60,272,8,32,4,10,30,15,128,0.0672,0.9697,0.1257,7.59,21,0.5,0.9
10000000,20,80,272,8,32,4,10,40,20,128,0.0634,0.9848,0.1191,7.31,28,0.5,0.9
10000000,20,100,272,8,32,4,10,50,25,128,0.0607,0.9848,0.1144,7.28,35,0.5,0.9
10000000,20,120,272,8,32,4,10,60,30,128,0.0535,0.9848,0.1015,7.05,42,0.5,0.9
10000000,20,140,272,8,32,4,10,70,35,128,0.0535,0.9848,0.1015,7.06,49,0.5,0.9
10000000,20,160,272,8,32,4,10,80,40,128,0.0504,0.9848,0.0959,6.81,57,0.5,0.9
10000000,20,180,272,8,32,4,10,90,45,128,0.0462,0.9848,0.0883,6.9,64,0.5,0.9
10000000,20,200,272,8,32,4,10,100,50,128,0.0453,0.9848,0.0866,7.08,71,0.5,0.9
10000000,20,220,272,8,32,4,10,110,55,128,0.0459,0.9848,0.0877,7.23,78,0.5,0.9
10000000,20,240,272,8,32,4,10,120,60,128,0.0448,0.9848,0.0857,10.89,85,0.5,0.9
10000000,20,260,272,8,32,4,10,130,65,128,0.0433,0.9848,0.083,8.2,92,0.5,0.9
10000000,20,280,272,8,32,4,10,140,70,128,0.0426,0.9848,0.0817,9.63,99,0.5,0.9
10000000,20,300,272,8,32,4,10,150,75,128,0.0419,0.9848,0.0804,11.13,106,0.5,0.9
10000000,20,320,272,8,32,4,10,160,80,128,0.0406,0.9848,0.078,7.97,114,0.5,0.9
10000000,20,340,272,8,32,4,10,170,85,128,0.0401,0.9848,0.0771,6.88,121,0.5,0.9
10000000,20,360,272,8,32,4,10,180,90,128,0.0391,0.9848,0.0752,6.82,128,0.5,0.9
10000000,20,380,272,8,32,4,10,190,95,128,0.0381,0.9848,0.0734,6.44,135,0.5,0.9
10000000,20,400,272,8,32,4,10,200,100,128,0.0371,0.9848,0.0715,6.66,142,0.5,0.9
"""
df_maxloghash = pd.DataFrame([line.split(',') for line in maxloghash_data.strip().split('\n')], columns=columns_maxloghash)
df_maxloghash['method'] = 'maxloghash'

# 解析用户数据并过滤最佳F1-score
user_data = """
10000000,20,20,272,8,32,4,10,10,5,1,272,16,1.0,0.2727,0.4285,9.95,13,0.5,0.5
10000000,20,20,272,8,32,4,10,10,5,1,272,16,1.0,0.2879,0.4471,13.5,13,0.5,0.5
10000000,20,20,272,8,32,4,10,10,5,1,272,16,1.0,0.3485,0.5169,10.99,13,0.5,0.5
10000000,20,40,272,8,32,4,10,20,10,1,272,16,1.0,0.3485,0.5169,10.59,26,0.5,0.5
10000000,20,60,272,8,32,4,10,30,15,1,272,16,1.0,0.5152,0.68,11.64,40,0.5,0.5
10000000,20,80,272,8,32,4,10,40,20,1,272,16,1.0,0.5909,0.7428,12.43,53,0.5,0.5
10000000,20,100,272,8,32,4,10,50,25,1,272,16,1.0,0.7879,0.8814,13.31,67,0.5,0.5
10000000,20,120,272,8,32,4,10,60,30,1,272,16,0.9815,0.803,0.8833,14.06,80,0.5,0.5
10000000,20,140,272,8,32,4,10,70,35,1,272,16,1.0,0.8636,0.9268,15.09,94,0.5,0.5
10000000,20,160,272,8,32,4,10,80,40,1,272,16,1.0,0.8788,0.9355,15.01,107,0.5,0.5
10000000,20,180,272,8,32,4,10,90,45,1,272,16,0.9672,0.8939,0.9291,17.51,121,0.5,0.5
10000000,20,200,272,8,32,4,10,100,50,1,272,16,0.9833,0.8939,0.9365,19.38,134,0.5,0.5
10000000,20,220,272,8,32,4,10,110,55,1,272,16,0.9833,0.8939,0.9365,19.9,147,0.5,0.5
"""
df_user = pd.DataFrame([line.split(',') for line in user_data.strip().split('\n')], columns=columns_user)
df_user['method'] = 'ours'

# 转换数据类型
numeric_cols = ['space(KB)', 'f1-score', 'insert-time']
for col in numeric_cols:
    df_minhash[col] = df_minhash[col].astype(float)
    df_maxloghash[col] = df_maxloghash[col].astype(float)
    df_user[col] = df_user[col].astype(float)

# 过滤用户数据中每组的最佳F1-score
group_keys = ['packet_size', 'entry_size', 'filter1_d', 'filter1_w', 'filter1_ct',
              'flow_id_size', 'simi_size', 'timestamp_size', 'filter2_main_num',
              'filter2_alter_num', 'cm_depth', 'cm_width', 'cm_ct']
df_user_filtered = df_user.loc[df_user.groupby(group_keys)['f1-score'].idxmax()]

# 在合并数据集后增加排序逻辑
df_combined = pd.concat([df_minhash, df_maxloghash, df_user_filtered])
df_combined = df_combined.sort_values(by='space(KB)')  # 全局排序


# 计算吞吐量（packets/sec）
df_combined['throughput'] = 10 / df_combined['insert-time']

# 绘制空间与F1-score关系图
def plot_with_limit(ax, x_col, y_col, ylabel, xlim=(0,150)):
    for method, group in df_combined.groupby('method'):
        group_sorted = group.sort_values(x_col)
        ax.plot(group_sorted[x_col], group_sorted[y_col],
                marker='o', linestyle='-', label=method)
    ax.set_xlabel('Space (KB)', fontweight='bold')
    ax.set_ylabel(ylabel, fontweight='bold')
    ax.set_xlim(xlim)  # 控制显示范围
    ax.legend()
    ax.grid(True)

# 创建带范围限制的图表
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# F1-score图表
plot_with_limit(ax1, 'space(KB)', 'f1-score', 'F1-score', xlim=(0, 150))
ax1.set_title('Space vs F1-score (0-150KB)',fontweight='bold')

# 吞吐量图表
plot_with_limit(ax2, 'space(KB)', 'throughput', 'Throughput (Mpps)', xlim=(0, 150))
ax2.set_title('Space vs Throughput (0-150KB)', fontweight='bold')
plt.savefig('fig\\vs_baseline_IMC.pdf',
           bbox_inches='tight',
           facecolor='white')
plt.show()