import pandas as pd
import matplotlib.pyplot as plt
from datetime import timedelta


def liaowei_comparison_plot(real_liaowei_data, start_time, time_length, time_span, liaowei_list, ax):
    """
    预测与真实料位对比曲线
    :param real_liaowei_data: 真实料位数据，元组类型，每个元素为 (时间戳, 料位值)
    :param start_time: 预测开始时间
    :param time_length: 预测总时间长度
    :param time_span: 预测时间间隔
    :param liaowei_list: 预测料位列表
    """
    try:
        # 将元组数据转换为 DataFrame
        timestamps = [pd.to_datetime(item[0]) for item in real_liaowei_data]
        real_liaowei_values = [float(item[1]) for item in real_liaowei_data]
        df = pd.DataFrame({
            'timestamp': timestamps,
            'liaowei': real_liaowei_values
        })
        real_liaowei = [real_liaowei_values[0]]
        selected_timestamps = [timestamps[0]]

        # 修正开始时间格式并只保留分钟信息
        start_time = pd.to_datetime(start_time, format='mixed').floor('min')

        # 按 time_span 分钟进行分组并计算平均值
        df['interval'] = df['timestamp'].apply(
            lambda x: (x - start_time).total_seconds() // (time_span * 60))
        df = df.groupby('interval').agg({'timestamp': 'min', 'liaowei': 'mean'}).reset_index()

        # 筛选出从开始时间起每 time_span 分钟的数据
        current_time = start_time
        end_time = start_time + pd.Timedelta(hours=time_length)
        interval = 0
        while current_time <= end_time:
            mask = df['interval'] == interval
            if any(mask):
                real_liaowei.append(df.loc[mask, 'liaowei'].values[0])
                selected_timestamps.append(df.loc[mask, 'timestamp'].values[0])
            current_time += timedelta(minutes=time_span)
            interval += 1

        # 确保数据长度一致
        min_len = min(len(liaowei_list), len(real_liaowei))
        liaowei_list = liaowei_list[:min_len]
        real_liaowei = real_liaowei[:min_len]
        selected_timestamps = selected_timestamps[:min_len]

        # print(f"对比最小长度: {min_len}")

        # 创建 DataFrame
        data = {
            'timestamp': selected_timestamps,
            'predict_line': liaowei_list,
            'real_line': real_liaowei
        }
        df_new = pd.DataFrame(data)

        # 绘制曲线

            
        # plt.figure(figsize=(12, 6))
        # plt.plot(df_new['timestamp'], df_new['predict_line'],
        #          label='predict_line', marker='o', color='black')
        # plt.plot(df_new['timestamp'], df_new['real_line'],
        #          label='real_line', marker='o', color='red')

        # plt.xlabel('Time')
        # plt.ylabel('Liaowei Value')
        # plt.title('Liaowei Comparison')
        # plt.legend()
        # plt.grid(True)
        # plt.xticks(rotation=45)
        # plt.tight_layout()
        # plt.show()

        # ax.plot(df_new['timestamp'], df_new['predict_line'],
        #         label='predict_line', marker='o', color='black')
        # ax.plot(df_new['timestamp'], df_new['real_line'],
        #         label='real_line', marker='o', color='red')
        ax.plot(df_new['timestamp'], df_new['predict_line'],
                label='predict_line', color='black')
        ax.plot(df_new['timestamp'], df_new['real_line'],
                label='real_line', color='red')

        ax.set_xlabel('Time')
        ax.set_ylabel('Liaowei Value')
        ax.set_title('Liaowei Comparison')
        ax.legend()
        ax.grid(True)
        ax.tick_params(axis='x', rotation=45)

    except Exception as e:
        print(f"发生错误: {e}")
    return ax



def liaowei_predict_plot(start_time, time_length, time_span, liaowei_list):
    """
    预测料位曲线
    :param start_time: 预测开始时间
    :param time_length: 预测总时间长度
    :param time_span: 预测时间间隔
    :param liaowei_list: 预测料位列表
    """
    # 修正开始时间格式并只保留分钟信息
    start_time = pd.to_datetime(start_time, format='mixed').floor('min')
    end_time = start_time + pd.Timedelta(hours=time_length)

    # 初始化时间列表
    timestamps_list = [start_time]
    current_time = start_time + timedelta(minutes=time_span)
    while current_time <= end_time:
        timestamps_list.append(current_time)
        current_time = current_time + timedelta(minutes=time_span)
                
    # 确保两个列表长度一致
    min_len = min(len(timestamps_list), len(liaowei_list))
    timestamps_list = timestamps_list[:min_len]
    liaowei_list = liaowei_list[:min_len]

    # 创建DataFrame（可选，便于后续操作）
    data = {
        'timestamp': timestamps_list,
        'liaowei': liaowei_list
    }
    df = pd.DataFrame(data)

    # 绘制曲线
    plt.figure(figsize=(12, 6))
    plt.plot(df['timestamp'], df['liaowei'], label='Predicted Liaowei', marker='o', color='blue')

    plt.xlabel('Time')
    plt.ylabel('Liaowei Value')
    plt.title('Predicted Liaowei Curve')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()