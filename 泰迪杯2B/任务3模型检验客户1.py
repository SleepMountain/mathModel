import json

# 读取JSON数据
with open('D:/桌面/竞赛/泰迪杯2/B/B题-特殊医学用途配方食品数据分析/文件/output.json', 'r') as file:
    data = json.load(file)

def decision_tree(data):

    if data["【适用人群】"] == "食物蛋白过敏婴儿":

        protein_content = data["【营养成分表】"]["蛋白质(等同物)(g)"]["每100g"]
        if protein_content > 0:
            return "拒绝"
        else:
            return "接受"
    else:
        return "拒绝"

results = []
for product_id, product_data in data.items():
    result = decision_tree(product_data)
    results.append(result)

print(results)