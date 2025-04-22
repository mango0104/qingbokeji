import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# 1. 读取历史数据文档、绘制散点图、拟合曲线
def plot_scatter_and_fit(history_file_path):

    try:
        history_df = pd.read_excel(history_file_path)
        
        # 筛选数据
        filtered_history_df = history_df[(history_df['zhenfu'] >= 23) & (history_df['zhenfu'] <= 34) &
                        (history_df['hight_change'] >= 2.5) & (history_df['hight_change'] <= 4.3)]

        # 准备数据用于线性回归
        X = filtered_history_df['zhenfu'].values.reshape(-1, 1)
        y = filtered_history_df['hight_change'].values

        # 创建并拟合线性回归模型
        model = LinearRegression()
        model.fit(X, y)

        # 获取斜率和截距
        slope = model.coef_[0]
        intercept = model.intercept_
        print(f"拟合曲线的斜率为: {slope}")
        print(f"拟合曲线的截距为: {intercept}")

        # # 预测并绘制拟合直线
        # x_fit = np.linspace(X.min(), X.max(), 100).reshape(-1, 1)
        # y_fit = model.predict(x_fit)

        # # 绘制散点图和拟合直线
        # plt.scatter(filtered_history_df['zhenfu'], filtered_history_df['hight_change'], label='Data Points')
        # plt.plot(x_fit, y_fit, color='red', label='Fitted Line')
        # plt.xlabel('zhenfu')
        # plt.ylabel('hight_change')
        # plt.title('Scatter Plot of zhenfu vs hight_change with Fitted Line')
        # plt.legend()
        # plt.show()

        # 返回预测好的线性模型
        return model, slope, intercept
    
    except FileNotFoundError:
        print(f"错误: 文件 {history_file_path} 未找到。")
        return None  # 文件未找到时返回 None


# 2. 读取待预测数据文档并进行数据处理
def process_predict_excel(predict_file_path, Initial_liaowei, start_time, end_time, time_span, slope, intercept):
    """
    读取待预测数据文档并进行数据处理
    :param predict_file_path: 待预测数据的文件路径
    :param Initial_liaowei: 料位初始值
    :param start_time: 预测开始时间
    :param end_time: 预测结束时间
    :param slope,intercept: 线性回归模型斜率与截距 
    :return filtered_predict_df: 更新后的表格
    """

    try:
        predict_df = pd.read_excel(predict_file_path)

        # 将时间戳列转换为 datetime 类型
        predict_df['timestamp'] = pd.to_datetime(predict_df['timestamp'], format='mixed')

        # 筛选出指定时间范围内的数据
        filtered_predict_df = predict_df[(predict_df['timestamp'] >= start_time) & (predict_df['timestamp'] <= end_time)]

        # 初始化物料值
        liaowei = Initial_liaowei
        predict_liaowei = []
        last_update_time = start_time

        for i in range(len(filtered_predict_df)):
            # 判断是否进料，是则 +0.7
            if i > 0: 
                if (filtered_predict_df.iloc[i]['jinjiao_1'] == 1) & (filtered_predict_df.iloc[i-1]['jinjiao_1'] == 0):
                    liaowei += 0.7

            # 每 time_span 分钟判断更新一次物料高度
            current_time = filtered_predict_df.iloc[i]['timestamp']
            time_diff = (current_time - last_update_time).total_seconds()
            if time_diff >= (time_span * 60):
                zhenfu = int(filtered_predict_df.iloc[i]['zhenfu'])
                update_liaowei = slope * zhenfu + intercept
                liaowei -= (update_liaowei / 60) * time_span
                last_update_time = current_time

            predict_liaowei.append(liaowei)
        
        # # 判断 predict_liaowei 列是否存在，如果存在则删除
        # if 'predict_liaowei' in predict_df.columns:
        #     predict_df.drop(columns=['predict_liaowei'], inplace=True)
        #     print(predict_df.columns)
        
        # 添加新的 predict_liaowei 列
        predict_df.loc[filtered_predict_df.index, 'predict_liaowei'] = predict_liaowei
        # print(predict_df.columns)

        # 更新待预测表格
        predict_df.update(filtered_predict_df)
        predict_df.to_excel(predict_file_path, index=False)

        return predict_df
    
    except FileNotFoundError:
        print(f"错误: 文件 {predict_file_path} 未找到。")
        return None

# 3. 绘制趋势图
def plot_trend(predict_df, start_time, end_time, time_span):
    if predict_df is not None and not predict_df.empty:
        predict_df_temp = predict_df[(predict_df['timestamp'] >= start_time) & (predict_df['timestamp'] <= end_time)]
        filtered = predict_df_temp[((predict_df_temp['timestamp'] - start_time).dt.total_seconds() % (time_span * 60)) == 0]
        if not filtered.empty:
            if 'predict_liaowei' in filtered.columns and 'liaowei' in filtered.columns:
                plt.plot(filtered['timestamp'], filtered['liaowei'], label='liaowei')
                plt.plot(filtered['timestamp'], filtered['predict_liaowei'], label='predict_liaowei')
                plt.xlabel('Time')
                plt.ylabel('Value')
                plt.title('Trend Plot')
                plt.legend()
                plt.xticks(rotation=45)
                plt.show()
            else:
                print("'predict_liaowei' 或 'liaowei' 列不存在于筛选后的数据中。")
                print("筛选后的数据列名:", filtered.columns)

if __name__ == "__main__":
    Initial_liaowei = 26.90  # 初始料位设定值
    history_file_path =  r'C:\Users\Administrator\Desktop\liaowei_and_zhenfu.xlsx'
    predict_file_path = r'C:\Users\Administrator\Desktop\predict_data.xlsx'
    start_time = pd.to_datetime('2025/4/2 0:00:00', format='mixed')
    end_time = pd.to_datetime('2025/4/3 12:30:00', format='mixed')
    time_span = 10 # 设定绘制点的时间间隔

    # 调用绘图和拟合函数，得到拟合好的模型
    model, slope, intercept = plot_scatter_and_fit(history_file_path)
    if (slope != None) & (intercept != None):
        predict_df = process_predict_excel(predict_file_path, Initial_liaowei, start_time, end_time, time_span, slope, intercept)
        plot_trend(predict_df, start_time, end_time, time_span)
