import csv
import json

tkey = ["月份", "日期", "时间", "故障类别", "推出状态", "推出累计数", "抓取状态", "抓取累计数", "安装状态",
        "安装累计数", "检测状态", "检测累计数", "合格产品累计数", "不合格产品累计数"]


def findkeyid(key):
    return tkey.index(key)


f = "M101"


def analysisData(fulldata):
    result = {}
    for rowid in range(0, len(fulldata)):
        data = fulldata[rowid]
        if data[findkeyid("推出状态")] == "1":
            push_id = data[findkeyid("推出累计数")]
            result[push_id] = {
                "推出": [int(data[findkeyid("时间")]), None, 0, 0],
                "抓取": [None, None, 0, 0],
                "安装": [None, None, 0, 0],
                "检测": [None, None, 0, 0]
            }
        # -1为出现错误，计算错误时间

        if (len(result) > 1 and data[findkeyid("推出状态")] == "-1" and fulldata[rowid - 1][
            findkeyid("推出状态")] != "-1"):
            push_id = data[findkeyid("推出累计数")]
            result[push_id]["推出"][2] = int(data[findkeyid("时间")])

        if (len(result) > 1 and data[findkeyid("推出状态")] != "-1" and fulldata[rowid - 1][
            findkeyid("推出状态")] == "-1"):
            push_id = fulldata[rowid - 1][findkeyid("推出累计数")]
            result[push_id]["推出"][3] = int(data[findkeyid("时间")])

        if len(result) > 1 and data[findkeyid("抓取状态")] == "-1" and fulldata[rowid - 1][
            findkeyid("抓取状态")] != "-1":
            tick_id = data[findkeyid("抓取累计数")]
            if int(tick_id) <= 0:
                continue
            result[tick_id]["抓取"][2] = int(data[findkeyid("时间")])

        if len(result) > 1 and data[findkeyid("抓取状态")] != "-1" and fulldata[rowid - 1][
            findkeyid("抓取状态")] == "-1":
            tick_id = fulldata[rowid - 1][findkeyid("抓取累计数")]
            if int(tick_id) <= 0:
                continue
            result[tick_id]["抓取"][3] = int(data[findkeyid("时间")])

        if len(result) > 1 and data[findkeyid("安装状态")] == "-1" and fulldata[rowid - 1][
            findkeyid("安装状态")] != "-1":
            install_id = data[findkeyid("安装累计数")]
            if int(install_id) <= 0:
                continue
            result[install_id]["安装"][2] = int(data[findkeyid("时间")])

        if len(result) > 1 and data[findkeyid("安装状态")] != "-1" and fulldata[rowid - 1][
            findkeyid("安装状态")] == "-1":
            install_id = fulldata[rowid - 1][findkeyid("安装累计数")]
            if int(install_id) <= 0:
                continue
            result[install_id]["安装"][3] = int(data[findkeyid("时间")])

        if len(result) > 1 and data[findkeyid("检测状态")] == "-1" and fulldata[rowid - 1][
            findkeyid("检测状态")] != "-1":
            check_id = data[findkeyid("检测累计数")]
            if int(check_id) <= 0:
                continue
            result[check_id]["检测"][2] = int(data[findkeyid("时间")])

        if len(result) > 1 and data[findkeyid("检测状态")] != "-1" and fulldata[rowid - 1][
            findkeyid("检测状态")] == "-1":
            check_id = fulldata[rowid - 1][findkeyid("检测累计数")]
            if int(check_id) <= 0:
                continue
            result[check_id]["检测"][3] = int(data[findkeyid("时间")])

        if data[findkeyid("抓取状态")] == "1":
            tick_id = data[findkeyid("抓取累计数")]
            result[tick_id]["推出"][1] = int(data[findkeyid("时间")])
            result[tick_id]["抓取"][0] = int(data[findkeyid("时间")])
            result[tick_id]["抓取"][1] = int(data[findkeyid("时间")]) + 1
        if len(result) > 1 and data[findkeyid("安装累计数")] != fulldata[rowid - 1][findkeyid("安装累计数")]:
            install_id = data[findkeyid("安装累计数")]
            result[install_id]["安装"][1] = int(data[findkeyid("时间")])
            for row in fulldata[rowid - 1::-1]:
                if row[findkeyid("安装状态")] == "1" and int(row[findkeyid("安装累计数")]) == int(install_id) - 1:
                    result[install_id]["安装"][0] = int(row[findkeyid("时间")])
                else:
                    break
        if len(result) > 1 and data[findkeyid("检测累计数")] != fulldata[rowid - 1][findkeyid("检测累计数")]:
            check_id = data[findkeyid("检测累计数")]
            result[check_id]["检测"][1] = int(data[findkeyid("时间")])
            for row in fulldata[rowid - 1::-1]:
                if row[findkeyid("检测状态")] == "1" and int(row[findkeyid("检测累计数")]) == int(check_id) - 1:
                    result[check_id]["检测"][0] = int(row[findkeyid("时间")])
                else:
                    break
    return result


