import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

def plot_scatter_and_fit(history_file_path):
    """
    根据历史数据拟合预测曲线
    """
    try:
        history_df = pd.read_excel(history_file_path)
        filtered_history_df = history_df[(history_df['zhenfu'] >= 23) & (history_df['zhenfu'] <= 34) &
                                         (history_df['hight_change'] >= 2.5) & (history_df['hight_change'] <= 4.3)]
        
        X = filtered_history_df['zhenfu'].values.reshape(-1, 1)
        y = filtered_history_df['hight_change'].values

        model = LinearRegression()
        model.fit(X, y)

        slope = model.coef_[0]
        intercept = model.intercept_
        print(f"拟合曲线的斜率为: {slope}")
        print(f"拟合曲线的截距为: {intercept}")

        return slope, intercept
    
    except FileNotFoundError:
        print(f"错误: 文件 {history_file_path} 未找到。")
        return None, None
    