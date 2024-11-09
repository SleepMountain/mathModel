
import csv
import json
tkey = ["月份","日期","时间","故障类别","推出状态","推出累计数","抓取状态","抓取累计数","安装状态","安装累计数","检测状态","检测累计数","合格产品累计数","不合格产品累计数"]
def findkeyid(key):
    return tkey.index(key)
result = []
file = ["M101"]
for f in file:
    worktable = {}
    s=0
    with open(f+".csv", newline='', encoding='gbk') as csvfile:
        reader = list(csv.reader(csvfile))
        for rowid in range(1,len(reader)):

            if(reader[rowid][findkeyid("月份")]=="4" and reader[rowid][findkeyid("日期")]=="26" and s<100):
                result.append(reader[rowid])
                s+=1
with open("Task2.5-"+"split.csv", 'w', newline='') as csvfile:
    writer  = csv.writer(csvfile)
    writer.writerow(tkey)
    for row in result:
        writer.writerow(row)