import pandas as pd
import matplotlib.pyplot as plt


# 设置学术图表样式
plt.rcParams.update({
    'font.size': 18,
    'axes.titlesize': 22,
    'axes.labelsize': 18,
    'xtick.labelsize': 16,
    'ytick.labelsize': 16,
    'legend.fontsize': 20,
    'font.family': 'Times New Roman',
    'pdf.fonttype': 42,
    'ps.fonttype': 42,
    'text.usetex': False,
})

# 原始数据
data = [[10000000,20,20,272,8,32,4,10,10,5,1,272,16,1.0,0.2143,0.353,17.74,13,0.5,0.5],
    [10000000,20,40,272,8,32,4,10,20,10,1,272,16,0.9545,0.5,0.6562,17.38,26,0.5,0.5],
    [10000000,20,60,272,8,32,4,10,30,15,1,272,16,0.963,0.619,0.7536,17.25,40,0.5,0.5],
    [10000000,20,80,272,8,32,4,10,40,20,1,272,16,0.9394,0.7381,0.8267,17.31,53,0.5,0.5],
    [10000000,20,100,272,8,32,4,10,50,25,1,272,16,0.9429,0.7857,0.8572,17.89,67,0.5,0.5],
    [10000000,20,120,272,8,32,4,10,60,30,1,272,16,0.9737,0.881,0.925,17.99,80,0.5,0.5],
    [10000000,20,140,272,8,32,4,10,70,35,1,272,16,0.95,0.9048,0.9268,18.41,94,0.5,0.5],
    [10000000,20,160,272,8,32,4,10,80,40,1,272,16,0.9459,0.8333,0.886,19.17,107,0.5,0.5],
    [10000000,20,180,272,8,32,4,10,90,45,1,272,16,0.9459,0.8333,0.886,19.66,121,0.5,0.5],
    [10000000,20,200,272,8,32,4,10,100,50,1,272,16,0.9459,0.8333,0.886,20.28,134,0.5,0.5],
    [10000000,20,20,272,8,32,4,10,10,5,2,272,16,1.0,0.2143,0.353,18.45,21,0.5,0.5],
    [10000000,20,40,272,8,32,4,10,20,10,2,272,16,0.9545,0.5,0.6562,18.46,42,0.5,0.5],
    [10000000,20,60,272,8,32,4,10,30,15,2,272,16,0.9655,0.6667,0.7887,18.43,64,0.5,0.5],
    [10000000,20,80,272,8,32,4,10,40,20,2,272,16,0.9231,0.8571,0.8889,18.97,85,0.5,0.5],
    [10000000,20,100,272,8,32,4,10,50,25,2,272,16,0.9459,0.8333,0.886,19.58,107,0.5,0.5],
    [10000000,20,120,272,8,32,4,10,60,30,2,272,16,0.9412,0.7619,0.8421,20.06,128,0.5,0.5],
    [10000000,20,140,272,8,32,4,10,70,35,2,272,16,0.9412,0.7619,0.8421,20.45,149,0.5,0.5],
    [10000000,20,20,272,8,32,4,10,10,5,3,272,16,1.0,0.1905,0.32,19.04,29,0.5,0.5],
    [10000000,20,40,272,8,32,4,10,20,10,3,272,16,0.9565,0.5238,0.6769,19.74,58,0.5,0.5],
    [10000000,20,60,272,8,32,4,10,30,15,3,272,16,0.96,0.5714,0.7164,19.71,88,0.5,0.5],
    [10000000,20,80,272,8,32,4,10,40,20,3,272,16,0.9394,0.7381,0.8267,20.32,117,0.5,0.5],
    [10000000,20,100,272,8,32,4,10,50,25,3,272,16,0.9394,0.7381,0.8267,21.17,146,0.5,0.5],
    ]  # 此处粘贴用户提供的完整数据

columns = [
    'packet_size', 'entry_size', 'filter1_d', 'filter1_w', 'filter1_ct', 'flow_id_size', 'simi_size', 'timestamp_size',
    'filter2_main_num', 'filter2_alter_num', 'cm_depth', 'cm_width', 'cm_ct', 'precision', 'recall', 'f1-score',
    'insert-time', 'space(KB)', 'filter1_threshold', 'filter2_threshold'
]



df = pd.DataFrame(data, columns=columns)
df = df[['cm_depth', 'space(KB)', 'f1-score', 'precision', 'recall']].astype(float)
df.sort_values(['cm_depth', 'space(KB)'], inplace=True)

# 样式设置
depth_colors = {1: '#1f77b4', 2: '#2ca02c', 3: '#d62728'}
markers = {1: 'o', 2: 's', 3: '^'}
linestyles = {1: '--', 2: '-.', 3: '-'}

# 绘图函数（横排三个子图 + 上方图例）
def plot_metrics_vs_depth(df, metrics, ylabels, filename):
    fig, axs = plt.subplots(1, 3, figsize=(18, 6), dpi=300, sharey=False)

    for idx, (metric, ylabel) in enumerate(zip(metrics, ylabels)):
        ax = axs[idx]
        for depth, group in df.groupby('cm_depth'):
            ax.plot(group['space(KB)'], group[metric],
                    label=f'Depth={int(depth)}',
                    color=depth_colors[depth],
                    marker=markers[depth],
                    linestyle=linestyles[depth],
                    linewidth=2.5,
                    markersize=7)

        ax.set_xlabel("Memory (KB)", fontweight='bold')
        ax.set_ylabel(ylabel, fontweight='bold')
        ax.grid(True, linestyle=':', alpha=0.5)
        ax.set_xlim(0, 150)
        ax.set_xticks(range(0, 151, 30))

        if metric == 'f1-score':
            ax.set_ylim(0.3, 1.0)
        elif metric == 'precision':
            ax.set_ylim(0.9, 1.0)
        else:
            ax.set_ylim(0, 1.0)

        ax.set_title(f"({chr(97+idx)}) {ylabel}", fontweight='bold', y=-0.35)

    # 图例统一放在上方
    handles, labels = axs[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper center', ncol=len(depth_colors),
               frameon=True, edgecolor='black', fontsize=16, prop={'weight': 'bold'})

    plt.tight_layout(rect=[0, 0, 1, 0.93])
    plt.savefig(f'fig/{filename}.pdf', bbox_inches='tight', facecolor='white')
    plt.show()

# 调用函数
plot_metrics_vs_depth(df,
                      ['precision', 'recall','f1-score'],
                      ['Precision', 'Recall','F1-score'],
                      'metrics_vs_memory_diff_depth')
