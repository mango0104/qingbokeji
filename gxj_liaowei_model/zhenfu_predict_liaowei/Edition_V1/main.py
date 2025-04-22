from liaowei_predict_result import Prediction
from read_mysql_model import real_liaowei_mysql
from result_and_plot import result_and_plot

# 创建 Prediction 类的实例
prediction = Prediction()

# 示例参数
# parameter = [28.25, '2025/4/7 02:00:00', 8, [(32, 2), (31, 5), (30, 1), (31, 2)]]
parameter = [28.21, '2025/4/13 08:00:00', 10, [(30, 1.5), (29, 1), (30, 2.5), (29, 2.5), (30, 2.5)]]


# 调用 predict_result 方法
result, total_deviation, liaowei_list = prediction.predict_result(parameter)
print(f"推理结果: {result}")
print(f"总偏差: {total_deviation}")

# # 绘制对比曲线查看效果
real_liaowei_data = real_liaowei_mysql()

# 绘制三图
result_and_plot(real_liaowei_data, '2025/4/13 08:00:00', 10, 1, liaowei_list, parameter, prediction)

