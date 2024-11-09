import pandas as pd


# M101
file_path = r'D:\桌面\竞赛\泰迪杯2\A\A题-自动化生产线数据分析\附件1\M101.csv'
output_file_path = r'D:\桌面\竞赛\泰迪杯2\A\A题-自动化生产线数据分析\附件1\2.3M101.xlsx'

# M02
file_path = r'D:\桌面\竞赛\泰迪杯2\A\A题-自动化生产线数据分析\附件1\M102.csv'
output_file_path = r'D:\桌面\竞赛\泰迪杯2\A\A题-自动化生产线数据分析\附件1\2.3M102.xlsx'

try:
    df = pd.read_csv(file_path, encoding='gbk', sep=',')
except Exception as e:
    print(f"读取文件时发生错误: {e}")
    exit(1)

fault_counts = df['故障类别'].value_counts()

all_faults = ['A1', 'A2', 'A3', 'A4']


fault_counts = fault_counts.reindex(all_faults, fill_value=0)

# 将统计结果转换为DataFrame
result_df = pd.DataFrame(fault_counts).reset_index()
result_df.columns = ['故障类别', '出现次数']

try:
    result_df.to_excel(output_file_path, index=False)
    print(f"统计结果已保存到 {output_file_path}")
except Exception as e:
    print(f"保存文件时发生错误: {e}")