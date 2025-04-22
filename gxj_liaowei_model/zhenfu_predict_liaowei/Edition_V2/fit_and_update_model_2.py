import read_mysql_model
from datetime import datetime, timedelta
import numpy as np
from sklearn.linear_model import LinearRegression
import subprocess
import pandas as pd
import os
import joblib
import matplotlib.pyplot as plt


def get_zero_time(current_time):
    """
    获取当前时间对应的0点时刻值
    """
    return current_time.replace(hour=0, minute=0, second=0, microsecond=0)


def get_data_list(jinjiao_time_data, real_data, step_size, time_window):
    """
    对数据进行分析, 更新zhenfu_list和liaowei_change_value_list , 用于线性模型拟合
    param: jinjiao_time_data: 进焦时间数据, 从数据库中获取得到,均为时间戳
    param: real_data: 数据库获取的真实数据，元组类型，每个元素为 (时间戳, 料位值, 振幅值)
    param: step_size: 步长,以多长的时间间隔进行滑动
    param: time_window: 每次分析所需的时间长度
    return: 振幅列表 zhenfu_list 及料位变化量列表 liaowei_change_value_list
    """

    # 解析数据，将元组中的时间戳转换为datetime对象
    jinjiao_time_data = [(datetime.strptime(data[0], '%Y-%m-%d %H:%M:%S'),) for data in jinjiao_time_data]
    real_data = [(datetime.strptime(data[0], '%Y-%m-%d %H:%M:%S'), float(data[1]), float(data[2])) for data in real_data]

    # 定义列表，分别存储振幅及相应料位的变化值
    zhenfu_list = []
    liaowei_change_value_list = []

    # 初始化开始时间及结束时间
    start_time = real_data[0][0]
    end_time = start_time + timedelta(hours=time_window)
    step = timedelta(hours=step_size)

    while end_time <= real_data[-1][0]:
        # 筛选出当前时间窗口内的数据
        current_real_data = [data for data in real_data if start_time <= data[0] <= end_time]
        current_jinjiao_time_data = [data for data in jinjiao_time_data if start_time <= data[0] <= end_time]

        if current_real_data:
            zhenfu_values = [data[2] for data in current_real_data]
            zhenfu_max_min_diff = max(zhenfu_values) - min(zhenfu_values)

            # 判断换皮带的情况及其他可能出现导致振幅值突变的异常情况
            if zhenfu_max_min_diff <= 3:
                # 计算振幅平均值
                zhenfu_avg = np.mean(zhenfu_values)

                # 计算料位变化值
                start_liaowei = current_real_data[0][1]
                end_liaowei = current_real_data[-1][1]
                feed_count = len(current_jinjiao_time_data)
                liaowei_change_value = (start_liaowei - end_liaowei + feed_count * 0.7) / time_window

                zhenfu_list.append(zhenfu_avg)
                liaowei_change_value_list.append(liaowei_change_value)

        # 滑动时间窗口
        start_time += step
        end_time += step

    return zhenfu_list, liaowei_change_value_list


def fit_linear_model(zhenfu_list, liaowei_change_value_list):
    """
    对zhenfu_list和liaowei_change_value_list进行线性模型拟合
    """
    if not zhenfu_list or not liaowei_change_value_list:
        return None, None

    try:
        # 线性回归的横纵坐标
        X = np.array(zhenfu_list).reshape(-1, 1)
        y = np.array(liaowei_change_value_list)

        # 初始化模型
        model = LinearRegression()

        # 训练模型
        model.fit(X, y)

        slope = model.coef_[0]
        intercept = model.intercept_
        
        # 打印斜率及截距
        print(f"斜率为： {slope}")
        print(f"截距为： {intercept}")

        # 保存模型到本地特定路径
        local_save_path = 'model.pkl'
        joblib.dump(model, local_save_path)
        print(f"模型已保存到本地 {local_save_path}")

        # 设置 GitHub 仓库路径
        github_repo = 'git clone ssh://git@111.15.165.82:2200/gitlab-instance-b03aeb89/jhzn_gxj_predict.git'
        repo_folder = 'jhzn_gxj_predict'

        # 克隆仓库（如果不存在）
        if not os.path.exists(repo_folder):
            subprocess.run(['git', 'clone', github_repo])

        # 将模型文件复制到仓库目录
        import shutil
        shutil.copy(local_save_path, os.path.join(repo_folder, local_save_path))

        # 进入仓库目录
        os.chdir(repo_folder)

        # 添加文件到暂存区
        subprocess.run(['git', 'add', local_save_path])

        # 提交更改
        subprocess.run(['git', 'commit', '-m', 'Update model.pkl'])

        # 推送更改到 GitHub
        subprocess.run(['git', 'push', 'origin', 'main'])

        print(f"模型已成功推送到 {github_repo}")

        # 绘制散点图及拟合曲线
        plt.scatter(X, y, color='blue', label='Data Points')
        plt.plot(X, model.predict(X), color='red', linewidth=2, label='Fitted Line')
        plt.xlabel('Amplitude')
        plt.ylabel('Level Change Value')
        plt.title('Linear Regression Fit')
        plt.legend()
        plt.show()

    except Exception as e:
        print(f"训练、保存或推送模型时出错: {e}")

    return slope, intercept


def main():
    # # 获取当前时间
    # current_time = datetime.now()
    current_time = pd.to_datetime('2025/4/17 08:00:00', format='mixed')
    
    # 获取当前时间对应的0点时刻值
    end_time = get_zero_time(current_time)

    # 初始化遍历数据范围及步长，time_length(使用多久的数据拟合模型)、step_size(滑动步长)、time_window(使用多久的数据获得一个数据点)
    time_length = 24 * 7
    step_size = 0.5
    time_window = 8

    # 获取数据
    start_time = end_time - timedelta(hours=time_length)
    jinjiao_time_data = read_mysql_model.tjjh_time_mysql(start_time, time_length)
    real_data = read_mysql_model.real_liaowei_mysql(start_time, time_length)

    # 分析数据
    zhenfu_list, liaowei_change_value_list = get_data_list(jinjiao_time_data, real_data, step_size, time_window)
    print(f"{len(zhenfu_list)}")
    # print(f"{zhenfu_list}")
    # print(f"{liaowei_change_value_list}")
    # 拟合线性模型
    slope, intercept = fit_linear_model(zhenfu_list, liaowei_change_value_list)

    # if slope is not None and intercept is not None:
    #     print(f"斜率: {slope}")
    #     print(f"截距: {intercept}")
    # else:
    #     print("数据不足，无法进行线性回归拟合。")


if __name__ == "__main__":
    main()