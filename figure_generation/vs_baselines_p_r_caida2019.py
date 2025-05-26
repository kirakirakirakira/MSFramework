import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

total_positives = 42
total_samples = 167074
total_negatives = total_samples - total_positives

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
10000000,20,20,272,8,32,4,10,10,5,200,0.5094,0.6429,0.5684,38.29,11,0.5,0.9
10000000,20,40,272,8,32,4,10,20,10,200,0.4416,0.8095,0.5715,36.23,22,0.5,0.9
10000000,20,60,272,8,32,4,10,30,15,200,0.375,0.7857,0.5077,37.13,34,0.5,0.9
10000000,20,80,272,8,32,4,10,40,20,200,0.37,0.881,0.5211,40.0,45,0.5,0.9
10000000,20,100,272,8,32,4,10,50,25,200,0.3302,0.8333,0.473,40.48,56,0.5,0.9
10000000,20,120,272,8,32,4,10,60,30,200,0.319,0.881,0.4684,42.02,68,0.5,0.9
10000000,20,140,272,8,32,4,10,70,35,200,0.2734,0.8333,0.4117,42.73,79,0.5,0.9
10000000,20,160,272,8,32,4,10,80,40,200,0.2606,0.881,0.4022,43.15,90,0.5,0.9
10000000,20,180,272,8,32,4,10,90,45,200,0.2517,0.881,0.3915,44.78,102,0.5,0.9
10000000,20,200,272,8,32,4,10,100,50,200,0.2574,0.8333,0.3933,45.42,113,0.5,0.9
10000000,20,220,272,8,32,4,10,110,55,200,0.269,0.9286,0.4172,53.91,124,0.5,0.9
10000000,20,240,272,8,32,4,10,120,60,200,0.2657,0.9048,0.4108,66.09,136,0.5,0.9
"""
df_minhash = pd.DataFrame([line.split(',') for line in minhash_data.strip().split('\n')], columns=columns_minhash)
df_minhash['method'] = 'minhash'

# 解析maxloghash数据
maxloghash_data = """
10000000,20,40,272,8,32,4,10,20,10,128,0.0538,0.9048,0.1016,27.45,14,0.5,0.9
10000000,20,60,272,8,32,4,10,30,15,128,0.0471,1.0,0.09,20.41,21,0.5,0.9
10000000,20,80,272,8,32,4,10,40,20,128,0.0371,0.9762,0.0715,20.99,28,0.5,0.9
10000000,20,100,272,8,32,4,10,50,25,128,0.0317,0.9762,0.0614,22.45,35,0.5,0.9
10000000,20,120,272,8,32,4,10,60,30,128,0.0299,1.0,0.0581,22.63,42,0.5,0.9
10000000,20,140,272,8,32,4,10,70,35,128,0.0276,1.0,0.0537,24.83,49,0.5,0.9
10000000,20,160,272,8,32,4,10,80,40,128,0.0254,1.0,0.0495,19.25,57,0.5,0.9
10000000,20,180,272,8,32,4,10,90,45,128,0.0226,1.0,0.0442,19.94,64,0.5,0.9
10000000,20,200,272,8,32,4,10,100,50,128,0.0205,0.9762,0.0402,19.48,71,0.5,0.9
10000000,20,220,272,8,32,4,10,110,55,128,0.0198,1.0,0.0388,18.87,78,0.5,0.9
10000000,20,240,272,8,32,4,10,120,60,128,0.0191,1.0,0.0375,19.48,85,0.5,0.9
10000000,20,260,272,8,32,4,10,130,65,128,0.0178,0.9762,0.035,18.79,92,0.5,0.9
10000000,20,280,272,8,32,4,10,140,70,128,0.0171,1.0,0.0336,19.33,99,0.5,0.9
10000000,20,300,272,8,32,4,10,150,75,128,0.0164,1.0,0.0323,19.46,106,0.5,0.9
10000000,20,320,272,8,32,4,10,160,80,128,0.016,1.0,0.0315,18.67,114,0.5,0.9
10000000,20,340,272,8,32,4,10,170,85,128,0.0153,1.0,0.0301,19.63,121,0.5,0.9
10000000,20,360,272,8,32,4,10,180,90,128,0.0146,1.0,0.0288,20.41,128,0.5,0.9
10000000,20,380,272,8,32,4,10,190,95,128,0.0144,1.0,0.0284,18.17,135,0.5,0.9
10000000,20,400,272,8,32,4,10,200,100,128,0.0137,1.0,0.027,19.83,142,0.5,0.9
"""
df_maxloghash = pd.DataFrame([line.split(',') for line in maxloghash_data.strip().split('\n')], columns=columns_maxloghash)
df_maxloghash['method'] = 'maxloghash'

# 解析用户数据并过滤最佳F1-score
user_data = """
10000000,20,20,272,8,32,4,10,10,5,1,272,16,1.0,0.2619,0.4151,19.05,13,0.5,0.4
10000000,20,40,272,8,32,4,10,20,10,1,272,16,0.9444,0.4048,0.5667,16.7,26,0.5,0.4
10000000,20,60,272,8,32,4,10,30,15,1,272,16,0.9143,0.7619,0.8312,16.82,40,0.5,0.4
10000000,20,80,272,8,32,4,10,40,20,1,272,16,0.9394,0.7381,0.8267,17.68,53,0.5,0.4
10000000,20,100,272,8,32,4,10,50,25,1,272,16,0.9268,0.9048,0.9157,18.47,67,0.5,0.4
10000000,20,120,272,8,32,4,10,60,30,1,272,16,0.8293,0.8095,0.8193,18.95,80,0.5,0.4
10000000,20,140,272,8,32,4,10,70,35,1,272,16,0.814,0.8333,0.8235,19.18,94,0.5,0.4
10000000,20,160,272,8,32,4,10,80,40,1,272,16,0.875,0.8333,0.8536,19.69,107,0.5,0.4
10000000,20,180,272,8,32,4,10,90,45,1,272,16,0.8974,0.8333,0.8642,19.34,121,0.5,0.4
10000000,20,200,272,8,32,4,10,100,50,1,272,16,0.8667,0.9286,0.8966,19.25,134,0.5,0.4
10000000,20,120,272,8,32,4,10,60,30,1,272,16,0.9444,0.8095,0.8718,18.74,80,0.5,0.5
10000000,20,140,272,8,32,4,10,70,35,1,272,16,0.9286,0.9286,0.9286,19.29,94,0.5,0.5
10000000,20,160,272,8,32,4,10,80,40,1,272,16,0.973,0.8571,0.9114,20.07,107,0.5,0.5
10000000,20,180,272,8,32,4,10,90,45,1,272,16,0.9444,0.8095,0.8718,22.82,121,0.5,0.5
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
df_combined['TP'] = df_combined['recall'] * total_positives
df_combined['FP'] = df_combined['TP'] / df_combined['precision'] - df_combined['TP']
df_combined['FPR'] = df_combined['FP'] / total_negatives
df_combined['FN'] = total_positives - df_combined['TP']
df_combined['Accuracy'] = 1 - (df_combined['FP'] + df_combined['FN']) / total_samples

