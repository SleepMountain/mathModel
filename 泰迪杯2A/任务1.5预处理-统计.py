import pandas as pd

input_file = r'D:\桌面\竞赛\泰迪杯2\A\A题-自动化生产线数据分析\附件1\M101.csv'
output_file = r'D:\桌面\竞赛\泰迪杯2\A\A题-自动化生产线数据分析\附件1\result.xlsx'

df = pd.read_csv(input_file, encoding='gbk')

result = df.groupby(['月份', '日期'])[['推出状态', '抓取状态', '安装状态', '检测状态']].apply(lambda x: (x == -1).sum()).reset_index()

result.columns = ['月份', '日期', '推出状态_计数', '抓取状态_计数', '安装状态_计数', '检测状态_计数']

result.to_excel(output_file, index=False)

print("处理完成，结果已保存至:", output_file)