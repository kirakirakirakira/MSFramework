import pandas as pd
import matplotlib.pyplot as plt
import os

# 设置学术图表样式
plt.rcParams.update({
    'font.size': 18,
    'axes.titlesize': 30,
    'axes.labelsize': 30,
    'xtick.labelsize': 30,
    'ytick.labelsize': 30,
    'legend.fontsize': 30,
    'font.family': 'Times New Roman',
    'pdf.fonttype': 42,
    'ps.fonttype': 42,
    'text.usetex': False,
})

# 创建保存路径
os.makedirs('fig', exist_ok=True)

# 原始数据
# data = [
#     [10000000, 20, 20, 272, 8, 32, 4, 10, 10, 5, 1, 272, 16, 1.0, 0.2619, 0.4151, 19.05, 13, 0.5, 0.4],
#     [10000000, 20, 40, 272, 8, 32, 4, 10, 20, 10, 1, 272, 16, 0.9444, 0.4048, 0.5667, 16.7, 26, 0.5, 0.4],
#     [10000000, 20, 60, 272, 8, 32, 4, 10, 30, 15, 1, 272, 16, 0.9143, 0.7619, 0.8312, 16.82, 40, 0.5, 0.4],
#     [10000000, 20, 80, 272, 8, 32, 4, 10, 40, 20, 1, 272, 16, 0.9394, 0.7381, 0.8267, 17.68, 53, 0.5, 0.4],
#     [10000000, 20, 100, 272, 8, 32, 4, 10, 50, 25, 1, 272, 16, 0.9268, 0.9048, 0.9157, 18.47, 67, 0.5, 0.4],
#     [10000000, 20, 120, 272, 8, 32, 4, 10, 60, 30, 1, 272, 16, 0.9444, 0.8095, 0.8718, 18.74, 80, 0.5, 0.5],
#     [10000000, 20, 140, 272, 8, 32, 4, 10, 70, 35, 1, 272, 16, 0.9286, 0.9286, 0.9286, 19.29, 94, 0.5, 0.5],
#     [10000000, 20, 160, 272, 8, 32, 4, 10, 80, 40, 1, 272, 16, 0.973, 0.8571, 0.9114, 20.07, 107, 0.5, 0.5]
# ]
data='''
10000000,20,20,272,8,32,4,10,10,5,3,272,16,1.0,0.1905,0.32,19.04,29,0.5,0.5
10000000,20,40,272,8,32,4,10,20,10,3,272,16,0.9565,0.5238,0.6769,19.74,58,0.5,0.5
10000000,20,60,272,8,32,4,10,30,15,3,272,16,0.96,0.5714,0.7164,19.71,88,0.5,0.5
10000000,20,80,272,8,32,4,10,40,20,3,272,16,0.9394,0.7381,0.8267,20.32,117,0.5,0.5
10000000,20,100,272,8,32,4,10,50,25,3,272,16,0.9394,0.7381,0.8267,21.17,146,0.5,0.5
10000000,20,120,272,8,32,4,10,60,30,3,272,16,0.9444,0.8095,0.8718,21.87,176,0.5,0.5
10000000,20,140,272,8,32,4,10,70,35,3,272,16,0.9459,0.8333,0.886,22.44,205,0.5,0.5'''
columns = [
    "packet_size", "entry_size", "filter1_d", "filter1_w", "filter1_ct", "flow_id_size",
    "simi_size", "timestamp_size", "filter2_main_num", "filter2_alter_num", "cm_depth",
    "cm_width", "cm_ct", "precision", "recall", "f1-score", "insert-time", "space(KB)",
    "filter1_threshold", "filter2_threshold"
]

#df = pd.DataFrame(data, columns=columns)
df = pd.DataFrame([line.split(',') for line in data.strip().split('\n')], columns=columns)
#df = pd.DataFrame(data, columns=columns)
numeric_cols = ['space(KB)', 'precision', 'recall', 'f1-score', 'insert-time']
df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric)
# 数据预处理
df['throughput'] = 10 / df['insert-time']
df_sorted = df.sort_values('space(KB)')

# 创建画布
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6.5), dpi=300)
plt.subplots_adjust(wspace=0.3)

# ===== 左图：P/R/F1 =====
ax1.plot(df_sorted['space(KB)'], df_sorted['f1-score'],
         marker='o', color='#2ca02c', linewidth=2,
         markersize=8, markeredgewidth=1.5, label='F1-Score',linestyle='-.')

ax1.plot(df_sorted['space(KB)'], df_sorted['precision'],
         marker='^', color='#1f77b4', linewidth=2,
         markersize=7, markeredgewidth=1.5, label='Precision',linestyle='--')

ax1.plot(df_sorted['space(KB)'], df_sorted['recall'],
         marker='s', color='#ff7f0e', linewidth=2,
         markersize=7, markeredgewidth=1.5, label='Recall')

ax1.set_xlabel('Memory Usage (KB)', fontweight='bold')
ax1.set_ylabel('Score', fontweight='bold')
ax1.set_title('(a) P, R, F1 vs Memory', fontweight='bold', y=-0.3)
ax1.grid(True, linestyle=':', alpha=0.6)

# 仅左图显示 legend
ax1.legend(loc='lower right', frameon=True, edgecolor='black', framealpha=0.95,prop={'weight':'bold'})

# ===== 右图：吞吐量 =====
ax2.plot(df_sorted['space(KB)'], df_sorted['throughput'],
         marker='s', color='#d62728', linewidth=2,
         markersize=8, markeredgewidth=1.5,linestyle="--")

ax2.set_xlabel('Memory Usage (KB)', fontweight='bold')
ax2.set_ylabel('Throughput (Mpps)', fontweight='bold')
ax2.set_title('(b) Throughput vs Memory', fontweight='bold', y=-0.3)
ax2.grid(True, linestyle=':', alpha=0.6)

# ===== 坐标范围设置 =====
for ax in [ax1, ax2]:
    ax.set_xlim(10, 210)
    ax.set_xticks(range(20, 220, 40))
    ax.tick_params(axis='both', width=1.5)

ax1.set_ylim(0.1, 1.0)
ax2.set_ylim(0.4, 0.55)

# 保存图像
plt.tight_layout()
plt.savefig('fig/memory_vs_f1_throughput.pdf', bbox_inches='tight', facecolor='white')
# plt.show()
