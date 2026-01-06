import json
import subprocess
import os
import sys
import argparse
import re
import ast

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# Assuming has_print is available in src.utils based on previous context
# If not, you can use the simple regex fallback provided in the logic below.
from src.utils import get_uuid, has_print 

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

def run_harness(input_path, output_dir, model_name, main_code_path):
    os.makedirs(output_dir, exist_ok=True)
    
    # Ensure temp directory exists
    temp_dir = os.path.dirname(main_code_path)
    if temp_dir:
        os.makedirs(temp_dir, exist_ok=True)

    print("Running harness (Single-Turn)...")
    try:
        json_data = json.load(open(input_path, encoding='utf-8'))
    except Exception as e:
        print(f"Error loading JSON: {e}")
        return

    uuid_set = get_uuid(output_dir)

    for problem in json_data:
        uuid = problem.get("problem-id") or problem.get("task_id")
        if uuid in uuid_set:
            continue

        subproblems = problem.get("subproblems", [])
        
        # In single-turn datasets, usually turn_num isn't strictly tracked, 
        # but we iterate to be safe.
        
        for subproblem in subproblems:
            if not subproblem.get("generated"):
                continue

            # 1. Extract and Validate Code
            raw_code = subproblem["generated"]
            code = extract_code(raw_code)
            name = subproblem["name"]
            result_list = []

            if not check_syntax(code):
                # Mark as 0 if syntax is invalid
                subproblem.update({'harness_result': [0]})
                continue

            if not subproblem.get("test_code"):
                subproblem.update({'harness_result': []})
                continue

            # 2. Prepare Input/Output
            # Legacy logic to clean input string for stdin injection
            input_raw = subproblem["test_code"][0]["input"]
            if isinstance(input_raw, str):
                input_ = input_raw.strip("[]'").replace('\\n', '\n')
            else:
                input_ = str(input_raw)
            
            # Normalize spaces (legacy behavior)
            input_ = ' '.join(input_.split())
            # print(f"Processing {name}, Input: {input_}")

            output_raw = subproblem["test_code"][0]["output"]
            output = output_raw.replace('\\n', '\n') if isinstance(output_raw, str) else str(output_raw)

            # 3. Construct Execution File
            try:
                with open(main_code_path, 'w', encoding='utf-8') as main:
                    main.write("import sys\n")
                    main.write(code)
                    
                    # Decide how to call the function
                    # If the model code prints the result itself, just call it.
                    # Otherwise, wrap it in print().
                    if has_print(code):
                        main.write(f"\n{name}()")
                    else:
                        main.write(f"\nprint({name}())")
            except Exception as e:
                print(f"Error writing temp file: {e}")
                subproblem.update({'harness_result': [0]})
                continue

            # 4. Execute
            try:
                result = subprocess.run(
                    [sys.executable, main_code_path], # Use sys.executable for environment safety
                    capture_output=True,
                    text=True,
                    input=input_,
                    timeout=2
                )
                
                # Capture and clean stdout
                stdout_res = result.stdout.strip()
                
                # 5. Compare Results
                if result.returncode != 0:
                    # Check if stdout matches despite error (sometimes simple prints pass before crash)
                    if stdout_res == output.strip():
                        result_list.append(1)
                    else:
                        result_list.append(0) # Mark as 0 instead of "wrong"
                else:
                    # Loose comparison to handle potential extra quotes from raw strings
                    expected = output.strip()
                    if stdout_res == expected or stdout_res.strip("'") == expected.strip("'"):
                        result_list.append(1)
                    else:
                        result_list.append(0)

            except subprocess.TimeoutExpired:
                result_list.append(0) # Timeout counts as failure
            except Exception as e:
                print(f"Execution error: {e}")
                result_list.append(0)

            # Cleanup
            if os.path.exists(main_code_path):
                os.remove(main_code_path)

            subproblem.update({
                'harness_result': result_list
            })

        # Save results
        file_name = os.path.join(output_dir, f"{uuid}.json")
        try:
            with open(file_name, 'w', encoding='utf-8') as f:
                f.write(json.dumps(problem, ensure_ascii=False) + "\n")
            print(f"Saved to {file_name}")
        except Exception as e:
            print(f"Error saving result for {uuid}: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run harness testing on generated code (Single Turn)")

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