df_combined['TN'] = total_negatives - df_combined['FP']

# 避免除零错误
denom = np.sqrt(
    (df_combined['TP'] + df_combined['FP']) *
    (df_combined['TP'] + df_combined['FN']) *
    (df_combined['TN'] + df_combined['FP']) *
    (df_combined['TN'] + df_combined['FN'])
)
df_combined['MCC'] = ((df_combined['TP'] * df_combined['TN']) - (df_combined['FP'] * df_combined['FN'])) / denom
df_combined['MCC'] = df_combined['MCC'].fillna(0)


# 设置子图 2 行 4 列
fig, axes = plt.subplots(2, 4, figsize=(24, 10), sharey=False)
metric_names = ['precision', 'recall', 'f1-score', 'throughput']
titles = ['(a) Precision', '(b) Recall', '(c) F1-score', '(d) Throughput ']

# 第一行：精度/召回率/F1/吞吐量
for idx, (ax, metric, title) in enumerate(zip(axes[0], metric_names, titles)):
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
    ax.set_ylabel(metric.capitalize(), fontweight='bold')
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.annotate(title,
                xy=(0.5, -0.35),
                xycoords='axes fraction',
                ha='center', va='center',
                fontweight='bold')

# 第二行第一个图：FPR
ax_fpr = axes[1][0]
for i, (method, group) in enumerate(df_combined.groupby('method')):
    group_sorted = group.sort_values('space(KB)')
    ax_fpr.plot(group_sorted['space(KB)'], group_sorted['FPR'],
                label=method,
                marker=markers[method],
                linestyle=linestyles[method],
                linewidth=2,
                markersize=8,
                color=colors[i])
