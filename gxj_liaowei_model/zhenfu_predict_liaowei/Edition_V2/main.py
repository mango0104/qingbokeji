from liaowei_predict_result import Prediction
from read_mysql_model import real_liaowei_mysql, tjjh_time_mysql
from result_and_plot import result_and_plot
from liaowei_predict_model_byReal import liaowei_predict_byReal
from liaowei_comparison_plot import liaowei_comparison_plot
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt

# 创建 Prediction 类的实例
prediction = Prediction()

# 示例参数
start_time = '2025/4/13 08:00:00'
time_length = 10
# 参数示例
parameter = [28.21, start_time, time_length, [(32, 1.5), (31, 1), (32, 2.5), (31, 2.5), (32, 2.5)]]

# # 示例参数
# start_time = '2025/4/17 04:00:00'
# time_length = 10
# # 参数示例
# parameter = [27.78, start_time, time_length, [(31, 3), (32, 3.5), (31, 1.5), (32, 2)]]

# 调用 predict_result 方法
result, total_deviation, liaowei_list = prediction.predict_result(parameter)
print(f"推理结果: {result}")
print(f"总偏差: {total_deviation}")
print(f"预测料位长度: {len(liaowei_list)}")

# # 绘制对比曲线查看效果
real_liaowei_data = real_liaowei_mysql(start_time, time_length)

# 绘制三图
result_and_plot(real_liaowei_data, start_time, time_length, 1, liaowei_list, parameter, prediction)

############################

# real_liaowei_data = real_liaowei_mysql(start_time, time_length)

# time_span = 1
# fig, axes = plt.subplots()

# jinjiao_time_data = tjjh_time_mysql(start_time, time_length)
# real_liaowei_list = liaowei_predict_byReal(real_liaowei_data, jinjiao_time_data, start_time, time_length, time_span, prediction.slope, prediction.intercept)
# print(f"预测料位长度: {len(real_liaowei_list)}")
# liaowei_comparison_plot(real_liaowei_data, start_time, time_length, time_span, real_liaowei_list, axes)
# plt.tight_layout()
# plt.show()