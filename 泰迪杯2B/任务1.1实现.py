import json
import regex as re
import csv

data = json.loads(open('../output.json', encoding='utf-8').read())

# 营养需求
nutrient_name_require = ['能量', '脂肪', '碳水化合物', '蛋白质', '钠', '氯', '钾', '磷']
nutrient_unit_require = ['kJ', 'g', 'g', 'g', 'mg', 'mg', 'mg', 'mg']

result = {}

for tyid in data:
    result[tyid] = {key: 0 for key in nutrient_name_require}
    for nutrient in data[tyid]["【营养成分表】"]:
        for require_nutrient_name in nutrient_name_require:
            if re.match(r'^' + require_nutrient_name + "\\(", nutrient):
                result[tyid][require_nutrient_name] = float(data[tyid]["【营养成分表】"][nutrient]["每100kJ"])
                # 单位检查
                if re.search('\\(' + nutrient_unit_require[nutrient_name_require.index(require_nutrient_name)] + '\\)',
                             nutrient) == None:
                    # 少量单位错误直接手动修改，不进行转换
                    print("!!!!单位错误：", tyid, nutrient)
                break;
result_csv = []
result_csv_header = [nutrient_name_require[i] + "({})".format(nutrient_unit_require[i]) for i in
                     range(len(nutrient_name_require))]
result_csv_header.insert(0, "注册证号")
for tyid in result:
    result_row = ["国食注字TY" + tyid]
    for nutrient_name in nutrient_name_require:
        result_row.append(result[tyid][nutrient_name])
    result_csv.append(result_row)

with open("Task1.1-result.csv", 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(result_csv_header)
    for row in result_csv:
        writer.writerow(row)