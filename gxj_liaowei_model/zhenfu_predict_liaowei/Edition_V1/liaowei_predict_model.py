import pandas as pd


def liaowei_predict(liaowei_limit_upper, liaowei_limit_lower, time_span, slope, intercept, jinjiao_time_data,
                      Initial_liaowei, start_time, time_length, zhenfu_time_list):
    """
    料位预测模型: 判断当前组合的振幅时间列表是否合理并输出结果(1/0)、总偏差、料位列表
    :param liaowei_limit_upper, liaowei_limit_lower: 料位的最高及最低阈值
    :param time_span: 判断料位的间隔时间，单位为分钟
    :param slope,intercept: 线性回归模型斜率与截距 
    :param jinjiao_time_data: 进焦时间数据，元组类型，每个元素为含时间戳的元组 (('2025-04-07 00:00:00',),())
    :param Initial_liaowei: 料位初始值
    :param start_time: 预测开始时间
    :param time_length: 预测时间总长度,单位小时(h)
    :param zhenfu_time_list: 振幅与时间的对应关系，列表形式
    :return 1/0: 表示该振幅组合是否满足预测要求
    """

    ### 初始化
    # 整理进焦时间计划表
    try:
        # 将元组数据转换为 DataFrame
        timestamps = [timestamp[0] for timestamp in jinjiao_time_data]
        jinjiao_df = pd.DataFrame({'timestamp': timestamps})
        jinjiao_df['timestamp'] = pd.to_datetime(jinjiao_df['timestamp'], format='mixed')
        # 对数据按时间戳进行排序
        jinjiao_df = jinjiao_df.sort_values(by='timestamp')
    except Exception as e:
        print(f"处理进焦时间数据时出现错误: {e}")
        return None

    # 整理振幅时间表，计算每个振幅对应的结束时间点
    cumulative_durations = []   # 累积持续时间
    current_duration = 0
    for _, duration in zhenfu_time_list:
        current_duration += duration
        cumulative_durations.append(current_duration)
    
    # 划分时间间隔用于大循环，初始时间向后移动一个时间间隔，后包含原则（包含结束不包含开始）
    current_time = start_time + pd.Timedelta(minutes=time_span)
    liaowei = Initial_liaowei
    num_intervals = int(time_length * 60 / time_span)

    # 记录初始料位、初始化总偏差
    liaowei_list = [liaowei]
    total_deviation = 0


    ### 对每个时间间隔进行分析，包括进料、振幅影响的降低，记录料位具体值、与限定范围的偏差值
    for i in range(num_intervals):
        interval_start = current_time - pd.Timedelta(minutes=time_span)
        interval_end = current_time

        # 时间间隔判断前的料位值y1
        y1 = liaowei

        # 筛选出在当前时间间隔内的进料记录，大于 interval_start 且小于等于 interval_end
        filtered_df = jinjiao_df[(jinjiao_df['timestamp'] > interval_start) & (jinjiao_df['timestamp'] <= interval_end)]
        # 统计进料次数，即筛选后数据的行数
        feed_count = len(filtered_df)
        liaowei += feed_count * 0.7

        # 以结束时刻 interval_end 对应的振幅值进行计算
        elapsed_hours = (interval_end - start_time).total_seconds() / 3600 # 计算已经过了多少小时
        for j, cumulative_duration in enumerate(cumulative_durations):
            if elapsed_hours <= cumulative_duration:
                zhenfu = zhenfu_time_list[j][0]
                break
        else:
            zhenfu = zhenfu_time_list[-1][0]        # 考虑总经过时长大于设置时长的情况

        # 根据查询的振幅值计算当前的料位
        liaowei -= (zhenfu * slope + intercept) * time_span / 60
        y2 = liaowei

        # 计算偏差，可能出现的有种情况
        if (y1 - liaowei_limit_upper) * (y2 - liaowei_limit_upper) > 0 and y1 > liaowei_limit_upper:
            total_deviation += (y1 + y2 - 2 * liaowei_limit_upper) * time_span / 2
        elif (y1 - liaowei_limit_lower) * (y2 - liaowei_limit_lower) > 0 and y1 < liaowei_limit_lower:
            total_deviation += (2 * liaowei_limit_lower - (y1 + y2)) * time_span / 2
        elif y1 > liaowei_limit_upper >= y2:
            total_deviation += (y1 - liaowei_limit_upper) ** 2 * time_span / (2 * (y1 - y2))
        elif y1 < liaowei_limit_lower <= y2:
            total_deviation += (liaowei_limit_lower - y1) ** 2 * time_span / (2 * (y2 - y1))
        elif y1 <= liaowei_limit_upper < y2:
            total_deviation += (y2 - liaowei_limit_upper)  ** 2 * time_span / (2 * (y2 - y1)) 
        elif y1 >= liaowei_limit_lower > y2:
            total_deviation += (liaowei_limit_lower - y2)  ** 2 * time_span / (2 * (y1 - y2)) 

        # 记录当前时间间隔结束后的料位
        liaowei_list.append(liaowei)

        # 移动到下一个时间间隔
        current_time = current_time + pd.Timedelta(minutes=time_span)


    ### 判断并返回结果
    # 判断是否所有的点都在范围内
    if total_deviation > 0:
        return 0, total_deviation, liaowei_list
    
    return 1, total_deviation, liaowei_list
