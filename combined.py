import json
import os

# 设置文件夹路径
folder_path = "/mnt/public/code/wangzr/mds/multi-turn_code/output/test3"

# 用于存储所有 JSON 数据的列表
merged_data = []
i=0
# 遍历文件夹中的所有 JSON 文件
for filename in os.listdir(folder_path):
    i+=1
    print(i)
    if filename.endswith(".json"):
        file_path = os.path.join(folder_path, filename)
        
        # 读取每个 JSON 文件内容并添加到列表
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            merged_data.append(data)

# 将合并后的数据写入到一个新的 JSON 文件中
with open(f"{folder_path}/merged_output.json", 'w', encoding='utf-8') as f:
#with open("/mnt/public/code/wangzr/mds/AI4MED/Training_free/try_merged_output.json", 'w', encoding='utf-8') as f:
    json.dump(merged_data, f, ensure_ascii=False, indent=4)
