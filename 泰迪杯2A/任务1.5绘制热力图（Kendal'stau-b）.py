import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号

data = {
    '总数': [1, -0.454, 1],
    '抓取累计数': [-0.454, 1, -0.454],
    '抓取异常_计数': [1, -0.454, 1]
}

df = pd.DataFrame(data, index=['总数', '抓取累计数', '抓取异常_计数'])

plt.figure(figsize=(8, 6))
sns.heatmap(df, annot=True, fmt=".3f", cmap='coolwarm', cbar_kws={'label': '相关系数'}, linewidths=.5)

plt.title('热力图')

plt.show()