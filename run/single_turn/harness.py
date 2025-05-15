import json
import subprocess
import os
import sys
import argparse

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.utils import get_uuid

def run_harness(input_path, output_dir, model_name, main_code_path):
    os.makedirs(output_dir, exist_ok=True)

    print("Running harness...")
    json_data = json.load(open(input_path))
    uuid_set = get_uuid(output_dir)

    for problem in json_data:
        uuid = problem["problem-id"]
        if uuid in uuid_set:
            continue

        subproblems = problem["subproblems"]
        overall_turns = problem["overall-turns"]
        turn_num = 0

        for subproblem in subproblems:
            if not subproblem.get("generated"):
                continue

            code = subproblem["generated"]
            name = subproblem["name"]
            turn_num += 1
            result_list = []

            if not subproblem.get("test_code"):
                continue

            function_name = subproblem["name"]
            input_ = subproblem["test_code"][0]["input"]
            input_ = input_.strip("[]'")
            input_ = input_.replace('\\n', '\n')
            input_ = ' '.join(input_.split())

            print(f"input_: {input_}")
            output = subproblem["test_code"][0]["output"]
            output = output.replace('\\n', '\n')

            with open(main_code_path, 'w') as main:
                main.write(code)
                main.write(f"\n{name}()")

            try:
                result = subprocess.run(
                    ["python3", main_code_path],
                    capture_output=True,
                    text=True,
                    check=True,
                    input=input_,
                    timeout=2
                )
                result = result.stdout.strip() + "\n"
                try:
                    output = output.strip("'")
                    assert result == output
                    result_list.append(1)
                except:
                    result_list.append(0)
            except subprocess.TimeoutExpired:
                result_list.append("wrong")
            except subprocess.CalledProcessError as e:
                if e.stdout == output:
                    result_list.append(1)
                else:
                    result_list.append("wrong")
            except:
                result_list.append("wrong")

            os.remove(main_code_path)

            subproblem.update({
                'harness_result': result_list
            })

        file_name = os.path.join(output_dir, f"{uuid}.json")
        with open(file_name, 'w') as f:
            f.write(json.dumps(problem) + "\n")
        print(f"Saved to {file_name}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run harness testing on generated code")

    parser.add_argument("--model_name", type=str, required=True, help="Model name")
    parser.add_argument("--input_path", type=str, required=True, help="Path to the input JSON file")
    parser.add_argument("--output_dir", type=str, required=True, help="Directory to save harness results")
    parser.add_argument("--main_code", type=str, default="temp/main_code.py", help="Path to main code file")

    args = parser.parse_args()

    run_harness(
        input_path=args.input_path,
        output_dir=args.output_dir,
        model_name=args.model_name,
        main_code_path=args.main_code,
    )
