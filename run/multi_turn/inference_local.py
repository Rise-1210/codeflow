import os
import sys
import argparse
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.local import ChatModel
from src.utils import (
    get_filenames_without_extension,
    extract_code,
    get_input,
    ensure_python_code_block,
    ensure_python_code_block_main,
    clean_code_block,
)


def main(args):
    os.makedirs(args.output_dir, exist_ok=True)

    data = json.load(open(args.input_file))
    chat_model = ChatModel(model_path=args.model_path, tensor_parallel_size=args.tensor_parallel_size)
    filename_list = get_filenames_without_extension(args.output_dir)

    for problem in data:
        problem_description_now = problem["problem-description"]
        subproblems = problem["subproblems"]
        problemid = problem["problem-id"]
        print(f"Solving Problem {problemid}...")

        overall_turns = problem["overall-turns"]

        if problemid in filename_list:
            continue

        turn_number = 1
        history = []

        for subproblem in subproblems:
            input_text = get_input(subproblem, turn_number, overall_turns, problem_description_now, history)
            turn_number += 1

            input_all = [
                {"role": "system", "content": "You are a Programming Expert. You always provide correct and reliable code solutions."},
                {"role": "user", "content": input_text}
            ]

            generated = chat_model.generate(input_all)
            output = generated[0].outputs[0].text

            if turn_number == overall_turns + 1:
                output = ensure_python_code_block_main(output, subproblem)
            else:
                output = ensure_python_code_block(output)

            subproblem.update({"original_output": output})

            code_output = extract_code(output)
            #print(output)
            code_output = clean_code_block(code_output)

            subproblem.update({"prompt": input_text})
            subproblem.update({"generated": code_output})

            history.append(code_output)

        output_path = os.path.join(args.output_dir, f"{problemid}.json")
        with open(output_path, "w") as f:
            json.dump(problem, f, ensure_ascii=False, indent=4)

        print(f"Processing completed, results saved to {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Multi-turn code generation")
    parser.add_argument("--model_path", type=str, required=True, help="Path to the model")
    parser.add_argument("--input_file", type=str, required=True, help="Path to the input JSON file")
    parser.add_argument("--output_dir", type=str, required=True, help="Directory to save output")
    parser.add_argument("--tensor_parallel_size", type=int, default=4, help="Tensor parallel size")

    args = parser.parse_args()
    main(args)
