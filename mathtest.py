
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
def memory_size_test(data):
    filter1_d = data['filter1_d']
    filter1_w = data['filter1_w']
    filter1_ct = data['filter1_ct']
    flow_id_size = data['flow_id_size']
    simi_size = data['simi_size']
    timestamp_size = data['timestamp_size']
    filter2_main_num = data['filter2_main_num']
    filter2_alter_num = data['filter2_alter_num']
    cm_depth = data['cm_depth']
    cm_width = data['cm_width']
    cm_ct = data['cm_ct']
    #filter1总空间大小
    filter1_total_size=filter1_d*filter1_w*filter1_ct+filter1_d*flow_id_size+filter1_d*simi_size
    #filter2 space
    filter2_total_size=(filter2_main_num+filter2_alter_num)*((cm_depth*cm_width*cm_ct)+(flow_id_size+simi_size+timestamp_size))
    total_bit=filter1_total_size+filter2_total_size
    total_KB=total_bit/8//1024
    print("共占用%dKB"%total_KB)

def exp_result():
    data={
    "packet_size":10000000,
    'filter1_d': 100,
    'filter1_w': 272,
    'filter1_ct': 8,
    'flow_id_size': 32,
    'simi_size': 4,
    'timestamp_size': 10,
    'filter2_main_num': 50,
    'filter2_alter_num': 25,
    'cm_depth': 1,
    'cm_width': 272,
    'cm_ct': 16,
    'precision':0.9677,
    'recall':0.7143,
    'f1-score':0.8219,
    'insert-time':36.61,
    'space(KB)':67,
    'filter1_threshold':0.5,
    'filter2_threshold':0.5
    }
    return data

def save_to_csv(data):
    df = pd.DataFrame([data])
    df.to_csv('experiment_result.csv',mode='a', header=False, index=False)


def get_figure_space_and_f1():
    file_path = "experiment_result.csv"  # 替换为你的 CSV 文件路径
    df = pd.read_csv(file_path)
    df_sorted = df.sort_values(by="space(KB)")

    # 提取排序后的数据
    space_kb = df_sorted["space(KB)"]
    f1_score = df_sorted["f1-score"]

    # 绘制折线图
    plt.figure(figsize=(8, 6))
    plt.plot(space_kb, f1_score, marker='o', linestyle='-', color='b', label='Data Points')

    # 添加标签和标题
    plt.xlabel("Space (KB)")
    plt.ylabel("F1-Score")
    plt.title("Relationship between Space Usage and F1-Score")
    plt.legend()
    plt.grid(True)

    # 显示图像
    plt.show()


def get_figure_throughput():
    file_path = "experiment_result.csv"  # 替换为你的 CSV 文件路径
    df = pd.read_csv(file_path)
    # 计算吞吐量（单位：Mpps）
    df['throughput(Mpps)'] = (df['packet_size'] / df['insert-time']) / 1e6

    # 按空间大小排序数据
    df_sorted = df.sort_values('space(KB)')

    # 绘制图表
    plt.figure(figsize=(10, 6))
    plt.plot(df_sorted['space(KB)'], df_sorted['throughput(Mpps)'],
             marker='o', linestyle='-', linewidth=1.5, markersize=8, color='b')
    plt.title('Throughput vs. Space', fontsize=14)
    plt.xlabel('Space (KB)', fontsize=12)
    plt.ylabel('Throughput (Mpps)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)

    # 标注数据点
    for i, row in df_sorted.iterrows():
        plt.text(row['space(KB)'], row['throughput(Mpps)'],
                 f"({row['space(KB)']}KB, {row['throughput(Mpps)']:.2f}Mpps)",
                 fontsize=9, ha='left', va='bottom')

    plt.tight_layout()
    plt.show()


def get_figure_p_r_f1_score():
    file_path = "experiment_result.csv"  # 替换为你的 CSV 文件路径
    df = pd.read_csv(file_path)
    df_sorted = df.sort_values('space(KB)')
    plt.figure(figsize=(12, 6))
    plt.plot(df_sorted['space(KB)'], df_sorted['precision'], marker='o', label='Precision')
    plt.plot(df_sorted['space(KB)'], df_sorted['recall'], marker='s', label='Recall')
    plt.plot(df_sorted['space(KB)'], df_sorted['f1-score'], marker='^', label='F1-score')
    plt.xlabel('Space (KB)')
    plt.ylabel('Score')
    plt.title('Precision/Recall/F1-score vs. Space')
    plt.legend()
    plt.grid(True)
    plt.show()

def get_figure_throughput_f1():
    file_path = "experiment_result.csv"  # 替换为你的 CSV 文件路径
    df = pd.read_csv(file_path)

    # 计算吞吐量（Mpps）
    df['throughput(Mpps)'] = (df['packet_size'] / df['insert-time']) / 1e6

    # 按吞吐量排序数据
    df_sorted = df.sort_values('throughput(Mpps)')

    # 绘制折线图
    plt.figure(figsize=(10, 6))
    plt.plot(
        df_sorted['throughput(Mpps)'],
        df_sorted['f1-score'],
        marker='o',
        linestyle='--',
        linewidth=2,
        markersize=8,
        color='purple'
    )
    plt.title('F1-score vs. Throughput', fontsize=14)
    plt.xlabel('Throughput (Million Packets per Second, Mpps)', fontsize=12)
    plt.ylabel('F1-score', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)

    # 标注关键参数（例如filter1_d）
    for i, row in df_sorted.iterrows():
        plt.text(
            row['throughput(Mpps)'],
            row['f1-score'] + 0.02,  # 避免文字重叠
            f"filter1_d={row['filter1_d']}\nspace={row['space(KB)']}KB",
            fontsize=8,
            ha='center',
            va='bottom'
        )

    plt.tight_layout()
    plt.show()

def get_figure_f1_threshold_2():
    file_path = "experiment_result.csv"  # 替换为你的 CSV 文件路径
    df = pd.read_csv(file_path)

    # 筛选其他参数相同的组（以 filter1_d=100 的配置为基准）
    base_condition = (
            (df['filter1_d'] == 100) &
            (df['filter2_main_num'] == 50) &
            (df['filter2_alter_num'] == 25) &
            (df['cm_depth'] == 1) &
            (df['cm_width'] == 272) &
            (df['cm_ct'] == 16) &
            (df['filter1_threshold'] == 0.5)
    )

    filtered_df = df[base_condition].sort_values('filter2_threshold')

    # 绘制关系图
    plt.figure(figsize=(8, 5))
    plt.plot(filtered_df['filter2_threshold'], filtered_df['f1-score'],
             marker='o', linestyle='--', color='tab:blue')
    plt.xlabel('threshold for part 2', fontsize=12)
    plt.ylabel('F1-score', fontsize=12)
    plt.title('threshold for part 2 vs. F1-score', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.show()
if __name__=="__main__":
    temp_data=exp_result()
    memory_size_test(temp_data)
    # save_to_csv(temp_data)
    #get_figure_throughput_f1()
    get_figure_f1_threshold_2()

