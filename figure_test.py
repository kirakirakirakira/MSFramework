import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import precision_recall_curve, roc_curve, auc

# 设置绘图风格
sns.set_style("whitegrid")

# 模拟数据（请替换为真实数据）
y_true = np.random.randint(0, 2, 1000)  # 真实标签（0-正常，1-异常）
y_scores = np.random.rand(1000)  # 预测得分（0-1之间）
thresholds = np.linspace(0, 1, 100)

precision, recall, _ = precision_recall_curve(y_true, y_scores)
fpr, tpr, _ = roc_curve(y_true, y_scores)
roc_auc = auc(fpr, tpr)

# 运行时间 vs. 数据规模
flow_counts = np.arange(1000, 11000, 1000)
run_times = np.log(flow_counts) + np.random.rand(len(flow_counts))  # 模拟时间数据

# 内存占用 vs. 数据规模
memory_usage = np.log(flow_counts) * 10 + np.random.rand(len(flow_counts))  # 模拟内存数据

# 误报率 vs. 检测时间
detection_time = np.linspace(0.1, 1.0, 10)
false_positive_rate = np.exp(-detection_time)  # 模拟误报率数据

# 开始绘图
fig, axs = plt.subplots(3, 3, figsize=(15, 12))

# (1) PR 曲线
axs[0, 0].plot(recall, precision, marker='o', label=f'PR Curve (AUC={auc(recall, precision):.2f})')
axs[0, 0].set_xlabel('Recall')
axs[0, 0].set_ylabel('Precision')
axs[0, 0].set_title('Precision-Recall Curve')
axs[0, 0].legend()

# (2) ROC 曲线
axs[0, 1].plot(fpr, tpr, marker='o', label=f'ROC Curve (AUC={roc_auc:.2f})')
axs[0, 1].plot([0, 1], [0, 1], 'k--')  # 随机分类器参考线
axs[0, 1].set_xlabel('False Positive Rate')
axs[0, 1].set_ylabel('True Positive Rate')
axs[0, 1].set_title('ROC Curve')
axs[0, 1].legend()

# (3) 运行时间 vs. 数据规模
axs[0, 2].plot(flow_counts, run_times, marker='o', linestyle='--', label='Run Time')
axs[0, 2].set_xlabel('Number of Flows')
axs[0, 2].set_ylabel('Time (s)')
axs[0, 2].set_title('Run Time vs. Data Scale')
axs[0, 2].legend()

# (4) 内存占用 vs. 数据规模
axs[1, 0].plot(flow_counts, memory_usage, marker='s', linestyle='--', color='g', label='Memory Usage')
axs[1, 0].set_xlabel('Number of Flows')
axs[1, 0].set_ylabel('Memory (MB)')
axs[1, 0].set_title('Memory Usage vs. Data Scale')
axs[1, 0].legend()

# (5) 误报率 vs. 检测时间
axs[1, 1].plot(detection_time, false_positive_rate, marker='d', linestyle='-', color='r', label='False Positive Rate')
axs[1, 1].set_xlabel('Detection Time (s)')
axs[1, 1].set_ylabel('False Positive Rate')
axs[1, 1].set_title('False Positive Rate vs. Detection Time')
axs[1, 1].legend()

# (6) 阈值 vs. 检测性能
axs[1, 2].plot(thresholds, np.sin(2*np.pi*thresholds), label='Precision', linestyle='--')
axs[1, 2].plot(thresholds, np.cos(2*np.pi*thresholds), label='Recall', linestyle='-.')
axs[1, 2].set_xlabel('Threshold')
axs[1, 2].set_ylabel('Metric Value')
axs[1, 2].set_title('Threshold vs. Precision/Recall')
axs[1, 2].legend()

# (7) 不同算法的检测性能对比
algorithms = ['Baseline', 'Method A', 'Method B', 'Your Method']
f1_scores = [0.75, 0.82, 0.85, 0.91]  # 假设你的方法最优
axs[2, 0].bar(algorithms, f1_scores, color=['gray', 'blue', 'purple', 'orange'])
axs[2, 0].set_xlabel('Algorithm')
axs[2, 0].set_ylabel('F1 Score')
axs[2, 0].set_title('Algorithm Performance Comparison')

# (8) 不同参数的影响
param_values = [10, 50, 100, 500, 1000]
performance = np.log(param_values) / 2  # 模拟性能数据
axs[2, 1].plot(param_values, performance, marker='o', linestyle='-', label='F1 Score')
axs[2, 1].set_xscale('log')
axs[2, 1].set_xlabel('Parameter Value')
axs[2, 1].set_ylabel('F1 Score')
axs[2, 1].set_title('Effect of Parameter Tuning')
axs[2, 1].legend()

# 调整布局
plt.tight_layout()
plt.show()
