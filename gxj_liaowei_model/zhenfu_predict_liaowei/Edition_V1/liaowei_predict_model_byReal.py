import pandas as pd

def liaowei_predict_byReal(real_liaowei_data, jinjiao_time_data, start_time, time_length, time_span, slope, intercept):
    """
    根据实际数据预测料位值
    :param real_liaowei_data: 数据库中实时获取的时间戳、实际料位、振幅数据
    :param jinjiao_time_data: 数据库中的进焦时刻数据
    :param start_time: 预测开始时间
    :param time_length: 预测时间总长度，单位小时(h)
    :param time_span: 判断料位的间隔时间，单位为分钟
    :param slope, intercept: 线性回归模型斜率与截距
    :return: 预测料位列表
    """

    ### 数据整理及初始化
    # 修正开始时间格式并只保留分钟信息
    start_time = pd.to_datetime(start_time, format='mixed').floor('min')

    # 整理真实料位、振幅数据 real_liaowei_data
    real_timestamps = []
    real_liaowei_values = []
    real_zhenfu_values = []
    for timestamp, real_liaowei, zhenfu in real_liaowei_data:
        real_timestamps.append(pd.to_datetime(timestamp))
        real_liaowei_values.append(float(real_liaowei))
        real_zhenfu_values.append(float(zhenfu))
    real_df = pd.DataFrame({
        'timestamp': real_timestamps,
        'liaowei': real_liaowei_values,
        'zhenfu': real_zhenfu_values
    })

    # 获取初始物料值
    Initial_liaowei = real_liaowei_values[0]

    # 整理进焦时间计划表
    try:
        # 将元组数据转换为 DataFrame
        jinjiao_timestamps = [timestamp[0] for timestamp in jinjiao_time_data]
        jinjiao_df = pd.DataFrame({'timestamp': jinjiao_timestamps})
        jinjiao_df['timestamp'] = pd.to_datetime(jinjiao_df['timestamp'], format='mixed')
        # 对数据按时间戳进行排序
        jinjiao_df = jinjiao_df.sort_values(by='timestamp')
    except Exception as e:
        print(f"处理进焦时间数据时出现错误: {e}")
        return None

    # 划分时间间隔用于大循环，初始时间向后移动一个时间间隔，后包含原则（包含结束不包含开始）
    current_time = start_time + pd.Timedelta(minutes=time_span)
    liaowei = Initial_liaowei
    num_intervals = int(time_length * 60 / time_span)

    # 记录初始料位
    liaowei_list = [liaowei]


    ### 对每个时间间隔进行分析，包括进料、振幅的影响
    for i in range(num_intervals):
        interval_start = current_time - pd.Timedelta(minutes=time_span)
        interval_end = current_time

        # 筛选出在当前时间间隔内的进料记录，大于 interval_start 且小于等于 interval_end
        filtered_jinjiao_df = jinjiao_df[(jinjiao_df['timestamp'] > interval_start) & (jinjiao_df['timestamp'] <= interval_end)]
        # 统计当前时间间隔内的进料次数，即筛选后数据的行数
        feed_count = len(filtered_jinjiao_df)
        liaowei += feed_count * 0.7

        # 筛选出当前时间间隔内的实际数据
        interval_real_df = real_df[(real_df['timestamp'] > interval_start) & (real_df['timestamp'] <= interval_end)]
        if not interval_real_df.empty:
            # 计算平均振幅
            average_zhenfu = interval_real_df['zhenfu'].mean()
            # 根据平均振幅计算当前的料位
            liaowei -= (average_zhenfu * slope + intercept) * time_span / 60

        # 记录当前时间间隔结束后的料位
        liaowei_list.append(liaowei)

        # 移动到下一个时间间隔
        current_time = current_time + pd.Timedelta(minutes=time_span)

    return liaowei_list