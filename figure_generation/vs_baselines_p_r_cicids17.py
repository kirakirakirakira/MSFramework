import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
total_positives = 10
total_samples = 8278
total_negatives = total_samples - total_positives
plt.subplots_adjust(hspace=0.1)
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
10000000,20,20,272,8,32,32,32,10,5,200,1.0,0.6,0.75,134.65,11,0.5,0.9
10000000,20,60,272,8,32,32,32,30,15,200,0.8571,0.6,0.7059,113.31,34,0.5,0.9
10000000,20,100,272,8,32,32,32,50,25,200,0.75,0.9,0.8182,152.44,57,0.5,0.9
10000000,20,140,272,8,32,32,32,70,35,200,0.7273,0.8,0.7619,124.81,80,0.5,0.9
10000000,20,180,272,8,32,32,32,90,45,200,0.7273,0.8,0.7619,124.69,103,0.5,0.9
10000000,20,220,272,8,32,32,32,110,55,200,0.8333,1.0,0.9091,160.86,126,0.5,0.9
10000000,20,260,272,8,32,32,32,130,65,200,0.6667,0.8,0.7273,128.62,149,0.5,0.9
"""
df_minhash = pd.DataFrame([line.split(',') for line in minhash_data.strip().split('\n')], columns=columns_minhash)
df_minhash['method'] = 'minhash'

# 解析maxloghash数据
maxloghash_data = """
10000000,20,20,272,8,32,32,32,10,5,128,0.0926,1.0,0.1695,6.46,7,0.5,0.9
10000000,20,100,272,8,32,32,32,50,25,128,0.0168,1.0,0.033,7.3,36,0.5,0.9
10000000,20,120,272,8,32,32,32,60,30,128,0.0108,0.9,0.0213,8.29,43,0.5,0.9
10000000,20,200,272,8,32,32,32,100,50,128,0.0122,1.0,0.0241,7.24,72,0.5,0.9
10000000,20,240,272,8,32,32,32,120,60,128,0.0065,0.9,0.0129,8.98,87,0.5,0.9
10000000,20,300,272,8,32,32,32,150,75,128,0.008,1.0,0.0159,7.63,109,0.5,0.9
10000000,20,340,272,8,32,32,32,170,85,128,0.0071,1.0,0.0141,7.16,123,0.5,0.9
10000000,20,380,272,8,32,32,32,190,95,128,0.005,0.9,0.0099,9.5,138,0.5,0.9
10000000,20,420,272,8,32,32,32,210,105,128,0.0046,0.9,0.0092,8.59,152,0.5,0.9
"""
df_maxloghash = pd.DataFrame([line.split(',') for line in maxloghash_data.strip().split('\n')], columns=columns_maxloghash)
df_maxloghash['method'] = 'maxloghash'

# 解析用户数据并过滤最佳F1-score
user_data = """
10000000,20,200,272,8,32,32,32,100,50,1,272,16,1.0,1.0,1.0,21.35,136,0.5,0.7
10000000,20,180,272,8,32,32,32,90,40,1,272,16,0.9,0.9,0.9,17.02,119,0.5,0.7
10000000,20,160,272,8,32,32,32,80,40,1,272,16,0.9,0.9,0.9,16.09,108,0.5,0.7
10000000,20,140,272,8,32,32,32,60,30,1,272,16,0.9,0.9,0.9,15.14,87,0.5,0.7
10000000,20,120,272,8,32,32,32,50,25,1,272,16,0.8889,0.8,0.8421,13.73,73,0.5,0.7
10000000,20,100,272,8,32,32,32,40,20,1,272,16,1.0,1.0,1.0,15.83,59,0.5,0.7
10000000,20,80,272,8,32,32,32,30,15,1,272,16,0.9,0.9,0.9,15.24,46,0.5,0.7
10000000,20,60,272,8,32,32,32,20,10,1,272,16,0.8889,0.8,0.8421,11.99,32,0.5,0.7
10000000,20,40,272,8,32,32,32,15,7,1,272,16,1.0,0.9,0.9474,13.67,22,0.5,0.7
10000000,20,20,272,8,32,32,32,10,5,1,272,16,1.0,0.7,0.8235,12.74,13,0.5,0.7
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
fig, axes = plt.subplots(2, 4, figsize=(24, 10), sharey=False,
                         constrained_layout=True)

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
fig.legend(handles, labels,
           loc='upper center',
           bbox_to_anchor=(0.5, 1.08),  # 上浮
           ncol=3,
           frameon=True, edgecolor='black', prop={'weight': 'bold'})
# plt.tight_layout(rect=[0, 0.02, 1, 0.95])  # 留出上方空间给图例
plt.savefig('fig/vs_baseline_cicids17.pdf', bbox_inches='tight')
#plt.show()

# metrics_to_output = {
#     '(a) Precision': 'precision',
#     '(b) Recall': 'recall',
#     '(c) F1-score': 'f1-score',
#     '(d) Throughput': 'throughput',
#     '(e) FPR': 'FPR',
#     '(f) FNR': lambda df: 1 - df['recall'],
#     '(g) Accuracy': 'Accuracy',
#     '(h) MCC': 'MCC'
# }
#
# print("\n=== 每张图的原始数据点坐标 ===")
# for title, metric in metrics_to_output.items():
#     print(f"\n{title}")
#     for method, group in df_combined.groupby('method'):
#         group_sorted = group.sort_values('space(KB)')
#         x = group_sorted['space(KB)'].values
#         y = group_sorted[metric].values if not callable(metric) else metric(group_sorted).values
#         coords = [f"({xi:.2f}, {yi:.4f})" for xi, yi in zip(x, y)]
#         print(f"方法：{method}  " + "  ".join(coords))
