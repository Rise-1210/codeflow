import json
import subprocess
import os
import sys
import argparse
import shutil
import re
import ast

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.utils import get_uuid

def parse_args():
    parser = argparse.ArgumentParser(description="Run harness evaluation on multi-turn problems")
    parser.add_argument('--model_name', type=str, required=True, help='Model name')
    parser.add_argument('--input_path', type=str, required=True, help='Path to input JSON file')
    parser.add_argument('--output_dir', type=str, required=True, help='Directory to save output results')
    parser.add_argument('--main_code', type=str, default='temp/main_code.py', help='Path to main code file')
    return parser.parse_args()

def extract_code(text):
    """
    智能代码提取逻辑：
    1. 优先提取 Markdown 代码块 (```python ... ```)
    2. 如果有多个代码块，将它们拼接 (应对 import 和 function 分开的情况)
    3. 如果没有代码块，尝试把整段文本作为代码 (应对模型忘了写 Markdown 的情况)
    """
    if not text:
        return ""
    

    pattern = r'```(?:python)?\s*(.*?)```'
    matches = re.findall(pattern, text, re.DOTALL | re.IGNORECASE)
    
    if matches:

        valid_blocks = [m.strip() for m in matches if m.strip()]
        return "\n\n".join(valid_blocks)

    return text.strip()

def check_syntax(code_str):
    """
    使用 AST 检查代码是否为合法的 Python 代码。
    非法代码（如纯文本）会被拦截。
    """
    if not code_str:
        return False
    try:
        ast.parse(code_str)
        return True
    except (SyntaxError, ValueError):
        return False

