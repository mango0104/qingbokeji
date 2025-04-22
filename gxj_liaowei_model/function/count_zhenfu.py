import pandas as pd

def count_zhenfu(file_path, start_time, end_time, unit):
    """
    函数功能: 判断一段时间内, 每个振幅出现的时间,并以列表形式返回
    param: file_path: 文件路径，本地形式
    param: unit: 表示时间单位, 60为分钟, 3600为小时
    """
    try:
        # 读取 Excel 文件
        df = pd.read_excel(file_path)

        df['timestamp'] = pd.to_datetime(df['timestamp'], format='mixed')
        df = df[(df['timestamp'] >= start_time) & (df['timestamp'] <= end_time)]

        # 对 zhenfu 列取整，并存储在新的列 zhenfu_int 中
        # df['zhenfu_int'] = df['zhenfu'].round().astype(int)
        df['zhenfu_int'] = df['zhenfu'].astype(int)

        # 用于存储最终分析结果的列表
        results = []
        # 初始化当前振幅值、当前振幅出现次数、开始出现时间、结束出现时间
        current_value = None
        current_count = 0
        start_timestamp = None
        end_timestamp = None

        # 逐行遍历 DataFrame
        for index, row in df.iterrows():
            # 获取当前行的振幅及时间
            zhenfu_int = row['zhenfu_int']
            timestamp = row['timestamp']

            # 若 current_value 为 None，说明是第一次处理数据
            if current_value is None:
                current_value = zhenfu_int
                current_count = 1
                start_timestamp = timestamp
                end_timestamp = timestamp
            # 若当前取整后的数值和之前记录的相同，则数量 +1，结束时间更新
            elif zhenfu_int == current_value:
                current_count += 1
                end_timestamp = timestamp
            # 若当前取整后的数值和之前记录的不同，则将计算时间差并存储，并重新计数
            else:
                # 计算时间差（小时）
                time_diff = (end_timestamp - start_timestamp).total_seconds() / unit
                results.append((current_value, current_count, start_timestamp, end_timestamp, time_diff))
                # 重新计数
                current_value = zhenfu_int
                current_count = 1
                start_timestamp = timestamp
                end_timestamp = timestamp

        # 处理最后一组数据，防止最后一组数据未被添加到结果列表中
        if current_value is not None:
            time_diff = (end_timestamp - start_timestamp).total_seconds() / unit
            results.append((current_value, current_count, start_timestamp, end_timestamp, time_diff))

        return results

    except FileNotFoundError:
        print(f"错误: 文件 {file_path} 未找到。")
    except Exception as e:
        print(f"发生未知错误: {e}")

if __name__ == "__main__":
    file_path = r'C:\Users\Administrator\Desktop\predict_data.xlsx'
    start_time = pd.to_datetime('2025/4/2 0:00:00', format='mixed')
    end_time = pd.to_datetime('2025/4/3 12:30:00', format='mixed')
    unit = 60  # 作为秒数的除数，60表示分钟，3600表示小时
    results = count_zhenfu(file_path, start_time, end_time, unit)
    if results:
        for result in results:
            print(result)    