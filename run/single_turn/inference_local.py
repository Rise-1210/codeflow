import os
import json
import sys
import argparse

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.local import ChatModel
from src.utils import (
    get_filenames_without_extension,
    extract_code,
    get_input_single,
    ensure_python_code_block,
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
        overall_turns = problem["overall-turns"]

        # Skip already processed problems
        if problemid in filename_list:
            continue

        history = ""
        turn_number = 1
        for subproblem in subproblems:
            # Construct the prompt based on turn number and overall context
            user_input = get_input_single(subproblem, turn_number, overall_turns, problem_description_now, history)
            turn_number += 1

            # Accumulate context until final turn
            if turn_number != overall_turns + 1:
                history += "\n" + user_input
                continue

            # Final turn: complete generation
            input_all = [
                {"role": "system", "content": "You are a Programming Expert. You always provide correct and reliable code solutions."},
                {"role": "user", "content": user_input}
            ]
            generated = chat_model.generate(input_all)
            output = generated[0].outputs[0].text

            # Ensure the output is wrapped in a code block
            output = ensure_python_code_block(output)
            subproblem.update({"original_output": output})

            # Extract code from generated output
            code_output = extract_code(output)
            subproblem.update({"prompt": user_input})
            subproblem.update({"generated": code_output})

        with open(f"{args.output_dir}/{problemid}.json", "w") as f:
            json.dump(problem, f, ensure_ascii=False, indent=4)

        print(f"Finished: saved to {args.output_dir}/{problemid}.json")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Single-turn code generation inference")

    parser.add_argument("--model_path", type=str, required=True, help="Path to the model")
    parser.add_argument("--input_file", type=str, required=True, help="Path to input JSON file")
    parser.add_argument("--output_dir", type=str, required=True, help="Directory to save outputs")
    parser.add_argument("--tensor_parallel_size", type=int, default=1, help="Tensor parallel size")

    args = parser.parse_args()
    main(args)
