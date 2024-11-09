import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

data = {
    '总数': [1, 1, -0.637],
    '抓取累计数': [1, 1, -0.637],
    '抓取异常_计数': [-0.637, -0.637, 1]
}

df = pd.DataFrame(data, index=['总数', '抓取累计数', '抓取异常_计数'])

plt.figure(figsize=(8, 6))
sns.heatmap(df, annot=True, fmt=".3f", cmap='coolwarm', cbar_kws={'label': '相关系数'}, linewidths=.5)

plt.title('热力图')

plt.show()