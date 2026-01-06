import json
import subprocess
import os
import sys
import argparse
import re
import ast
import shutil

# Add parent directory to path to import src.utils
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.utils import get_uuid, has_print

def parse_args():
    parser = argparse.ArgumentParser(description="Run harness evaluation on multi-turn problems (Legacy Mode)")
    parser.add_argument('--model_name', type=str, required=True, help='Model name')
    parser.add_argument('--input_path', type=str, required=True, help='Path to input JSON file')
    parser.add_argument('--output_dir', type=str, required=True, help='Directory to save output results')
    parser.add_argument('--temp_code', type=str, default='temp/temp_code.py', help='Path to temp code file')
    parser.add_argument('--assert_code', type=str, default='temp/assert_code.py', help='Path to assert code file')
    parser.add_argument('--main_code', type=str, default='temp/main_code.py', help='Path to main code file')
    return parser.parse_args()

def extract_code(text):
    """
    Extracts Python code from Markdown code blocks.
    If no blocks are found, returns the original text stripped of whitespace.
    """
    if not text:
        return ""
    # Pattern to match ```python ... ``` or ``` ... ```
    pattern = r'```(?:python)?\s*(.*?)```'
    matches = re.findall(pattern, text, re.DOTALL | re.IGNORECASE)
    if matches:
        valid_blocks = [m.strip() for m in matches if m.strip()]
        return "\n\n".join(valid_blocks)
    return text.strip()

