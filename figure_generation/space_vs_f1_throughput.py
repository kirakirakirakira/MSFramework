import pandas as pd
import matplotlib.pyplot as plt

# 设置学术图表样式
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

# 原始数据
data = [
    [10000000, 20, 20, 272, 8, 32, 4, 10, 10, 5, 1, 272, 16, 1.0, 0.2619, 0.4151, 19.05, 13, 0.5, 0.4],
    [10000000, 20, 40, 272, 8, 32, 4, 10, 20, 10, 1, 272, 16, 0.9444, 0.4048, 0.5667, 16.7, 26, 0.5, 0.4],
    [10000000, 20, 60, 272, 8, 32, 4, 10, 30, 15, 1, 272, 16, 0.9143, 0.7619, 0.8312, 16.82, 40, 0.5, 0.4],
    [10000000, 20, 80, 272, 8, 32, 4, 10, 40, 20, 1, 272, 16, 0.9394, 0.7381, 0.8267, 17.68, 53, 0.5, 0.4],
    [10000000, 20, 100, 272, 8, 32, 4, 10, 50, 25, 1, 272, 16, 0.9268, 0.9048, 0.9157, 18.47, 67, 0.5, 0.4],
    [10000000, 20, 120, 272, 8, 32, 4, 10, 60, 30, 1, 272, 16, 0.9444, 0.8095, 0.8718, 18.74, 80, 0.5, 0.5],
    [10000000, 20, 140, 272, 8, 32, 4, 10, 70, 35, 1, 272, 16, 0.9286, 0.9286, 0.9286, 19.29, 94, 0.5, 0.5],
    [10000000, 20, 160, 272, 8, 32, 4, 10, 80, 40, 1, 272, 16, 0.973, 0.8571, 0.9114, 20.07, 107, 0.5, 0.5]
]

columns = [
    "packet_size", "entry_size", "filter1_d", "filter1_w", "filter1_ct", "flow_id_size",
    "simi_size", "timestamp_size", "filter2_main_num", "filter2_alter_num", "cm_depth",
    "cm_width", "cm_ct", "precision", "recall", "f1-score", "insert-time", "space(KB)",
    "filter1_threshold", "filter2_threshold"
]

df = pd.DataFrame(data, columns=columns)

# 数据预处理
df['throughput'] = 10 / df['insert-time']  # 计算吞吐量
df_sorted = df.sort_values('space(KB)')  # 按存储空间排序

# 创建画布
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5), dpi=300)
plt.subplots_adjust(wspace=0.3)  # 子图间距

# ===== 左图：存储空间 vs F1-Score =====
ax1.plot(df_sorted['space(KB)'], df_sorted['f1-score'],
         marker='o', color='#2ca02c', linewidth=2,
         markersize=8, markeredgewidth=1.5)

ax1.set_xlabel('Memory Usage (KB)', fontweight='bold')
ax1.set_ylabel('F1-Score', fontweight='bold')
ax1.set_title('F1-Score vs Memory', fontweight='bold', pad=15)
ax1.grid(True, linestyle=':', alpha=0.6)


# ===== 右图：存储空间 vs 吞吐量 =====
ax2.plot(df_sorted['space(KB)'], df_sorted['throughput'],
         marker='s', color='#d62728', linewidth=2,
         markersize=8, markeredgewidth=1.5)

ax2.set_xlabel('Memory Usage (KB)', fontweight='bold')
ax2.set_ylabel('Throughput (Mpps)', fontweight='bold')
ax2.set_title('Throughput vs Memory', fontweight='bold', pad=15)
ax2.grid(True, linestyle=':', alpha=0.6)

# ===== 统一坐标轴范围 =====
for ax in [ax1, ax2]:
    ax.set_xlim(10, 110)
    ax.set_xticks(range(20, 120, 20))
    ax.tick_params(axis='both', width=1.5)

ax1.set_ylim(0.4, 1.0)
ax2.set_ylim(0.4, 0.6)

# 保存输出
plt.tight_layout()
plt.savefig('memory_vs_f1_throughput.png',
            bbox_inches='tight',
            facecolor='white')
plt.show()