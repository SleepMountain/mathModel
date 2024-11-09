import csv
import json

tkey = ["月份", "日期", "时间", "故障类别", "推出状态", "推出累计数", "抓取状态", "抓取累计数", "安装状态",
        "安装累计数", "检测状态", "检测累计数", "合格产品累计数", "不合格产品累计数"]


def findkeyid(key):
    return tkey.index(key)


errorkey = ["A1", "A2", "A3", "A4"]
file = ["M101", "M102"]
result = {key: {ekey: 0 for ekey in errorkey} for key in file}
for f in file:
    worktable = {}
    with open("Task1.2-" + f + "-" + "result.csv", newline='', encoding='gbk') as csvfile:
        reader = list(csv.reader(csvfile))
        for rowid in range(1, len(reader)):
            result[f][reader[rowid][3]] += int(reader[rowid][4])

json.dump(result, open("Task2.4.json", "w", encoding='utf-8'), ensure_ascii=False, indent=4)