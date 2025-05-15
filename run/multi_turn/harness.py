import json
import subprocess
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import argparse
from src.utils import get_uuid, has_print

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def parse_args():
    parser = argparse.ArgumentParser(description="Run harness evaluation on multi-turn problems")
    parser.add_argument('--model_name', type=str, required=True, help='Model name')
    parser.add_argument('--input_path', type=str, required=True, help='Path to input JSON file')
    parser.add_argument('--output_dir', type=str, required=True, help='Directory to save output results')
    parser.add_argument('--temp_code', type=str, default='temp/temp_code.py', help='Path to temp code file')
    parser.add_argument('--assert_code', type=str, default='temp/assert_code.py', help='Path to assert code file')
    parser.add_argument('--main_code', type=str, default='temp/main_code.py', help='Path to main code file')
    return parser.parse_args()

def main():
    args = parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    json_data = json.load(open(args.input_path))
    print("Start harness evaluation")
    uuid_set = get_uuid(args.output_dir)

    for problem in json_data:
        problem_id = problem["problem-id"]
        subproblems = problem["subproblems"]

        for file_path in [args.temp_code, args.assert_code, args.main_code]:
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except Exception as e:
                    print(f"Failed to delete temp file {file_path}: {e}")

        uuid = problem["problem-id"]
        if uuid in uuid_set:
            continue

        turn_num = 0
        overall_turns = problem["overall-turns"]

        for subproblem in subproblems:
            if not subproblem.get("generated"):
                continue

            code = subproblem["generated"]
            turn_num += 1
            result_list = []

            if not subproblem.get("test_code"):
                continue

            if turn_num == overall_turns:
                function_name = subproblem["name"]
                print(function_name)

                input_ = subproblem["test_code"][0]["input"].strip("[]'").replace('\\n', '\n')
                input_ = ' '.join(input_.split())
                print(f"input_: {input_}")

                output = subproblem["test_code"][0]["output"].replace('\\n', '\n')

                try:
                    with open(args.temp_code, 'r') as temp:
                        content = temp.read().rstrip()
                except:
                    content = ""

                try:
                    with open(args.main_code, 'w') as main:
                        main.write(content)
                        if not content.endswith('\n'):
                            main.write("\n")
                except:
                    pass

                name = subproblem["name"]
                if has_print(code):
                    with open(args.main_code, 'a') as file:
                        file.write("\nimport sys\n")
                        file.write(code + "\n")
                        file.write(f"{name}()")
                else:
                    with open(args.main_code, 'a') as file:
                        file.write("\nimport sys\n")
                        file.write(code + "\n")
                        file.write(f"print({name}())")

                try:
                    result = subprocess.run(
                        ["python3", args.main_code],
                        capture_output=True,
                        text=True,
                        check=True,
                        input=input_,
                        timeout=5
                    )
                    result = result.stdout.strip() + "\n"

                    try:
                        if result.strip("'") == output.strip("'"):
                            result_list.append(1)
                            print(f"result1: {result}")
                        else:
                            result_list.append(0)
                            print(f"result0: {result}")
                    except:
                        result_list.append(0)

                except subprocess.TimeoutExpired:
                    result_list.append("wrong")
                except subprocess.CalledProcessError as e:
                    if e.stdout.strip() == output.strip():
                        result_list.append(1)
                    else:
                        result_list.append("wrong")
                except:
                    result_list.append("wrong")

                os.remove(args.main_code)

            else:
                function_name = subproblem["name"]
                print(function_name)
                input_list = []
                output_list = []
                for i in subproblem["test_code"]:
                    i["input"] = i["input"].replace(",)", ")")
                    input_list.append(i["input"])
                    output_list.append(i["output"])

                with open(args.temp_code, 'a') as file:
                    file.write("\n" + code)

                for input_, output in zip(input_list, output_list):
                    with open(args.assert_code, 'w') as file:
                        file.write("from temp_code import *\n")
                        file.write(f"print({function_name}{input_})")

                    try:
                        result = subprocess.run(
                            ["python3", args.assert_code],
                            capture_output=True,
                            text=True,
                            check=True,
                            timeout=5
                        )
                        result = result.stdout.strip()
                        result_list.append(1 if result == output else 0)
                    except subprocess.TimeoutExpired:
                        result_list.append("wrong")
                    except:
                        result_list.append("wrong")

                    os.remove(args.assert_code)

            subproblem.update({ 'harness_result': result_list })

        file_name = f"{args.output_dir}/{uuid}.json"
        with open(file_name, 'w') as f:
            f.write(json.dumps(problem) + "\n")
        print("File written successfully")

        try:
            os.remove(args.temp_code)
        except:
            pass

if __name__ == '__main__':
    main()