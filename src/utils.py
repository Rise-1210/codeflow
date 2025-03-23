import os
from prompt import *
def get_filenames_without_extension(folder_path):
    # 初始化一个空列表，用于保存文件名（不带后缀）
    filenames = []

    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder_path):
        # 检查是否是文件（排除文件夹）
        if os.path.isfile(os.path.join(folder_path, filename)):
            # 去掉文件的后缀名
            name_without_extension = os.path.splitext(filename)[0]
            # 将文件名添加到列表中
            filenames.append(name_without_extension)

    return filenames


import re

def replace_spaces_with_commas(text):
    # 使用正则表达式替换空格为逗号
    # 正则表达式解释：
    # (?<!,) 表示前面不是逗号
    # \s 表示空格
    # (?!,) 表示后面不是逗号
    result = re.sub(r'(?<!,)\s(?!,)', ',', text)
    return result


def get_uuid(dir):    
    files = os.listdir(dir)
    uuids_in_files = set()
    for file_name in files:
        if file_name.endswith(".json"):  # 只处理 .json 文件
            try:
                # 去掉 .json 后缀并转换为整数
                file_uuid = file_name[:-5]
                uuids_in_files.add(file_uuid)
            except ValueError:
                # 如果文件名不是数字，则忽略
                continue
    return uuids_in_files


def extract_code(pred):
    # 定义正则表达式模式
    patterns = [
        r'```python\n(.*?)\n```',  # 匹配 ```python\n...\n```
    ]

    # 用于存储最后一个匹配的代码块
    last_match = None

    # 遍历所有模式
    for pattern in patterns:
        # 使用 re.finditer 查找所有匹配项
        matches = list(re.finditer(pattern, pred, re.DOTALL))
        if matches:
            # 取最后一个匹配项
            last_match = matches[-1].group(1)

    # 如果没有匹配到任何内容，返回原始字符串
    if last_match is None:
        return pred.strip()

    # 返回最后一个匹配的代码块，并去除多余的空格
    return last_match.strip()


def get_input(subproblem,turn_number,overall_turns,problem_description_now,history):
    if history:
        history_all="\n\n".join(f'```python\n{item}\n```' for item in history)
    else:
        history_all=""
    
    #首轮输入
    if turn_number==1 and turn_number!=overall_turns:
        input=PROMPT1.format(
                problem_description=problem_description_now,
                name=subproblem["name"],
                statement=subproblem["statement"],
                )

    #最后一轮输入
    elif turn_number==overall_turns:
        if "dependencies" in subproblem and isinstance(subproblem["dependencies"], list) and subproblem["dependencies"]:#存在依赖且不为空
            input=PROMPT3.format(
                problem_description=problem_description_now,
                name=subproblem["name"],
                statement=subproblem["statement"],
                dependencies=subproblem["dependencies"],
                history=history_all
                    )
        else:
            input=PROMPT4.format(
                    problem_description=problem_description_now,
                    name=subproblem["name"],
                    statement=subproblem["statement"],
                    history=history_all
                    )
    #中间输入，有依赖
    elif "dependencies" in subproblem and isinstance(subproblem["dependencies"], list) and subproblem["dependencies"]:#存在依赖且不为空
        input=PROMPT2.format(
                problem_description=problem_description_now,
                name=subproblem["name"],
                statement=subproblem["statement"],
                dependencies=subproblem["dependencies"],
                history=history_all
                )
                
    #中间输入，没有依赖    
    else:
        input=PROMPT5.format(
                problem_description=problem_description_now,
                name=subproblem["name"],
                statement=subproblem["statement"],
                history=history_all
                )
    return input