full_result = {}
with open(f + ".csv", newline='', encoding='gbk') as csvfile:
    # with open("t2split.csv",newline='', encoding='gbk') as csvfile:
    reader = list(csv.reader(csvfile))
    for rowid in range(1, len(reader)):
        if (rowid % 4000 == 0):
            print(str(rowid / len(reader) * 100) + "%")
        data = reader[rowid]
        if reader[rowid][findkeyid("月份")] not in full_result:
            full_result[reader[rowid][findkeyid("月份")]] = {}
        if reader[rowid][findkeyid("日期")] not in full_result[reader[rowid][findkeyid("月份")]]:
            full_result[reader[rowid][findkeyid("月份")]][reader[rowid][findkeyid("日期")]] = []
        full_result[reader[rowid][findkeyid("月份")]][reader[rowid][findkeyid("日期")]].append(data)

error_data = {}
with open("Task1.2-" + f + "-" + "result.csv", newline='', encoding='gbk') as csvfile:
    reader = list(csv.reader(csvfile))
    for rowid in range(1, len(reader)):
        data = reader[rowid]
        if data[0] not in error_data:
            error_data[data[0]] = {}
        if data[1] not in error_data[data[0]]:
            error_data[data[0]][data[1]] = []
        error_data[data[0]][data[1]].append({
            "error_type": data[3],
            "error_start": int(data[2]),
            "error_end": int(data[2]) + int(data[4])
        })
day = 0
AnaDataCSVHeader = [
    "日期",
    "统计周期开始时间",
    "统计周期结束时间",
    "统计周期时长",
    "统计绝对时间",
    "推出平均耗时",
    "推出最大耗时",
    "推出最小耗时",
    "推出错误出现次数",
    "抓取平均耗时",
    "抓取最大耗时",
    "抓取最小耗时",
    "抓取错误出现次数",
    "安装平均耗时",
    "安装最大耗时",
    "安装最小耗时",
    "安装错误出现次数",
    "检测平均耗时",
    "检测最大耗时",
    "检测最小耗时",
    "检测错误出现次数",
    "A1错误出现次数",
    "A2错误出现次数",
    "A3错误出现次数",
    "A4错误出现次数"
]
AnaDataCSV = []

step = 60 * 60 * 3

for month in full_result:
    for date in full_result[month]:
        day += 1
        anadata = analysisData(full_result[month][date])
        for i in range(1, 28800, step):
            count = {
                "推出": [0, 0, 0, step, 0],
                "抓取": [0, 0, 0, step, 0],
                "安装": [0, 0, 0, step, 0],
                "检测": [0, 0, 0, step, 0],  # 0:count,1:all_time,2:max_time,3:min_time,4:error_count
                "A1": 0,
                "A2": 0,
                "A3": 0,
                "A4": 0
            }

            # 推出平均耗时：指查询anadata钟轮询所有id，计算其开始时间是否在i和i+step之间，如果是则计算其耗时

            for key in anadata:
                for skey in anadata[key]:
                    if anadata[key][skey][0] and anadata[key][skey][1] and anadata[key][skey][0] >= i and \
                            anadata[key][skey][0] < i + step:
                        count[skey][0] += 1
                        count[skey][1] += anadata[key][skey][1] - anadata[key][skey][0]
                        count[skey][2] = max(count[skey][2], anadata[key][skey][1] - anadata[key][skey][0])
                        count[skey][3] = min(count[skey][3], anadata[key][skey][1] - anadata[key][skey][0])
                    if anadata[key][skey][2] and anadata[key][skey][3] and anadata[key][skey][2] >= i and \
                            anadata[key][skey][2] < i + step:
                        count[skey][4] += 1

            for error in error_data[month][date]:
                if (error["error_start"] >= i and error["error_start"] < i + step) or (
                        error["error_end"] >= i and error["error_end"] < i + step):
                    count[error["error_type"]] += 1

            AnaDataCSV.append([
                month + "/" + date,
                i,
                i + step,
                step,
                day * 28800 + i,
                count["推出"][1] / count["推出"][0] if count["推出"][0] else 0,
                count["推出"][2] if count["推出"][0] else 0,
                count["推出"][3] if count["推出"][0] else 0,
                count["推出"][4],
                count["抓取"][1] / count["抓取"][0] if count["抓取"][0] else 0,
                count["抓取"][2] if count["抓取"][0] else 0,
                count["抓取"][3] if count["抓取"][0] else 0,
                count["抓取"][4],
                count["安装"][1] / count["安装"][0] if count["安装"][0] else 0,
                count["安装"][2] if count["安装"][0] else 0,
                count["安装"][3] if count["安装"][0] else 0,
                count["安装"][4],
                count["检测"][1] / count["检测"][0] if count["检测"][0] else 0,
                count["检测"][2] if count["检测"][0] else 0,
                count["检测"][3] if count["检测"][0] else 0,
                count["检测"][4],
                count["A1"],
                count["A2"],
                count["A3"],
                count["A4"]
            ])
        print("Finish " + month + "/" + date)

with open("t2result-101-3h-fix.csv", 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(AnaDataCSVHeader)
    for row in AnaDataCSV:
        writer.writerow(row)