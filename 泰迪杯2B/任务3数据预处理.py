import json
import pandas as pd

file_path = r"D:\桌面\竞赛\泰迪杯2\B\B题-特殊医学用途配方食品数据分析\文件\output.json"
with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

df_list = []

all_columns = set()

for key, value in data.items():
    row = {
        "注册号": key,
        "名称": value.get("【名称】", 0),
        "公司": value.get("【公司】", 0),
        "产品类别": value.get("【产品类别】", 0),
        "配料表": value.get("【配料表】", 0),
        "配方特点/营养学特征": value.get("【配方特点/营养学特征】", 0),
        "组织状态": value.get("【组织状态】", 0),
        "适用人群": value.get("【适用人群】", 0),
        "食用方法和食用量": value.get("【食用方法和食用量】", 0),
        "净含量和规格": value.get("【净含量和规格】", 0),
        "保质期": value.get("【保质期】", 0),
        "贮存条件": value.get("【贮存条件】", 0),
        "警示说明和注意事项": value.get("【警示说明和注意事项】", 0)
    }

    # 处理营养成分表
    for nutrient, values in value.get("【营养成分表】", {}).items():
        for unit, amount in values.items():
            column_name = f"{nutrient} ({unit})"
            if column_name not in all_columns:
                all_columns.add(column_name)
                row[column_name] = amount if amount is not None else 0
            else:

                continue

    df_list.append(row)

df = pd.DataFrame(df_list)

df.fillna(0, inplace=True)

output_file_path = r"D:\桌面\竞赛\泰迪杯2\B\B题-特殊医学用途配方食品数据分析\文件\output.xlsx"
df.to_excel(output_file_path, index=False, engine='openpyxl')

print(f"数据已成功保存到 {output_file_path}")