def check_syntax(code_str):
    """
    Checks if the code is valid Python syntax using AST.
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
    
    # Create temp directory if it doesn't exist
    temp_dir = os.path.dirname(args.temp_code)
    if temp_dir:
        os.makedirs(temp_dir, exist_ok=True)

    try:
        json_data = json.load(open(args.input_path, encoding='utf-8'))
    except Exception as e:
        print(f"Error loading JSON input: {e}")
        return

    print(f"Start harness evaluation: {len(json_data)} problems")
    uuid_set = get_uuid(args.output_dir)

    for problem in json_data:
        uuid = problem.get("problem-id") or problem.get("task_id")
        
        # Skip if already processed
        if uuid in uuid_set:
            continue

        # Clean up temp files before processing a new problem
        for file_path in [args.temp_code, args.assert_code, args.main_code]:
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except OSError:
                    pass

        subproblems = problem.get("subproblems", [])
        turn_num = 0
        overall_turns = problem.get("overall-turns", 0)

        for subproblem in subproblems:
            if not subproblem.get("generated"):
                continue

            # 1. Enhanced Code Extraction
            raw_generated = subproblem["generated"]
            code = extract_code(raw_generated)
            turn_num += 1
            result_list = []

            # 2. Syntax Check
            if not check_syntax(code):
                # If code is invalid, mark all tests as 0 (fail)
                test_len = len(subproblem.get("test_code", []))
                subproblem['harness_result'] = [0] * (test_len if test_len > 0 else 1)
                continue

            if not subproblem.get("test_code"):
                subproblem['harness_result'] = []
                continue

            # --- Logic for the Last Turn (ACM Style / Script Execution) ---
            if turn_num == overall_turns:
                function_name = subproblem["name"]
                # print(f"Processing Last Turn: {function_name}")

                # Prepare Input
                # Note: Keeping the original string manipulation logic for compatibility
                # with the dataset's specific formatting.
                input_raw = subproblem["test_code"][0]["input"]
                if isinstance(input_raw, str):
                    input_ = input_raw.strip("[]'").replace('\\n', '\n')
                else:
                    input_ = str(input_raw)
                
                input_ = ' '.join(input_.split()) # Normalize spaces
                
                output_raw = subproblem["test_code"][0]["output"]
                output = output_raw.replace('\\n', '\n') if isinstance(output_raw, str) else str(output_raw)

                # Read context from previous turns
                content = ""
                if os.path.exists(args.temp_code):
                    try:
                        with open(args.temp_code, 'r', encoding='utf-8') as temp:
                            content = temp.read().rstrip()
                    except Exception:
                        content = ""

                # Write main execution file
                try:
                    with open(args.main_code, 'w', encoding='utf-8') as main:
                        main.write(content)
                        if content and not content.endswith('\n'):
                            main.write("\n")
                        
                        main.write("\nimport sys\n")
                        main.write(code + "\n")
                        
                        # Determine call style based on whether the model prints output itself
                        if has_print(code):
                            main.write(f"{function_name}()")
                        else:
                            main.write(f"print({function_name}())")
                except Exception as e:
                    print(f"Error writing main code: {e}")
                    subproblem['harness_result'] = [0]
                    continue

                # Execute
                try:
                    result = subprocess.run(
                        [sys.executable, args.main_code], # Use sys.executable for safety
                        capture_output=True,
                        text=True,
                        input=input_,
                        timeout=5
                    )
                    
                    # Check return code
                    if result.returncode != 0:
                        # Handle CalledProcessError logic manually to capture output if any
                        stdout_res = result.stdout.strip()
                        if stdout_res == output.strip():
                            result_list.append(1)
                        else:
                            result_list.append(0)
                    else:
                        stdout_res = result.stdout.strip()
                        # Allow loose comparison (handling extra quotes often returned by simple prints)
                        if stdout_res == output.strip() or stdout_res.strip("'") == output.strip("'"):
                            result_list.append(1)
                        else:
                            result_list.append(0)

                except subprocess.TimeoutExpired:
                    result_list.append(0) # Mark as 0 instead of "wrong" for consistency
                except Exception:
                    result_list.append(0)

                # Cleanup main code
                if os.path.exists(args.main_code):
                    os.remove(args.main_code)

            # --- Logic for Intermediate Turns (Function Call Style) ---
            else:
                function_name = subproblem["name"]
                # print(f"Processing Intermediate Turn: {function_name}")
                
                input_list = []
                output_list = []
                
                # Preprocess test cases
                for i in subproblem["test_code"]:
                    inp = i["input"]
                    # Legacy replacement logic
                    if isinstance(inp, str):
                        inp = inp.replace(",)", ")")
                    input_list.append(inp)
                    output_list.append(i["output"])

                # Append current turn code to temp history
                with open(args.temp_code, 'a', encoding='utf-8') as file:
                    file.write("\n" + code)

                # Run assertions for each test case
                for inp, outp in zip(input_list, output_list):
                    with open(args.assert_code, 'w', encoding='utf-8') as file:
                        # Generate a runner script
                        # Note: This relies on temp_code.py being importable
                        file.write("import sys\n")
                        file.write(f"sys.path.append('{os.path.abspath(temp_dir)}')\n")
                        
                        # Try to import from temp_code (module name based on filename)
                        module_name = os.path.splitext(os.path.basename(args.temp_code))[0]
                        file.write(f"from {module_name} import *\n")
                        file.write(f"print({function_name}{inp})")

                    try:
                        result = subprocess.run(
                            [sys.executable, args.assert_code],
                            capture_output=True,
                            text=True,
                            timeout=5
                        )
                        
                        if result.returncode != 0:
                            result_list.append(0)
                        else:
                            actual = result.stdout.strip()
                            expected = str(outp).strip()
                            # Loose comparison
                            if actual == expected or actual.strip("'") == expected.strip("'"):
                                result_list.append(1)
                            else:
                                result_list.append(0)

                    except subprocess.TimeoutExpired:
                        result_list.append(0)
                    except Exception:
                        result_list.append(0)

                    if os.path.exists(args.assert_code):
                        os.remove(args.assert_code)

            subproblem['harness_result'] = result_list

        # Save result for the problem
        file_name = os.path.join(args.output_dir, f"{uuid}.json")
        try:
            with open(file_name, 'w', encoding='utf-8') as f:
                json.dump(problem, f, ensure_ascii=False)
            print(f"Processed {uuid}")
        except Exception as e:
            print(f"Failed to save {uuid}: {e}")

        # Cleanup temp history file for the next problem
        if os.path.exists(args.temp_code):
            os.remove(args.temp_code)

if __name__ == '__main__':
    main()