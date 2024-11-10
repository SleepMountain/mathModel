import json
import regex as re
import csv

data = json.loads(open('../output.json', encoding='utf-8').read())

name_require = ['产品类别', "组织状态", "适用人群"]

result = []

with open("data.csv", newline='', encoding='utf-8') as csvfile:
    reader = list(csv.reader(csvfile))
    result.append(reader[0] + name_require)
    for rowid in range(1, len(reader)):
        tyid = reader[rowid][2].replace("国食注字TY", "")
        single_result = []
        for name in name_require:
            name = "【{}】".format(name)
            if name in data[tyid]:
                if name == "【组织状态】":
                    data[tyid][name] = data[tyid][name].replace("。", "")
                single_result.append(data[tyid][name].replace("-", "～").replace("~", "～"))
            else:
                single_result.append("Null")
                print("!!!!缺失信息：", tyid, name)
        result.append(reader[rowid] + single_result)

with open("Task1.2-result.csv", 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    for row in result:
        writer.writerow(row)

# result_csv  = []
# result_csv_header = [nutrient_name_require[i]+"({})".format(nutrient_unit_require[i]) for i in range(len(nutrient_name_require))]
# result_csv_header.insert(0, "注册证号")
# for tyid in result:
#     result_row = ["国食注字TY"+tyid]
#     for nutrient_name in nutrient_name_require:
#         result_row.append(result[tyid][nutrient_name])
#     result_csv.append(result_row)

# with open("Task1.1-result.csv", 'w', newline='') as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerow(result_csv_header)
#     for row in result_csv:
#         writer.writerow(row)