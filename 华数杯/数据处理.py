import pandas as pd
import numpy as np

# 读取Excel数据
df = pd.read_excel('D:\桌面\竞赛\数模\\2023年第四届“华数杯”全国大学生数学建模竞赛\表格\数据处理.xlsx')

# 获取编号列和数据组列
numbers = df.iloc[:, 0].values.tolist()
data = df.iloc[:, 1:18].values


# 初始化结果字典
result = {}

# 遍历每个组合
for i in range(0, 7):
    for j in range(8, 15):
        for k in range(16, 23):
            # 获取三个编号对应的数据组
            group1 = data[i]
            group2 = data[j]
            group3 = data[k]

            # 计算相加结果
            new_group = group1 + group2 + group3

            # 添加到结果字典中
            result[(numbers[i], numbers[j], numbers[k])] = new_group

# 输出结果
for comb, val in result.items():
    print(f'组合：{comb}')
    print(f'处理后的数据组：{val}')
    print()

# 输出结果到DataFrame
output_data = []
for comb, val in result.items():
    output_data.append([comb, *val])
output_df = pd.DataFrame(output_data, columns=["组合"] + list(range(1, 17)))

# 将组合列设置为索引列
output_df.set_index("组合", inplace=True)

# 保存为Excel文件
output_df.to_excel("D:/桌面/竞赛/数模/2023年第四届“华数杯”全国大学生数学建模竞赛/表格/result.xlsx")