"""
用于绘制真实振幅与最优振幅的对比图
"""
import pandas as pd

def zhenfu_comparison_plot(real_liaowei_data, start_time, time_length, time_span, zhenfu_time_list, ax):
        
    # 将元组数据转换为 DataFrame
    timestamps = [pd.to_datetime(item[0]) for item in real_liaowei_data]
    real_zhenfu_values = [float(item[2]) for item in real_liaowei_data]
    real_df = pd.DataFrame({
        'timestamp': timestamps,
        'zhenfu': real_zhenfu_values
    })

    Initial_real_zhenfu = real_zhenfu_values[0]

    # 修正开始时间格式并只保留分钟信息
    start_time = pd.to_datetime(start_time, format='mixed').floor('min')

    # 整理振幅时间表，计算每个振幅对应的结束时间点
    cumulative_durations = []   # 累积持续时间
    current_duration = 0
    for _, duration in zhenfu_time_list:
        current_duration += duration
        cumulative_durations.append(current_duration)

    # 划分时间间隔用于大循环，初始时间向后移动一个时间间隔，后包含原则（包含结束不包含开始）
    current_time = start_time + pd.Timedelta(minutes=time_span)
    num_intervals = int(time_length * 60 / time_span)

    timestamp_list = [start_time]
    real_zhenfu_list = [Initial_real_zhenfu]
    optimal_zhenfu_list = [zhenfu_time_list[0][0]]

    for i in range(num_intervals):
        interval_start = current_time - pd.Timedelta(minutes=time_span)
        interval_end = current_time

        # 记录 real_liaowei_data 中的振幅值
        interval_real_df = real_df[(real_df['timestamp'] > interval_start) & (real_df['timestamp'] <= interval_end)]
        if not interval_real_df.empty:
            # 计算平均振幅
            average_zhenfu = interval_real_df['zhenfu'].mean()
        else:
            # 如果该时间间隔内没有数据，使用上一个振幅值
            average_zhenfu = real_zhenfu_list[-1]

        real_zhenfu_list.append(average_zhenfu)


        # 记录 zhenfu_time_list 中的振幅值
        elapsed_hours = (interval_end - start_time).total_seconds() / 3600 # 计算已经过了多少小时
        for j, cumulative_duration in enumerate(cumulative_durations):
            if elapsed_hours <= cumulative_duration:
                optimal_zhenfu = zhenfu_time_list[j][0]
                break
        else:
            optimal_zhenfu = zhenfu_time_list[-1][0]        # 考虑总经过时长大于设置时长的情况
        
        optimal_zhenfu_list.append(optimal_zhenfu)
        timestamp_list.append(current_time)
        
        # 移动到下一个时间间隔
        current_time = current_time + pd.Timedelta(minutes=time_span)

    
    # 绘制图形
    ax.plot(timestamp_list, optimal_zhenfu_list, label='Optimal Amplitude', marker='o', color='black')
    ax.plot(timestamp_list, real_zhenfu_list, label='Real Amplitude', marker='o', color='red')
    ax.set_xlabel('Time')
    ax.set_ylabel('Amplitude')
    ax.set_title('Comparison of Real and Optimal Amplitudes')
    ax.legend()
    ax.grid(True)
    ax.tick_params(axis='x', rotation=45)

    return ax
