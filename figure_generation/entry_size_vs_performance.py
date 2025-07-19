import pandas as pd
import matplotlib.pyplot as plt
import os

# 设置风格（统一学术论文风格）
plt.rcParams.update({
    'font.size': 18,
    'axes.titlesize': 30,
    'axes.labelsize': 30,
    'xtick.labelsize': 30,
    'ytick.labelsize': 30,
    'legend.fontsize': 26,
    'font.family': 'Times New Roman',
    'pdf.fonttype': 42,
    'ps.fonttype': 42,
    'text.usetex': False,
})

# 创建保存路径
os.makedirs('fig', exist_ok=True)

# 原始数据
data='''
10000000,8,96,272,8,32,4,10,50,25,1,272,16,1.0,0.7273,0.8421,12.82,66,0.5,0.5
10000000,20,100,272,8,32,4,10,50,25,1,272,16,1.0,0.7576,0.8621,12.99,67,0.5,0.5
10000000,25,100,272,8,32,4,10,50,25,1,272,16,1.0,0.7273,0.8421,13.54,67,0.5,0.5
10000000,50,100,272,8,32,4,10,50,25,1,272,16,0.9787,0.697,0.8142,13.6,67,0.5,0.5
10000000,100,100,272,8,32,4,10,50,25,1,272,16,0.9792,0.7121,0.8246,16.2,67,0.5,0.5
'''
columns = [
    "packet_size", "entry_size", "filter1_d", "filter1_w", "filter1_ct", "flow_id_size",
    "simi_size", "timestamp_size", "filter2_main_num", "filter2_alter_num", "cm_depth",
    "cm_width", "cm_ct", "precision", "recall", "f1-score", "insert-time", "space(KB)",
    "filter1_threshold", "filter2_threshold"
]
df = pd.DataFrame([line.split(',') for line in data.strip().split('\n')], columns=columns)
#df = pd.DataFrame(data, columns=columns)
numeric_cols = ['entry_size', 'precision', 'recall', 'f1-score', 'insert-time']
df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric)
df_sorted = df.sort_values('entry_size')
grouped = df_sorted.groupby('entry_size').agg({
    'precision': 'first',
    'recall': 'first',
    'f1-score': 'first',
    'insert-time': 'mean'
}).reset_index()
grouped['throughput'] = 10 / grouped['insert-time']

# 风格参数
line_config = {'linewidth': 2.5, 'markersize': 7, 'markeredgewidth': 1.5}
colors = {
    'precision': '#1f77b4',
    'recall': '#d62728',
    'f1-score': '#2ca02c',
    'throughput': '#9467bd'
}
markers = {
    'precision': '^',
    'recall': 's',
    'f1-score': 'o',
    'throughput': 'D'
}

# 创建子图
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), dpi=300)

# --- 左图：Precision / Recall / F1 ---
for metric in ['precision', 'recall', 'f1-score']:
    ax1.plot(grouped['entry_size'], grouped[metric],
             marker=markers[metric],
             color=colors[metric],
             label=metric.replace('-', ' ').title(),
             **line_config)

ax1.set_xlabel('Number of cells', fontweight='bold')
ax1.set_ylabel('Score', fontweight='bold')
ax1.set_xlim(0, 110)
ax1.set_xticks(range(0, 111, 20))
ax1.set_ylim(0.3, 1.0)
ax1.grid(True, linestyle=':', alpha=0.6)
ax1.set_title('(a) P, R, F1 vs number of cells', fontweight='bold', y=-0.35)

# 图例只显示在左图，放在图内左上角
ax1.legend(loc='lower right',
           frameon=True,
           framealpha=0.95,
           edgecolor='black',
           prop={"weight":"bold"})

# --- 右图：Throughput ---
bar_colors = "#4682b4"
bar_edge_color = 'black'

# --- 右图：Throughput（使用类目轴）---
entry_labels = grouped['entry_size'].astype(str)  # 把 entry_size 转为字符串作为分类标签

ax2.bar(entry_labels, grouped['throughput'],
        color=bar_colors,
        edgecolor=bar_edge_color,
        linewidth=1.2,
        width=0.6)  # 控制柱宽，更细致地调整美观度

# 可选：在柱子上显示吞吐量数值
# for x, y in zip(entry_labels, grouped['throughput']):
#     ax2.text(x, y + 0.005, f'{y:.2f}', ha='center', va='bottom', fontsize=20)

ax2.set_xlabel('Number of cells', fontweight='bold')
ax2.set_ylabel('Throughput (Mpps)', fontweight='bold')
ax2.grid(True, linestyle=':', alpha=0.6, axis='y')  # 只加横线网格
ax2.set_title('(b) Throughput vs number of cells', fontweight='bold', y=-0.35)


# 紧凑排版
plt.tight_layout()
plt.savefig('fig/entry_size_performance.pdf', bbox_inches='tight', facecolor='white')
plt.show()
