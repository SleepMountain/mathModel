import pandas as pd

# 读取CSV文件，指定编码为gbk
# M101
# file_path = r'D:\桌面\竞赛\泰迪杯2\A\A题-自动化生产线数据分析\附件1\M101.csv'
# output_path = r'D:\桌面\竞赛\泰迪杯2\A\A题-自动化生产线数据分析\附件1\3.2M101.xlsx'

# M102
file_path = r'D:\桌面\竞赛\泰迪杯2\A\A题-自动化生产线数据分析\附件1\M102.csv'
output_path = r'D:\桌面\竞赛\泰迪杯2\A\A题-自动化生产线数据分析\附件1\3.2M102.xlsx'

data = pd.read_csv(file_path, encoding='gbk')


filtered_data = data[data['时间'] == 28799]

# 第二步：根据月份字段，对每个相同月份的字段的合格产品累计数和不合格产品累计数求和
monthly_summary = filtered_data.groupby('月份').agg(
    合格产品总数=('合格产品累计数', 'sum'),
    不合格产品总数=('不合格产品累计数', 'sum')
).reset_index()

# 计算每个月份的合格率
monthly_summary['合格率'] = monthly_summary['合格产品总数'] / (monthly_summary['合格产品总数'] + monthly_summary['不合格产品总数'])

# 显示结果
print(monthly_summary)

monthly_summary.to_excel(output_path, index=False)

print(f"结果已保存到 {output_path}")