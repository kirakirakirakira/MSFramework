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
# 数据准备
data = [
    [10000000,100,100,272,8,32,4,10,50,25,1,272,16,0.9677,0.7143,0.8219,36.61,67,0.5,0.5],
    [10000000,100,100,272,8,32,4,10,50,25,1,272,16,0.9642,0.6428,0.7714,36.52,67,0.5,0.6],
    [10000000,100,100,272,8,32,4,10,50,25,1,272,16,1.0,0.6429,0.7826,39.83,67,0.5,0.7],
    [10000000,100,100,272,8,32,4,10,50,25,1,272,16,0.8462,0.7857,0.8148,46.34,67,0.5,0.3],
    [10000000,100,100,272,8,32,4,10,50,25,1,272,16,0.9667,0.6905,0.8056,35.56,67,0.5,0.5],
    [10000000,100,100,272,8,32,4,10,50,25,1,272,16,0.9062,0.6905,0.7838,40.55,67,0.5,0.4],
    [10000000,100,100,272,8,32,4,10,50,25,1,272,16,0.9091,0.9524,0.9302,35.45,67,0.5,0.4],
    [10000000,100,100,272,8,32,4,10,50,25,1,272,16,0.881,0.881,0.881,37.19,67,0.5,0.4]
]

columns = [
    "packet_size", "entry_size", "filter1_d", "filter1_w", "filter1_ct", "flow_id_size",
    "simi_size", "timestamp_size", "filter2_main_num", "filter2_alter_num", "cm_depth",
    "cm_width", "cm_ct", "precision", "recall", "f1-score", "insert-time", "space(KB)",
    "filter1_threshold", "filter2_threshold"
]

df = pd.DataFrame(data, columns=columns)
df = df.rename(columns={'filter2_threshold': 'threshold for promotion'})
df_grouped = df.groupby('threshold for promotion').agg({
    'precision': 'first',
    'recall': 'first',
    'f1-score': 'first'
}).reset_index().sort_values('threshold for promotion')

# 创建画布（调整尺寸和DPI）
plt.figure(figsize=(12, 5), dpi=300)  # 增大DPI到300

# 绘制三条折线（加粗线条）
line_styles = {
    'precision': {'marker': '^', 'ls': '--', 'color': '#1f77b4', 'label': 'Precision', 'lw': 2},
    'recall': {'marker': 's', 'ls': '-.', 'color': '#d62728', 'label': 'Recall', 'lw': 2},
    'f1-score': {'marker': 'o', 'ls': '-', 'color': '#2ca02c', 'label': 'F1-Score', 'lw': 3}
}

for metric, style in line_styles.items():
    plt.plot(df_grouped['threshold for promotion'],
             df_grouped[metric],
             marker=style['marker'],
             linestyle=style['ls'],
             linewidth=style['lw'],
             markersize=9,  # 增大标记尺寸
             color=style['color'],
             markeredgewidth=1.5,
             label=style['label'])

# 坐标轴设置
plt.xticks(df_grouped['threshold for promotion'], fontweight='bold')
plt.yticks(fontweight='bold')
plt.xlabel("Promotion Threshold", labelpad=10,fontweight='bold')
plt.ylabel("Score",labelpad=10,fontweight='bold')

# 图表修饰
plt.grid(axis='both', linestyle=':', alpha=0.4)
plt.ylim(0.6, 1.02)
plt.xlim(0.25, 0.75)
plt.title("Performance Metrics vs Promotion Threshold",
           pad=15, fontweight='bold')

# 图例设置
legend = plt.legend(loc='upper right',
                  frameon=True,
                  framealpha=0.95,
                  edgecolor='black',
                  title='Metrics:',
                  )
legend.get_frame().set_linewidth(1.5)  # 加粗图例边框

# 保存与显示
plt.tight_layout()
plt.savefig('fig\\threshold_vs_f1.pdf',   # 保存为矢量图
           bbox_inches='tight',
           dpi=300,
           facecolor='white')  # 确保白色背景    
plt.show()
