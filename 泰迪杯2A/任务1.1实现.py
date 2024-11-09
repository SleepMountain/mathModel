
import csv

tkey = ["月份", "日期", "时间", "故障类别", "推出状态", "推出累计数", "抓取状态", "抓取累计数", "安装状态",
        "安装累计数", "检测状态", "检测累计数", "合格产品累计数", "不合格产品累计数"]


def findkeyid(key):
    return tkey.index(key)


file = ["M101", "M102"]
# file= ["MT"]
for f in file:
    result = []
    with open(f + ".csv", newline='', encoding='gbk') as csvfile:
        reader = list(csv.reader(csvfile))
        reader.append([])
        for rowid in range(2, len(reader)):
            tmp = reader[rowid - 1]
            ftmp = reader[rowid]
            if (rowid == len(reader) - 1 or tmp[findkeyid("月份")] + "-" + tmp[findkeyid("日期")] != ftmp[
                findkeyid("月份")] + "-" + ftmp[findkeyid("日期")]):
                print(tmp)
                rdata = [
                    tmp[findkeyid("月份")],
                    tmp[findkeyid("日期")],
                    tmp[findkeyid("检测累计数")],
                    tmp[findkeyid("合格产品累计数")],
                    tmp[findkeyid("不合格产品累计数")],
                    0 if int(tmp[findkeyid("检测累计数")]) == 0 else int(tmp[findkeyid("合格产品累计数")]) / int(
                        tmp[findkeyid("检测累计数")])
                ]
                result.append(rdata)
    with open("Task1.1-" + f + "-" + "result.csv", 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["月份", "日期", "总数", "合格数", "不合格数", "合格率"])
        for row in result:
            writer.writerow(row)
    total = 0
    total_qual = 0
    total_unqual = 0
    for row in result:
        total += int(row[2])
        total_qual += int(row[3])
        total_unqual += int(row[4])
    total_rate = total_qual / total
    print("生产线" + f + "总数：" + str(total) + "合格数：" + str(total_qual) + "不合格数：" + str(
        total_unqual) + "合格率：" + str(total_rate))
