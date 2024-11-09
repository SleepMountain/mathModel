import pandas as pd

file_path = r'D:\桌面\竞赛\泰迪杯2\A\A题-自动化生产线数据分析\附件1\M101.csv'
output_path = r'D:\桌面\竞赛\泰迪杯2\A\A题-自动化生产线数据分析\附件1\monthly_production_totalM101.xlsx'

df = pd.read_csv(file_path, encoding='gbk')

monthly_production = df.groupby('月份').agg(
    total_production=('合格产品累计数', lambda x: x.iloc[-1] + df.loc[x.index, '不合格产品累计数'].iloc[-1])
).reset_index()

monthly_production.to_excel(output_path, index=False)

print(f"数据已成功处理并保存至: {output_path}")