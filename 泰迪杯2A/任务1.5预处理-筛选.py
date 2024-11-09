import pandas as pd

input_file = r'D:\桌面\竞赛\泰迪杯2\A\A题-自动化生产线数据分析\附件1\M101.csv'
output_file = r'D:\桌面\竞赛\泰迪杯2\A\A题-自动化生产线数据分析\附件1\result2.xlsx'

df = pd.read_csv(input_file, encoding='gbk')

print("数据基本信息:")
print(df.info())
print("\n数据前5行:")
print(df.head())

filtered_df = df[df['时间'] == 28799]

result = filtered_df.groupby(['月份', '日期'])[['推出累计数', '抓取累计数', '安装累计数', '检测累计数']].first().reset_index()

print("\n统计结果前5行:")
print(result.head())

result.to_excel(output_file, index=False)

print("处理完成，结果已保存至:", output_file)