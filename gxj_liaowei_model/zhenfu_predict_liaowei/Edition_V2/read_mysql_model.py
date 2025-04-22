import sys
import os
import pandas as pd
from datetime import datetime, timedelta

# 获取目录的路径
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from Utils.utils_MysqlHelper import MysqlHelper

def tjjh_time_mysql(start_time, time_length):
    # 规范开始时间格式，计算结束时间
    start_time = pd.to_datetime(start_time, format='mixed')
    end_time = start_time + timedelta(hours=time_length)
    # 将时间转换为字符串格式
    start_time_str = start_time.strftime('%Y-%m-%d %H:%M:%S')
    end_time_str = end_time.strftime('%Y-%m-%d %H:%M:%S')

    connect = MysqlHelper(MysqlHelper.conn_params)
    # sql = f"SELECT endtime FROM jhzn.jhzn_jh_jbte_time where endtime is not null and endtime >= '{start_time_str}' and endtime <= '{current_time_str}' ORDER BY endtime ASC;"
    # sql = f"SELECT endtime FROM jhzn.jhzn_jh_jbte_time where endtime is not null and endtime >= '{start_time_str}' and endtime <= '{end_time_str}' GROUP BY luhao ORDER BY endtime ASC;"
    # sql = f"SELECT jihuatuijiao_time FROM jhzn.jhzn_tjjh where jihuatuijiao_time is not null and jihuatuijiao_time >= '{start_time_str}' and jihuatuijiao_time <= '{end_time_str}' GROUP BY luhao ORDER BY jihuatuijiao_time ASC;"

    sql = f"SELECT timestamp, _GXJ_C068, _GXJ_C069 FROM jhzn.jhzn_gxj_tishengji where timestamp >= '{start_time_str}' and timestamp <= '{end_time_str}' order by timestamp asc;"

    param = ()
    data = connect.get_all(sql, param)
    # print(f"data 的数据类型是: {type(data)}")

    # 筛选符合条件的数据
    filtered_data = []
    prev_value = None
    for index, row in enumerate(data):
        current_value = row[1]
        if (index == 0 and current_value == 'true') or (prev_value == 'false' and current_value == 'true'):
            filtered_data.append((row[0],))
        prev_value = current_value


    return filtered_data

def real_liaowei_mysql(start_time, time_length):
    # 规范开始时间格式，计算结束时间
    start_time = pd.to_datetime(start_time, format='mixed')
    end_time = start_time + timedelta(hours=time_length)
    # 将时间转换为字符串格式
    start_time_str = start_time.strftime('%Y-%m-%d %H:%M:%S')
    end_time_str = end_time.strftime('%Y-%m-%d %H:%M:%S')

    connect = MysqlHelper(MysqlHelper.conn_params)
    sql = f"SELECT Timestamp AS timestamp, GXJ_B0036 AS liaowei, GXJ_ZDGLQ_GD AS zhenfu FROM jhzn.jhzn_gxj_others_history where Timestamp >= '{start_time_str}' AND Timestamp <= '{end_time_str}' ORDER BY Timestamp;"

    param = ()
    data = connect.get_all(sql, param)
    # print(f"data 的数据类型是: {type(data)}")
    return data

# # 示例调用
# current_time = datetime.now()
# time_length = 1

# result = tjjh_time_mysql(pd.to_datetime('2025/4/15 20:00:00', format='mixed'), 4)
# # # result = real_liaowei_mysql(current_time, time_length)
# if result:
#     for row in result:
#         print(row)
# else:
#     print("未查询到数据或查询过程中出现错误。")