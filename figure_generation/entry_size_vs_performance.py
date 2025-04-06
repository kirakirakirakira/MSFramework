import pandas as pd
import matplotlib.pyplot as plt
# 设置全局学术论文样式
plt.rcParams.update({
    'font.size': 12,
    'axes.titlesize': 14,
    'axes.labelsize': 13,
    'xtick.labelsize': 12,
    'ytick.labelsize': 12,
    'legend.fontsize': 12,
    'font.family': 'serif',
    'pdf.fonttype': 42
})
# Data provided
data = [
    [10000000,10,100,272,8,32,4,10,50,25,1,272,16,0.8649,0.7619,0.8101,14.01,67,0.5,0.4],
    [10000000,4,100,272,8,32,4,10,50,25,1,272,16,0.8684,0.7857,0.825,11.73,67,0.5,0.4],
    [10000000,8,104,272,8,32,4,10,50,25,1,272,16,0.878,0.8571,0.8674,13.93,68,0.5,0.4],
    [10000000,4,100,272,8,32,4,10,50,25,1,272,16,0.8684,0.7857,0.825,11.56,67,0.5,0.4],
    [10000000,20,100,272,8,32,4,10,50,25,1,272,16,0.9118,0.7381,0.8158,18.91,67,0.5,0.4],
    [10000000,33,99,272,8,32,4,10,50,25,1,272,16,0.9487,0.881,0.9136,24.42,66,0.5,0.4],
    [10000000,50,100,272,8,32,4,10,50,25,1,272,16,0.9302,0.9524,0.9412,44.44,67,0.5,0.4],
    [10000000,100,100,272,8,32,4,10,50,25,1,272,16,0.9091,0.9524,0.9302,35.45,67,0.5,0.4]
]

columns = [
    "packet_size", "entry_size", "filter1_d", "filter1_w", "filter1_ct", "flow_id_size",
    "simi_size", "timestamp_size", "filter2_main_num", "filter2_alter_num", "cm_depth",
    "cm_width", "cm_ct", "precision", "recall", "f1-score", "insert-time", "space(KB)",
    "filter1_threshold", "filter2_threshold"
]

df = pd.DataFrame(data, columns=columns)
df_sorted = df.sort_values('entry_size')
grouped = df_sorted.groupby('entry_size').agg({
    'precision': 'first',
    'recall': 'first',
    'f1-score': 'first',
    'insert-time': 'mean'
}).reset_index()
grouped['throughput'] = 10 / grouped['insert-time']  # 计算吞吐量

# 创建画布（适应双栏论文布局）
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5), dpi=300)
plt.subplots_adjust(wspace=0.25)  # 子图间距

# ========== 左图：精度/召回/F1 ==========
line_config = {
    'linewidth': 2,
    'markersize': 8,
    'markeredgewidth': 1.5
}

# 精度曲线
ax1.plot(grouped['entry_size'], grouped['precision'],
         marker='^', color='#1f77b4', label='Precision', **line_config)

# 召回曲线
ax1.plot(grouped['entry_size'], grouped['recall'],
         marker='s', color='#d62728', label='Recall', **line_config)

# F1曲线
ax1.plot(grouped['entry_size'], grouped['f1-score'],
         marker='o', color='#2ca02c', label='F1-Score', **line_config)

ax1.set_xlabel('Entry Size', fontweight='bold', labelpad=10)
ax1.set_ylabel('Score', fontweight='bold', labelpad=10)
ax1.set_title('Entry size vs P, R, F1', fontweight='bold', pad=15)
ax1.grid(True, linestyle=':', alpha=0.6)

# ========== 右图：吞吐量 ==========
ax2.plot(grouped['entry_size'], grouped['throughput'],
         marker='D', color='#9467bd', linewidth=2,
         markersize=8, markeredgewidth=1.5)

ax2.set_xlabel('Entry Size', fontweight='bold', labelpad=10)
ax2.set_ylabel('Throughput (Mpps)', fontweight='bold', labelpad=10)
ax2.set_title('Entry size vs Throughput', fontweight='bold', pad=15)
ax2.grid(True, linestyle=':', alpha=0.6)

# ========== 统一样式设置 ==========
for ax in [ax1, ax2]:
    ax.set_xlim(0, 110)
    ax.set_xticks(range(0, 110, 20))
    ax.tick_params(axis='both', width=1.5)

# 优化图例
ax1.legend(loc='upper left',
          frameon=True,
          framealpha=0.95,
          edgecolor='black',
          bbox_to_anchor=(0.02, 0.98))

# 保存输出
plt.tight_layout()
plt.savefig('entry_size_performance',
           bbox_inches='tight',
           facecolor='white',
           dpi=300)

plt.show()