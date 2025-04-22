"""
该 .py 文件用于判断不同振幅下的料位变化值
即根据 横坐标振幅, 带入拟合曲线, 计算纵坐标料位变化
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from scipy.stats import linregress


def plot_scatter_and_fit():
    history_file_path =  r'C:\Users\Administrator\Desktop\liaowei_and_zhenfu.xlsx'
    try:
        history_df = pd.read_excel(history_file_path)

        # 筛选数据
        filtered_df = history_df[(history_df['zhenfu_int'] >= 23) & (history_df['zhenfu_int'] <= 34) &
                                 (history_df['hight_change'] >= 2.5) & (history_df['hight_change_xin'] <= 4.3)]

        # 准备数据用于线性回归
        X = filtered_df['zhenfu_int'].values.reshape(-1, 1)
        y = filtered_df['hight_change_xin'].values

        # 创建并拟合线性回归模型
        model = LinearRegression()
        model.fit(X, y)

        # 获取斜率和截距
        slope = model.coef_[0]
        intercept = model.intercept_
        print(f"拟合曲线的斜率为: {slope}")         # 0.09329
        print(f"拟合曲线的截距为: {intercept}")     # 0.49383

        # 预测并绘制拟合直线
        x_fit = np.linspace(X.min(), X.max(), 100).reshape(-1, 1)
        y_fit = model.predict(x_fit)

        # # 绘制散点图和拟合直线
        # plt.scatter(filtered_df['zhenfu_int'], filtered_df['hight_change_xin'], label='Data Points')
        # plt.plot(x_fit, y_fit, color='red', label='Fitted Line')
        # plt.xlabel('zhenfu_int')
        # plt.ylabel('hight_change_xin')
        # plt.title('Scatter Plot of zhenfu_int vs hight_change_xin with Fitted Line')
        # plt.legend()
        # plt.show()

        return model, slope, intercept  # 返回拟合好的模型

    except FileNotFoundError:
        print(f"错误: 文件 {history_file_path} 未找到。")
        return None  # 文件未找到时返回 None

def predict_y_on_fit_curve(model, x_value):
    """
    根据拟合的线性回归模型，预测给定横坐标对应的纵坐标
    :param model: 拟合好的线性回归模型
    :param x_value: 输入的横坐标值
    :return: 对应的纵坐标预测值
    """
    x_pred = np.array([[x_value]])
    y_pred = model.predict(x_pred)
    return y_pred[0]


if __name__ == "__main__":
    # 调用绘图和拟合函数，得到拟合好的模型
    model, slope, intercept = plot_scatter_and_fit()
    if model:
        # 示例输入的横坐标值
        input_x = 35
        predicted_y = predict_y_on_fit_curve(model, input_x)
        print(f"当横坐标为 {input_x} 时，对应的纵坐标为: {predicted_y}")
    