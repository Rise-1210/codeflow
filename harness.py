import json
import subprocess
import os
import time
import re
from src.utils import get_uuid
import ast

INPUT_DIR="/mnt/public/code/wangzr/mds/multi-turn_code/output/test3/merged_output.json"
OUTPUT_DIR="/mnt/public/code/wangzr/mds/multi-turn_code/result_case_gold/test1"

# 读取 JSON 文件
json_data = json.load(open(INPUT_DIR))
uuid_set=get_uuid(OUTPUT_DIR)
for problem in json_data:
    
    subproblems=problem["subproblems"]
    temp_file = '/mnt/public/code/wangzr/mds/multi-turn_code/temp_code.py'
    assert_file='/mnt/public/code/wangzr/mds/multi-turn_code/assert_code.py'
    main_file='/mnt/public/code/wangzr/mds/multi-turn_code/main_code.py'
    uuid=problem["problem-id"]
    if uuid in uuid_set:
        continue
    turn_num=0
    overall_turns=problem["overall-turns"]
    for subproblem in subproblems:
        if not subproblem.get("generated"):
            continue
        code=subproblem["generated"]
        turn_num+=1
        result_list=[]
        if not subproblem.get("test_code"):
            continue
        #输入方式1

        if turn_num==overall_turns:
            function_name=subproblem["name"]
            input_=subproblem["test_code"][0]["input"]

            input_ = input_[2:-2]
            output= subproblem["test_code"][0]["output"]


            #print(input_list)
            #print(output_list)
            try:
                with open(temp_file, 'r') as temp:
                    content = temp.read()
            except:
                pass

            try:
                with open(main_file, 'w') as main:
                    main.write(content)
            except:
                pass
            code=subproblem["generated"]

            #print(code)
            name=subproblem["name"]
            with open(main_file, 'a') as file:
                file.write("\n")
                file.write(code)
                file.write("\n")
                file.write(f"{name}()")
            
            try:
                result = subprocess.run(
                    ["python3", main_file],
                    capture_output=True,
                    text=True,
                    check=True,
                    input=input_)  # 传递标准输入)
                result=result.stdout.strip()
                result+="\n"
                
                try:
                    output= output.strip("'")
                    assert result == output
                    result_list.append(1)
                except:
                    result_list.append(0)

            except:
                result_list.append("wrong")
            os.remove(main_file)

        else:    
            function_name=subproblem["name"]
            input_list=[]
            output_list=[]
            for i in subproblem["test_code"]:
                if i["input"].endswith(",)"):
                    i["input"] = i["input"].replace(",)", ")")
                input_list.append(i["input"])
                output_list.append(i["output"])
            #print(input_list)
            #print(output_list)
            with open(temp_file, 'a') as file:
                file.write("\n")
                file.write(code)
            for input_, output in zip(input_list, output_list):
                with open(assert_file, 'w') as file:
                    aaa="from temp_code import *"
                    file.write(aaa)
                    file.write("\n")
                    aaa=f"print({function_name}{input_})"
                    file.write(aaa)
                try:
                    result = subprocess.run(
                            ["python3", assert_file],
                            capture_output=True,
                            text=True,
                            check=True
                            )
                    result=result.stdout.strip()
                    try:
                        assert result==output
                        result_list.append(1)
                    except:
                        result_list.append(0)
  
                except:
                    result_list.append("wrong")
               


                os.remove(assert_file)
        subproblem.update({
                'harness_result': result_list
            })
            
    file_name = f"{OUTPUT_DIR}/{uuid}.json" 
        # print(samples)
    with open(file_name , 'w') as f:
        f.write(json.dumps(problem) + "\n")
    print("文件写入成功")
        #存答案

    try:
        os.remove(temp_file)
    except:
        pass