def main():
    args = parse_args()
    os.makedirs(args.output_dir, exist_ok=True)
    
    # 获取 temp 目录路径
    temp_dir = os.path.dirname(args.main_code)
    os.makedirs(temp_dir, exist_ok=True)

    try:
        json_data = json.load(open(args.input_path))
    except Exception as e:
        print(f"Error loading JSON: {e}")
        return

    print(f"Start harness evaluation: {len(json_data)} problems")
    
    # 定义非法 Python 对象的正则 (如 <function ... at 0x...>)
    INVALID_OBJ_PATTERN = re.compile(r"<[\w\s\.<>]+at\s0x[0-9a-fA-F]+>")

    for problem in json_data:
        uuid = problem.get("problem-id") or problem.get("task_id")
        subproblems = problem.get("subproblems", [])
        code_history = []
        
        for subproblem in subproblems:
            if not subproblem.get("generated"):
                continue

            # 【关键修改 1】使用增强版提取逻辑
            raw_generated = subproblem["generated"]
            extracted_code = extract_code(raw_generated)
            
            func_name = subproblem["name"]
   
            if check_syntax(extracted_code):
                code_history.append(extracted_code)
            else:

                pass
            
            test_cases = subproblem.get("test_code", [])
            if not test_cases:
                subproblem['harness_result'] = []
                subproblem['harness_debug'] = []
                continue

            result_list = []
            debug_list = []

     
            full_code_context = "\n".join(code_history)
            lib_name = "solution_lib"
            solution_lib_path = os.path.join(temp_dir, f"{lib_name}.py")
            
            with open(solution_lib_path, 'w', encoding='utf-8') as f:
                f.write(full_code_context)

            for i, test_case in enumerate(test_cases):
                input_str = test_case["input"]
                output_str = test_case["output"]

                # 脏数据过滤
                if INVALID_OBJ_PATTERN.search(input_str) or INVALID_OBJ_PATTERN.search(output_str):
                    result_list.append(-1)
                    debug_list.append({
                        "case_idx": i,
                        "input": input_str,
                        "expected": output_str,
                        "actual": "SKIPPED",
                        "status": "skipped",
                        "error": "Input/Output contains non-evaluable object repr"
                    })
                    continue

          
                driver_code = f"""
import sys
import os
import math
import collections
import itertools


sys.path.append({repr(os.path.abspath(temp_dir))})

try:

    from {lib_name} import *
    
  
    try:
        from {lib_name} import {func_name}
    except ImportError:
        pass
except Exception as e:

    print(f"IMPORT_ERROR: {{e}}")
    sys.exit(1)

def run_test():
    try:
  
        import datetime as _dt_module
        import pathlib as _pl_module
        
        eval_ctx = globals().copy()
        eval_ctx['datetime'] = _dt_module
        eval_ctx['pathlib'] = _pl_module
        eval_ctx['Path'] = _pl_module.Path
        eval_ctx['PosixPath'] = _pl_module.PosixPath
        eval_ctx['WindowsPath'] = _pl_module.WindowsPath

        input_raw = {repr(input_str)}
        expected_raw = {repr(output_str)}
        
        try:
            args, kwargs = eval(input_raw, eval_ctx)
            expected_output = eval(expected_raw, eval_ctx)
        except SyntaxError:
            print("EVAL_SYNTAX_ERROR")
            return
        except NameError as ne:
            print(f"EVAL_NAME_ERROR: {{ne}}")
            return

   
        actual_output = {func_name}(*args, **kwargs)

        if actual_output == expected_output:
            print("PASSED")
        else:
            if isinstance(actual_output, float) and isinstance(expected_output, float):
                if abs(actual_output - expected_output) < 1e-6:
                    print("PASSED")
                    return
            print(f"FAILED: Expected {{expected_output}}, got {{actual_output}}")
            sys.exit(1)

    except Exception as e:
        print(f"ERROR: {{e}}")
        sys.exit(1)

if __name__ == "__main__":
    run_test()
"""
                
                driver_file = args.main_code
                with open(driver_file, 'w', encoding='utf-8') as f:
                    f.write(driver_code)

                case_debug = {
                    "case_idx": i,
                    "input": input_str,
                    "expected": output_str,
                    "actual": "N/A",
                    "status": "wrong",
                    "error": ""
                }

                try:
                    result = subprocess.run(
                        [sys.executable, driver_file], 
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                    
                    stdout = result.stdout.strip()
                    stderr = result.stderr.strip()
                    
                    if result.returncode == 0 and "PASSED" in stdout:
                        result_list.append(1)
                        case_debug["status"] = 1
                        case_debug["actual"] = output_str
                    elif "IMPORT_ERROR" in stdout:
                        result_list.append(0)
                        case_debug["status"] = "syntax_error"
                        case_debug["error"] = stdout
                    elif "EVAL_SYNTAX_ERROR" in stdout:
                        result_list.append(-1)
                        case_debug["status"] = "skipped"
                        case_debug["error"] = "Input string syntax error"
                    else:
                        result_list.append(0)
                        case_debug["status"] = 0
                        case_debug["actual"] = stdout
                        case_debug["error"] = stderr if stderr else stdout

                except subprocess.TimeoutExpired:
                    result_list.append(0)
                    case_debug["status"] = "timeout"
                    case_debug["error"] = "Execution timed out"
                except Exception as e:
                    result_list.append(0)
                    case_debug["status"] = "error"
                    case_debug["error"] = str(e)

                debug_list.append(case_debug)

                if os.path.exists(driver_file):
                    os.remove(driver_file)

            if os.path.exists(solution_lib_path):
                os.remove(solution_lib_path)
                cache_dir = os.path.join(temp_dir, "__pycache__")
                if os.path.exists(cache_dir):
                    shutil.rmtree(cache_dir)

            subproblem['harness_result'] = result_list
            subproblem['harness_debug'] = debug_list

        file_name = os.path.join(args.output_dir, f"{uuid}.json")
        os.makedirs(os.path.dirname(file_name), exist_ok=True)
        
        with open(file_name, 'w', encoding='utf-8') as f:
            json.dump(problem, f, indent=4, ensure_ascii=False)
        print(f"Processed {uuid}: Saved to {file_name}")

if __name__ == '__main__':
    main()