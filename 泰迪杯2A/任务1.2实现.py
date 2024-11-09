
import csv
import json

tkey = ["月份", "日期", "时间", "故障类别", "推出状态", "推出累计数", "抓取状态", "抓取累计数", "安装状态",
        "安装累计数", "检测状态", "检测累计数", "合格产品累计数", "不合格产品累计数"]


def findkeyid(key):
    return tkey.index(key)


file = ["M101", "M102"]
errorkey = ["A1", "A2", "A3", "A4"]

for f in file:
    result = []
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
        for date in worktable[month]:
            errordata = worktable[month][date]
            for errorid in range(0, len(errordata)):
                if (errorid != 0):
                    if (errorid == len(errordata) - 1):
                        result[-1][-1] = int(errordata[errorid][findkeyid("时间")]) - int(result[-1][2]) + 1
                        break;
                    if (errordata[errorid][findkeyid("故障类别")] != errordata[errorid - 1][findkeyid("故障类别")]):
                        result[-1][-1] = int(errordata[errorid - 1][findkeyid("时间")]) - int(result[-1][2]) + 1
                    else:
                        continue
                result.append([
                    month,
                    date,
                    errordata[errorid][findkeyid("时间")],
                    errordata[errorid][findkeyid("故障类别")],
                    None
                ])

    result = [row for row in result if row[3] in errorkey]

    errorcount = {key: 0 for key in errorkey}
    errorresult = []
    # 找到第25次故障
    for row in result:
        errorcount[row[3]] += 1
        if errorcount[row[3]] == 25:
            error25 = [
                f,
                row[3],
                row[0],
                row[1],
                row[2],
                row[4]
            ]
            errorresult.append(error25)

    with open("Task1.2-" + f + "-" + "result.csv", 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["月份", "日期", "开始时间", "故障类别", "持续时长（秒）"])
        for row in result:
            writer.writerow(row)
    with open("Task1.2-" + f + "-" + "error25.csv", 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["生产线", "故障类别", "月份", "日期", "开始时间", "持续时长（秒）"])
        for row in errorresult:
            writer.writerow(row)


