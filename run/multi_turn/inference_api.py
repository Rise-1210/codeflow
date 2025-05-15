import json
import os
import argparse
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.api import ChatModelAPI
from src.utils_api import get_filenames_without_extension, extract_code, get_input, ensure_python_code_block, ensure_python_code_block_main

def main(args):
    output_dir = os.path.join(args.output_base, args.model_name)
    os.makedirs(output_dir, exist_ok=True)

    with open(args.input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    chat_model = ChatModelAPI(api_url=args.api_url, api_key=args.api_key, model_name=args.model_name)

    filename_list = get_filenames_without_extension(output_dir)
    for problem in data:
        problem_description = problem["problem-description"]
        subproblems = problem["subproblems"]
        problem_id = problem["problem-id"]
        overall_turns = problem["overall-turns"]

        # Skip already processed problems
        if problem_id in filename_list:
            continue

        turn_number = 1
        history = []

        try:
            for subproblem in subproblems:
                input_text = get_input(subproblem, turn_number, overall_turns, problem_description, history)
                turn_number += 1

                generated = chat_model.generate(input_text)
                output = generated.choices[0].message.content

                if turn_number == overall_turns + 1:
                    output = ensure_python_code_block_main(output, subproblem)
                else:
                    output = ensure_python_code_block(output)

                subproblem.update({
                    "original_output": output,
                    "prompt": input_text,
                    "generated": extract_code(output)
                })
                history.append(extract_code(output))

            with open(os.path.join(output_dir, f"{problem_id}.json"), "w", encoding='utf-8') as f:
                json.dump(problem, f, ensure_ascii=False, indent=4)

        except Exception as e:
            print(f"[Skipped] Error occurred while processing problem_id={problem_id}: {e}")
            continue

        print(f"Completed. Result saved to {output_dir}/{problem_id}.json")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_name", type=str, required=True, help="Model name, used in output folder naming")
    parser.add_argument("--input_file", type=str, required=True, help="Input JSON file path")
    parser.add_argument("--output_dir", type=str, required=True,help="Base output directory path")
    parser.add_argument("--api_key", type=str, required=True, help="API key for the model")
    parser.add_argument("--api_url", type=str, required=True, help="URL of the inference API")
    args = parser.parse_args()

    main(args)
