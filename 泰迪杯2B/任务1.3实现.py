import json
import regex as re
import csv

data = json.loads(open('../output.json', encoding='utf-8').read())

result = []

with open("Task1.2-result.csv", newline='', encoding='utf-8') as csvfile:
    reader = list(csv.reader(csvfile))
    result.append(reader[0] + ["适用人群类别"])
    for rowid in range(1, len(reader)):
        tyid = reader[rowid][2].replace("国食注字TY", "")
        single_result = "特医婴配食品" if data[tyid]["【适用人群】"].find("婴儿") + 1 else "1岁以上特医食品"
        result.append(reader[rowid] + [single_result])

with open("Task1.3-result.csv", 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    for row in result:
        writer.writerow(row)