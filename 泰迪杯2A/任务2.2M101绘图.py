import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号

file_path = r'D:\桌面\竞赛\泰迪杯2\A\A题-自动化生产线数据分析\附件1\任务2.2数据预处理.xlsx'
sheet_name = 'M101'
df = pd.read_excel(file_path, sheet_name=sheet_name)

print(df.head())

fig, ax1 = plt.subplots(figsize=(14, 7))

color1 = '#1f77b4'
ax1.set_xlabel('日期')
ax1.set_ylabel('M101不合格数', color=color1)
ax1.plot(df['日期'], df['M101不合格数'], color=color1, linewidth=2, marker='o', label='M101不合格数')
ax1.tick_params(axis='y', labelcolor=color1)
ax1.grid(True, linestyle='--', alpha=0.6)

# 创建第二个Y轴
ax2 = ax1.twinx()
color2 = '#ff7f0e'
ax2.set_ylabel('M101不合格率 (%)', color=color2)
ax2.plot(df['日期'], df['M101合格率'] * 100, color=color2, linewidth=2, marker='x', linestyle='--', label='M101不合格率')
ax2.tick_params(axis='y', labelcolor=color2)
ax2.grid(True, linestyle='--', alpha=0.6)

plt.title('M101生产线不合格数与不合格率变化趋势', fontsize=16)
fig.tight_layout()
ax1.legend(loc='upper left', fontsize=12)
ax2.legend(loc='upper right', fontsize=12)


plt.show()