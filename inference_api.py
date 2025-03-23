import json
from src.api import ChatModelAPI
from src.utils import get_filenames_without_extension,extract_code,get_input
#修改输入输出地址和模型地址
OUTPUT_DIR="/mnt/public/code/wangzr/mds/multi-turn_code/output/test3"
INPUT_DIR="/mnt/public/code/wangzr/mds/multi-turn_code/codeflowbench_sample.json"

data = json.load(open(INPUT_DIR))
# 初始化 ChatModel
API_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
API_KEY = " "
Model_Name="deepseek-v3"
chat_model = ChatModelAPI(api_url=API_URL,api_key=API_KEY,model_name=Model_Name)


filename_list=get_filenames_without_extension(OUTPUT_DIR)
for problem in data:

    problem_description_now=problem["problem-description"]
    subproblems=problem["subproblems"]
    problemid=problem["problem-id"]
    overall_turns=problem["overall-turns"]
    #避免断开后重复生成
    if problemid in filename_list:
        continue

    turn_number=1
    history = []  # 用于存储对话历史
    for subproblem in subproblems:

        #根据不同的条件给出不同的prompt
        input=get_input(subproblem,turn_number,overall_turns,problem_description_now,history)
        
        turn_number+=1

        generated = chat_model.generate(input)

        #不同的api输出不一样 需要修改output
        #print(generated)
        output=generated.choices[0].message.content


        output=extract_code(output) 
        print(output) 

        subproblem.update({"prompt": input})
        subproblem.update({"generated": output})

        history.append(output)
        
    with open(f"{OUTPUT_DIR}/{problemid}.json", "w") as f:
        json.dump(problem, f, ensure_ascii=False, indent=4)

    print(f"处理完成，结果已保存到 {OUTPUT_DIR}/{problemid}.json")


 