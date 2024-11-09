
import csv
import json
tkey = ["月份","日期","时间","故障类别","推出状态","推出累计数","抓取状态","抓取累计数","安装状态","安装累计数","检测状态","检测累计数","合格产品累计数","不合格产品累计数"]
def findkeyid(key):
    return tkey.index(key)

result = {
    "x":[time for time in range(1,101)],
    "y":{
        # "1":{ #原件id
        #     "推出":[0,1], #开始时间/结束时间
        #     "抓取":[0,1],
        #     "安装":[0,1],
        #     "检测":[0,1]
        # }
    }
}
with open("Task2.5-split.csv",newline='', encoding='gbk') as csvfile:
    reader = list(csv.reader(csvfile))
    for rowid in range(1,len(reader)):
        data = reader[rowid]

        if data[findkeyid("推出状态")] == "1":
            push_id = data[findkeyid("推出累计数")]
            result["y"][push_id] = {
                "推出":[int(data[findkeyid("时间")]),None],
                "抓取":[None,None],
                "安装":[None,None],
                "检测":[None,None]
            }
        if data[findkeyid("抓取状态")] == "1":
            tick_id = data[findkeyid("抓取累计数")]
            result["y"][tick_id]["推出"][1] = int(data[findkeyid("时间")])
            result["y"][tick_id]["抓取"] = [int(data[findkeyid("时间")]),int(data[findkeyid("时间")])+1]
        if rowid>1 and data[findkeyid("安装累计数")]!=reader[rowid-1][findkeyid("安装累计数")]:
            install_id = data[findkeyid("安装累计数")]
            result["y"][install_id]["安装"][1] = int(data[findkeyid("时间")])
            for row in reader[rowid-1::-1]:
                if row[findkeyid("安装状态")] == "1" and int(row[findkeyid("安装累计数")]) == int(install_id)-1:
                    result["y"][install_id]["安装"][0] = int(row[findkeyid("时间")])
                else:
                    break
        if rowid>1 and data[findkeyid("检测累计数")]!=reader[rowid-1][findkeyid("检测累计数")]:
            check_id = data[findkeyid("检测累计数")]
            result["y"][check_id]["检测"][1] = int(data[findkeyid("时间")])
            for row in reader[rowid-1::-1]:
                if row[findkeyid("检测状态")] == "1" and int(row[findkeyid("检测累计数")]) == int(check_id)-1:
                    result["y"][check_id]["检测"][0] = int(row[findkeyid("时间")])
                else:
                    break
json.dump(result,open("Task2.5.json","w",encoding='utf-8'),ensure_ascii=False,indent=4)