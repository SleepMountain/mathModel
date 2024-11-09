import json

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
key = ['推出', '抓取', '安装', '检测']
# Load the Excel file
file_path = './Task2.5.json'
#gdk
data = json.loads(open(file_path, 'r', encoding='utf-8').read())
max = 100
x = data['x']
y = {}
for id in data['y']:
    for skey in key:
        y["工件"+str(id)+skey] = data['y'][id][skey]

colors = {
    '推出': '#FF9999',  # light red
    '抓取': '#66B2FF',  # light blue
    '安装': '#99FF99',  # light green
    '检测': '#FFCC66'   # light orange
}


fig, ax = plt.subplots(figsize=(12, 6))


for i,dataname in enumerate(y):
    start_time = y[dataname][0]
    end_time = y[dataname][1]
    duration = 100 if not (end_time and start_time) else end_time - start_time
    if start_time:
        ax.barh(i, duration, left=start_time, color=colors[dataname[-2:]], label=dataname[-2:])


ax.set_xlabel("时间 (秒)")
ax.set_ylabel("工序")
ax.set_title("生产线 M101 的 4 个工序甘特图（前 100 秒）")
ax.set_xlim(0, 100)

ax.set_yticks(range(len(colors.keys())))
ax.set_yticklabels(colors.keys())


handles = [mpatches.Patch(color=color, label=task) for task, color in colors.items()]
ax.legend(handles=handles, title="工序状态", loc='upper right')

ax.grid(axis='x', linestyle='--', alpha=0.6)

plt.tight_layout()
plt.show()