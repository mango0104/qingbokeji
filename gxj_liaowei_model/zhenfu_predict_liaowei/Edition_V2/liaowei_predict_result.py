# 功能：执行料位预测功能，获得当前振幅组合的料位预测结果，定义一个 预测类  Prediction， 具体包含
# 初始化: __init__ : 料位上限、料位下限、判断料位时间间隔、加载拟合曲线预测模型（获取斜率截距）、数据库中读取的进焦计划数据
# 预测函数: predict : 传入判断所有参数，初始料位、开始时间、判断总时长、振幅与持续时间列表
# 预测结果函数: predict_result : 用来给出最终结果（0/1），总偏差total_deviation, 预测料位列表liaowei_list,传入参数为上述四个的列表形式

import pandas as pd
import joblib
import subprocess
import os
from datetime import timedelta
from liaowei_predict_model import liaowei_predict
from liaowei_comparison_plot import liaowei_comparison_plot
from read_mysql_model import tjjh_time_mysql, real_liaowei_mysql

class Prediction:
    def __init__(self, liaowei_limit_upper=32, liaowei_limit_lower=25, time_span=1,  
                 github_repo='ssh://git@111.15.165.82:2200/gitlab-instance-b03aeb89/jhzn_gxj_predict.git', repo_folder='jhzn_gxj_predict'):
        self.liaowei_limit_upper = liaowei_limit_upper
        self.liaowei_limit_lower = liaowei_limit_lower
        self.time_span = time_span

        # 克隆 GitHub 仓库（如果不存在）
        if not os.path.exists(repo_folder):
            subprocess.run(['git', 'clone', github_repo])

        # 加载模型
        model_path = os.path.join(repo_folder, 'model.pkl') 
        model = joblib.load(model_path)

        # 获取斜率和截距
        self.slope = model.coef_[0]
        self.intercept = model.intercept_

    def predict(self, jinjiao_time_data, Initial_liaowei, start_time, time_length, zhenfu_time_list):
        result, total_deviation, liaowei_list = liaowei_predict(self.liaowei_limit_upper, self.liaowei_limit_lower, self.time_span, 
                                 self.slope, self.intercept, jinjiao_time_data, 
                                 Initial_liaowei, start_time, time_length, zhenfu_time_list)
        return result, total_deviation, liaowei_list
    
    def predict_result(self, parameter:list):
        """
        料位预测, 得到预测结果, 0/1, 总偏差total_deviation, 预测料位列表liaowei_list
        :param prediction: 预测类实例
        :param parameter: 包含初始料位、开始时间戳、时间长度和振幅时间列表的参数列表
        :return: 预测结果
        """

        # 检查参数列表长度是否符合要求
        if len(parameter) != 4:
            raise ValueError("输入参数列表长度必须为 4, 分别对应初始料位、开始时间戳、时间长度和振幅时间列表。")

        # 实例化时输入参数
        Initial_liaowei = float(parameter[0])
        start_time = pd.to_datetime(parameter[1], format='mixed')
        time_length = parameter[2]
        zhenfu_time_list = parameter[3]

        # 获取该时段的进焦时间数据
        jinjiao_time_data = tjjh_time_mysql(start_time, time_length)

        # 检查振幅时间列表是否为正确的格式
        if not all(isinstance(item, tuple) and len(item) == 2 for item in zhenfu_time_list):
            raise ValueError("振幅时间列表中的每个元素必须是长度为 2 的元组。")
         
        # 进行预测
        result, total_deviation, liaowei_list = self.predict(jinjiao_time_data, Initial_liaowei, start_time, time_length, zhenfu_time_list)
        # print(f"预测结果: {result}")
        print(f"斜率为: {self.slope}")
        print(f"截距为: {self.intercept}")


        return result, total_deviation, liaowei_list
