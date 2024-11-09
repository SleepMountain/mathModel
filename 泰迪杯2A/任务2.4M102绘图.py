import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

file_path = r'D:\桌面\竞赛\泰迪杯2\A\A题-自动化生产线数据分析\附件1\任务2.4数据预处理.xlsx'
df = pd.read_excel(file_path, sheet_name='M102')


# df.dropna(inplace=True)

df['持续时长（秒）'] = df['持续时长（秒）'].astype(float)

fault_categories = df['故障类别'].unique()

plt.figure(figsize=(10, 6))
for category in fault_categories:
    data = df[df['故障类别'] == category]['持续时长（秒）']

    plt.hist(data, bins=30, alpha=0.5, label=f'故障类别 {category}')


plt.title('M102在不同故障类别下故障持续时长的直方图')
plt.xlabel('持续时长（秒）')
plt.ylabel('频数')
plt.legend()
plt.show()