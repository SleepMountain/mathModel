import json

# 定义JSON文件路径
json_file_path = r'D:\桌面\111\姜帅杰.json'
# 定义目标TXT文件路径
txt_file_path = r'D:\桌面\111\姜帅杰.txt'

with open(json_file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

with open(txt_file_path, 'w', encoding='utf-8') as file:

    if isinstance(data, (dict, list)):
        for key, value in data.items() if isinstance(data, dict) else enumerate(data):
            file.write(f'{key}: {value}\n')
    else:
        file.write(str(data))

print("转换完成！")