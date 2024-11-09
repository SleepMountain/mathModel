# 读取./M101.csv ./M102.csv ，字段头分别为月份	日期	时间	故障类别	推出状态	推出累计数	抓取状态	抓取累计数	安装状态	安装累计数	检测状态	检测累计数	合格产品累计数	不合格产品累计数

# 遍历所有日期和时间
import csv
import json

tkey = ["月份", "日期", "时间", "故障类别", "推出状态", "推出累计数", "抓取状态", "抓取累计数", "安装状态",
        "安装累计数", "检测状态", "检测累计数", "合格产品累计数", "不合格产品累计数"]


def findkeyid(key):
    return tkey.index(key)


def second2time(second):
    time_base = [second % 60, second // 60 % 60, second // 3600]
    time_base.reverse()
    time_unit = ["秒", "分钟", "小时"]
    time_unit.reverse()
    time_str = ""
    for i in range(len(time_base)):
        if time_base[i] != 0:
            time_str += str(time_base[i]) + time_unit[i]
    return time_str


file = ["M101", "M102"]
# Trick：将没有错误视为出错，复用Task1.2逻辑
errorkey = [""]
result = {key: {} for key in file}
for f in file:
    worktable = {}

    with open(f + ".csv", newline='', encoding='gbk') as csvfile:
        reader = list(csv.reader(csvfile))
        for rowid in range(1, len(reader)):
            if (rowid % 4000 == 0):
                print(str(rowid / len(reader) * 100) + "%")
            data = reader[rowid]
            if data[findkeyid("月份")] not in worktable:
                worktable[data[findkeyid("月份")]] = {}
            if data[findkeyid("日期")] not in worktable[data[findkeyid("月份")]]:
                worktable[data[findkeyid("月份")]][data[findkeyid("日期")]] = []
            worktable[data[findkeyid("月份")]][data[findkeyid("日期")]].append(data)
    for month in worktable:
        result[f][month] = {}
        for date in worktable[month]:
            result[f][month][date] = {}
    for month in worktable:
        for date in worktable[month]:
            result[f][month][date]["total_time"] = 1 + int(worktable[month][date][-1][findkeyid("时间")]) - int(
                worktable[month][date][0][findkeyid("时间")])
            result[f][month][date]["error_time"] = 0
    with open("Task1.2-" + f + "-" + "result.csv", newline='', encoding='gbk') as csvfile:
        reader = list(csv.reader(csvfile))
        for rowid in range(1, len(reader)):
            data = reader[rowid]
            result[f][data[0]][data[1]]["error_time"] += int(data[4])

resultcsv = []

for month in result[f]:
    for date in result[f][month]:
        resultcsv.append([
            month + "/" + date,
            int(result["M101"][month][date]["total_time"]) - int(result["M101"][month][date]["error_time"]),
            int(result["M102"][month][date]["total_time"]) - int(result["M102"][month][date]["error_time"])
        ])
with open("Task1.t-" + "result.csv", 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["时间", "M101", "M102"])
    for row in resultcsv:
        writer.writerow(row)
