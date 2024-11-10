import json
import regex as re
import csv

data = json.loads(open('../output.json', encoding='utf-8').read())

namelist = ["产品来源", "登记年份"]

result = []

with open("Task1.3-result.csv", newline='', encoding='utf-8') as csvfile:
    reader = list(csv.reader(csvfile))
    result.append(reader[0] + namelist)
    for rowid in range(1, len(reader)):
        tyid = reader[rowid][2].replace("国食注字TY", "")
        single_result = [
            "进口产品" if tyid[4] == "5" else "国产产品",
            tyid[0:4]
        ]
        result.append(reader[rowid] + single_result)

with open("Task1.4-result.csv", 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    for row in result:
        writer.writerow(row)