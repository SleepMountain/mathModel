import pandas as pd

# 定义文件路径
# M101
# file_path = r'D:\桌面\竞赛\泰迪杯2\A\A题-自动化生产线数据分析\附件1\M101.csv'
# output_file_path = r'D:\桌面\竞赛\泰迪杯2\A\A题-自动化生产线数据分析\附件1\3.1M101.xlsx'

# M102
file_path = r'D:\桌面\竞赛\泰迪杯2\A\A题-自动化生产线数据分析\附件1\M102.csv'
output_file_path = r'D:\桌面\竞赛\泰迪杯2\A\A题-自动化生产线数据分析\附件1\3.1M102.xlsx'

result_dict = {}

# 逐行读取文件
with open(file_path, 'r', encoding='gbk') as f:
    header = f.readline().strip().split(',')
    time_index = header.index('时间')
    推出状态_index = header.index('推出状态')
    抓取状态_index = header.index('抓取状态')
    安装状态_index = header.index('安装状态')
    检测状态_index = header.index('检测状态')

    for line in f:
        data = line.strip().split(',')
        time = data[time_index]
        推出状态 = int(data[推出状态_index])
        抓取状态 = int(data[抓取状态_index])
        安装状态 = int(data[安装状态_index])
        检测状态 = int(data[检测状态_index])

        if time not in result_dict:
            result_dict[time] = {
                '推出状态_1': 0,
                '抓取状态_1': 0,
                '安装状态_1': 0,
                '检测状态_1': 0
            }

        if 推出状态 == -1:
            result_dict[time]['推出状态_1'] += 1
        if 抓取状态 == -1:
            result_dict[time]['抓取状态_1'] += 1
        if 安装状态 == -1:
            result_dict[time]['安装状态_1'] += 1
        if 检测状态 == -1:
            result_dict[time]['检测状态_1'] += 1

result_df = pd.DataFrame.from_dict(result_dict, orient='index').reset_index()
result_df.columns = ['时间', '推出状态_1', '抓取状态_1', '安装状态_1', '检测状态_1']

result_df.to_excel(output_file_path, index=False)

print(f"处理完成，结果已保存至 {output_file_path}")