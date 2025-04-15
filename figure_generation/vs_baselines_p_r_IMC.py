import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
plt.rcParams.update({
    'font.size': 24,
    'axes.titlesize': 24,
    'axes.labelsize': 24,
    'xtick.labelsize': 24,
    'ytick.labelsize': 24,
    'legend.fontsize': 24,
    'font.family': 'Times New Roman',
    'pdf.fonttype': 42,
    'ps.fonttype': 42,
    'text.usetex': False,
})
colors = sns.color_palette("tab10")
markers = {
    'ours': 'o',
    'minhash': 's',
    'maxloghash': '^'
}
linestyles = {
    'ours': '-',
    'minhash': '--',
    'maxloghash': ':'
}

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
numeric_cols = ['space(KB)', 'precision', 'insert-time', 'recall','f1-score']
for col in numeric_cols:
    df_minhash[col] = df_minhash[col].astype(float)
    df_maxloghash[col] = df_maxloghash[col].astype(float)
    df_user[col] = df_user[col].astype(float)

# 过滤用户数据中每组的最佳F1-score
group_keys = ['packet_size', 'entry_size', 'filter1_d', 'filter1_w', 'filter1_ct',
              'flow_id_size', 'simi_size', 'timestamp_size', 'filter2_main_num',
              'filter2_alter_num', 'cm_depth', 'cm_width', 'cm_ct']
df_user_filtered = df_user.loc[df_user.groupby(group_keys)['precision'].idxmax()]

# 在合并数据集后增加排序逻辑
df_combined = pd.concat([df_minhash, df_maxloghash, df_user_filtered])
df_combined = df_combined.sort_values(by='space(KB)')  # 全局排序


# 计算吞吐量（packets/sec）
df_combined['throughput'] = 10 / df_combined['insert-time']
fig, axes = plt.subplots(1, 4, figsize=(24, 6), sharey=False)

metric_names = ['precision', 'recall', 'f1-score', 'throughput']
titles = ['(a)Precision', '(b)Recall', '(c)F1-score', '(d)Throughput (Mpps)']

for idx, (ax, metric, title) in enumerate(zip(axes, metric_names, titles)):
    for i, (method, group) in enumerate(df_combined.groupby('method')):
        group_sorted = group.sort_values('space(KB)')
        ax.plot(group_sorted['space(KB)'], group_sorted[metric],
                label=method,
                marker=markers[method],
                linestyle=linestyles[method],
                linewidth=2,
                markersize=8,
                color=colors[i])
    ax.set_xlabel('Space (KB)', fontweight='bold')
    ax.set_ylabel(metric, fontweight='bold')
    ax.grid(True, linestyle='--', alpha=0.6)

    # 把小标题放在图下方
    ax.annotate(title,
                xy=(0.5, -0.35),
                xycoords='axes fraction',
                ha='center', va='center',
             fontweight='bold')

# 添加共享图例在上方
handles, labels = axes[0].get_legend_handles_labels()
fig.legend(handles, labels, loc='upper center', ncol=3, frameon=True,edgecolor='black',prop={'weight': 'bold'})

plt.tight_layout(rect=[0, 0, 1, 0.88])  # 给图例留出顶部空间
plt.savefig('fig/vs_baseline_IMC_new.pdf', bbox_inches='tight', facecolor='white')
plt.show()