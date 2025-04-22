import pandas as pd

def count_jinliao(file_path, start_time, end_time):
    """
    函数功能: 判断在给定的开始及结束时间内, 共进料几次
    param: file_path 表示文件路径，本地形式
    param: start_time,end_time 开始及结束时间
    """
    try:
        # 读取 Excel 文件
        df = pd.read_excel(file_path)

        # 将时间戳列转换为 datetime 类型
        df['timestamp'] = pd.to_datetime(df['timestamp'], format='%Y/%m/%d %H:%M')

        # 筛选出指定时间范围内的数据
        filtered_df = df[(df['timestamp'] >= start_time) & (df['timestamp'] <= end_time)]

        # 记录该范围内的数据的行数
        count_row = len(filtered_df)

        # 初始化不同次数计数器
        count_jinliao = 0

        # 依次对两个相邻行对应的 jinjiao_1 列进行比较
        for i in range(len(filtered_df) - 1):
            if filtered_df.iloc[i]['jinjiao_1'] != filtered_df.iloc[i + 1]['jinjiao_1']:
                count_jinliao += 1

        return count_jinliao, count_row

    except FileNotFoundError:
        print(f"错误：未找到文件 {file_path}。")
    except KeyError:
        print("错误：数据中缺少 'timestamp' 或 'jinjiao_1' 列。")
    except Exception as e:
        print(f"发生未知错误：{e}")

    return None, None



if __name__ == "__main__":
    file_path = r'C:\Users\Administrator\Desktop\326_402.xlsx'
    start_time = pd.to_datetime('2025/4/2 9:35', format='%Y/%m/%d %H:%M')
    end_time = pd.to_datetime('2025/4/2 11:05', format='%Y/%m/%d %H:%M')

    count_jinliao, count_row = count_jinliao(file_path, start_time, end_time)

    if count_jinliao is not None and count_row is not None:
        # print(f"在指定时间范围内，相邻 'jinjiao_1' 列数据不同的次数为：{diff_count}")
        print(f"在指定时间范围内，'jinjiao_1' 列的进料次数为：{count_jinliao/2}")
        print(f"该范围内的数据的行数为：{count_row}")
    