ax_fpr.set_xlabel('Space (KB)', fontweight='bold')
ax_fpr.set_ylabel('FPR', fontweight='bold')
ax_fpr.grid(True, linestyle='--', alpha=0.6)
ax_fpr.annotate('(e) FPR', xy=(0.5, -0.35), xycoords='axes fraction',
                ha='center', va='center', fontweight='bold')

ax_fnr = axes[1][1]
for i, (method, group) in enumerate(df_combined.groupby('method')):
    group_sorted = group.sort_values('space(KB)')
    fnr_values = 1 - group_sorted['recall']
    ax_fnr.plot(group_sorted['space(KB)'], fnr_values,
                label=method,
                marker=markers[method],
                linestyle=linestyles[method],
                linewidth=2,
                markersize=8,
                color=colors[i])
ax_fnr.set_xlabel('Space (KB)', fontweight='bold')
ax_fnr.set_ylabel('FNR', fontweight='bold')
ax_fnr.grid(True, linestyle='--', alpha=0.6)
ax_fnr.annotate('(f) FNR', xy=(0.5, -0.35), xycoords='axes fraction',
                ha='center', va='center', fontweight='bold')


ax_acc = axes[1][2]
for i, (method, group) in enumerate(df_combined.groupby('method')):
    group_sorted = group.sort_values('space(KB)')
    ax_acc.plot(group_sorted['space(KB)'], group_sorted['Accuracy'],
                label=method,
                marker=markers[method],
                linestyle=linestyles[method],
                linewidth=2,
                markersize=8,
                color=colors[i])
ax_acc.set_xlabel('Space (KB)', fontweight='bold')
ax_acc.set_ylabel('Accuracy', fontweight='bold')
ax_acc.grid(True, linestyle='--', alpha=0.6)
ax_acc.annotate('(g) Accuracy', xy=(0.5, -0.35), xycoords='axes fraction',
                ha='center', va='center', fontweight='bold')

ax_mcc = axes[1][3]
for i, (method, group) in enumerate(df_combined.groupby('method')):
    group_sorted = group.sort_values('space(KB)')
    ax_mcc.plot(group_sorted['space(KB)'], group_sorted['MCC'],
                label=method,
                marker=markers[method],
                linestyle=linestyles[method],
                linewidth=2,
                markersize=8,
                color=colors[i])
ax_mcc.set_xlabel('Space (KB)', fontweight='bold')
ax_mcc.set_ylabel('MCC', fontweight='bold')
ax_mcc.grid(True, linestyle='--', alpha=0.6)
ax_mcc.annotate('(h) MCC', xy=(0.5, -0.35), xycoords='axes fraction',
                ha='center', va='center', fontweight='bold')



# 添加图例
handles, labels = axes[0][0].get_legend_handles_labels()
fig.legend(handles, labels, loc='upper center', ncol=3, frameon=True, edgecolor='black', prop={'weight': 'bold'})

plt.tight_layout(rect=[0, 0, 1, 0.9])  # 留出上方空间给图例
plt.savefig('fig/vs_baseline_new.pdf', bbox_inches='tight')
plt.show()