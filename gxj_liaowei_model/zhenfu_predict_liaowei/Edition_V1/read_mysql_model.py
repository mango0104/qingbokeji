import sys
import os

# 获取目录的路径
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from utils_MysqlHelper import MysqlHelper

def tjjh_time_mysql():
    connect = MysqlHelper(MysqlHelper.conn_params)
    # sql = "SELECT jihuachujiaoshijian FROM jhzn.jhzn_jh_tuijiao_1 where jihuachujiaoshijian > '2025-04-07 00:00:00' order by timestamp desc;"
    # sql = "SELECT jihuachujiaoshijian FROM jhzn.jhzn_jh_tuijiao_1 where jihuachujiaoshijian > '2025-04-05 09:00:00' and jihuachujiaoshijian < '2025-04-05 21:00:00' ORDER BY jihuachujiaoshijian ASC;"
    # sql = "SELECT endtime FROM jhzn.jhzn_jh_jbte_time where endtime is not null and endtime >= '2025-04-07 02:00:00' and endtime <= '2025-04-07 12:00:00' ORDER BY endtime ASC;"
    sql = "SELECT endtime FROM jhzn.jhzn_jh_jbte_time where endtime is not null and endtime >= '2025-04-13 08:00:00' and endtime <= '2025-04-13 18:00:00' ORDER BY endtime ASC;"

    param = ()
    data = connect.get_all(sql, param)
    # print(f"data 的数据类型是: {type(data)}")
    return data

def real_liaowei_mysql():
    connect = MysqlHelper(MysqlHelper.conn_params)
    # sql = "SELECT Timestamp AS timestamp, GXJ_B0036 AS liaowei FROM jhzn.jhzn_gxj_add where Timestamp >= '2025-04-07 02:00:00' AND Timestamp <= '2025-04-07 12:00:00' ORDER BY Timestamp;"
    sql = "SELECT Timestamp AS timestamp, GXJ_B0036 AS liaowei, GXJ_ZDGLQZF AS zhenfu FROM jhzn.jhzn_gxj_add where Timestamp >= '2025-04-13 08:00:00' AND Timestamp <= '2025-04-13 18:00:00' ORDER BY Timestamp;"


    param = ()
    data = connect.get_all(sql, param)
    # print(f"data 的数据类型是: {type(data)}")
    return data

result = tjjh_time_mysql()
# result = real_liaowei_mysql()
if result:
    for row in result:
        print(row)
else:
    print("未查询到数据或查询过程中出现错误。")