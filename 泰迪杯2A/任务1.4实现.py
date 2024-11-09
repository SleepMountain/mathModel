
import csv

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

avgdata = {
    "total_day": 0,
    "M101": 0,
    "M102": 0
}

for month in result["M101"]:
    for date in result["M101"][month]:
        resultcsv.append([
            month,
            date,
            second2time(
                int(result["M101"][month][date]["total_time"]) - int(result["M101"][month][date]["error_time"])),
            second2time(int(result["M102"][month][date]["total_time"]) - int(result["M102"][month][date]["error_time"]))
        ])
        avgdata["total_day"] += 1
        avgdata["M101"] += int(result["M101"][month][date]["total_time"]) - int(
            result["M101"][month][date]["error_time"])
        avgdata["M102"] += int(result["M102"][month][date]["total_time"]) - int(
            result["M102"][month][date]["error_time"])

resulttotal = [
    ["生产线", "日平均有效工作时长（小时/天）"],
    ["M101", second2time(avgdata["M101"] / avgdata["total_day"])],
    ["M102", second2time(avgdata["M102"] / avgdata["total_day"])]
]

with open("Task1.4-" + "result.csv", 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["月份", "日期", "M101（小时）", "M102（小时）"])
    for row in resultcsv:
        writer.writerow(row)
with open("Task1.4-" + "resulttotal.csv", 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for row in resulttotal:
        writer.writerow(row)

