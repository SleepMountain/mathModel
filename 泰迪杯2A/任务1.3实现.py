
import numpy as np
import csv

tkey = ["月份", "日期", "时间", "故障类别", "推出状态", "推出累计数", "抓取状态", "抓取累计数", "安装状态",
        "安装累计数", "检测状态", "检测累计数", "合格产品累计数", "不合格产品累计数"]


def findkeyid(key):
    return tkey.index(key)


result = []
file = ["M101", "M102"]


for f in file:
    result = []
    errortable = {}
    errorkey = ["A1", "A2", "A3", "A4"]
    with open("Task1.2-" + f + "-" + "result.csv", newline='', encoding='gbk') as csvfile:
        reader = list(csv.reader(csvfile))
        for rowid in range(2, len(reader)):
            if reader[rowid][0] not in errortable:
                errortable[reader[rowid][0]] = {}
            if reader[rowid][1] not in errortable[reader[rowid][0]]:
                errortable[reader[rowid][0]][reader[rowid][1]] = {key: {"count": 0, "time": 0} for key in errorkey}

            errortable[reader[rowid][0]][reader[rowid][1]][reader[rowid][3]]["count"] += 1
            errortable[reader[rowid][0]][reader[rowid][1]][reader[rowid][3]]["time"] += int(reader[rowid][4])
    for month in errortable:
        for date in errortable[month]:
            for error in errortable[month][date]:
                result.append([
                    f,
                    month,
                    date,
                    error,
                    errortable[month][date][error]["count"],
                    errortable[month][date][error]["time"] / errortable[month][date][error]["count"] if
                    errortable[month][date][error]["count"] != 0 else "Null"
                ])
    ResultAnalysis = [["生产线" + f, "总次数", "平均持续时长（秒/次）", "发生频率（次/天）"]]
    for error in errorkey:
        count = 0
        time = 0
        for row in result:
            if row[3] == error:
                count += row[4]
                time += row[5] if row[5] != "Null" else 0
        ResultAnalysis.append(["故障类别" + error, count, time / count, count / len(errortable)])

    ResultAnalysis.append(["汇总",
                           sum([row[1] for row in ResultAnalysis[1:]]),
                           sum([row[2] * row[1] for row in ResultAnalysis[1:]]) / sum(
                               [row[1] for row in ResultAnalysis[1:]]),
                           sum([row[3] for row in ResultAnalysis[1:]]) / len(ResultAnalysis[1:])
                           ])
    print(ResultAnalysis)
    ResultAnalysis = np.array(ResultAnalysis).T
    with open("Task1.3-" + f + "-" + "ResultAnalysis.csv", 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in ResultAnalysis:
            writer.writerow(row)

    with open("Task1.3-" + f + "-" + "result.csv", 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["生产线", "月份", "日期", "故障类别", "总次数", "持续时长（秒）"])
        for row in result:
            writer.writerow(row)

