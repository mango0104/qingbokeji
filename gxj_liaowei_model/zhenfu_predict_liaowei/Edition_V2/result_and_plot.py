from read_mysql_model import tjjh_time_mysql, real_liaowei_mysql
from liaowei_comparison_plot import liaowei_comparison_plot
from liaowei_predict_model_byReal import liaowei_predict_byReal
from zhenfu_comparison_plot import zhenfu_comparison_plot
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import pandas as pd

def result_and_plot(real_liaowei_data, start_time, time_length, time_span, liaowei_list, parameter, prediction):
    """
    函数作用: 绘制三个图形，最优及真实振幅下的真实与预测料位对比、最优及真实振幅对比
    param: real_liaowei_data: 真实数据
    param: start_time: 开始时间
    param: time_length: 时间总长度
    param: time_span: 时间间隔
    param: liaowei_list: 最优振幅下的预测料位列表
    param: parameter: 上传参数四部分：初始料位、开始时间、总时长、振幅时间列表
    param: prediction: 预测类实例
    return: 3x1的子图
    """
    # 规范开始时间格式，计算结束时间
    start_time = pd.to_datetime(start_time, format='mixed')

    # 创建一个3x1的子图布局
    fig, axes = plt.subplots(3, 1, figsize=(12, 18))

    # 绘制第一个图形，最优振幅下真实与预测料位对比
    liaowei_comparison_plot(real_liaowei_data, start_time, time_length, time_span, liaowei_list, axes[0])

    # 绘制第二个图形，真实振幅下真实与预测料位对比
    jinjiao_time_data = tjjh_time_mysql(start_time, time_length)
    real_liaowei_list = liaowei_predict_byReal(real_liaowei_data, jinjiao_time_data, start_time, time_length, time_span, prediction.slope, prediction.intercept)
    liaowei_comparison_plot(real_liaowei_data, start_time, time_length, time_span, real_liaowei_list, axes[1])

    # 绘制第三个图形，真实振幅与最优振幅对比
    zhenfu_comparison_plot(real_liaowei_data, start_time, time_length, time_span, parameter[3], axes[2])
    plt.tight_layout()
    plt.show()