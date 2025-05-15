import os
import sys
import json
import argparse

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.api import ChatModelAPI
from src.utils import (
    get_filenames_without_extension,
    extract_code,
    ensure_python_code_block,
    get_input_single,
)


def main(args):
    os.makedirs(args.output_dir, exist_ok=True)
    data = json.load(open(args.input_file))

    chat_model = ChatModelAPI(
        api_url=args.api_url,
        api_key=args.api_key,
        model_name=args.model_name
    )

    filename_list = get_filenames_without_extension(args.output_dir)

    for problem in data:
        problem_description_now = problem["problem-description"]
        subproblems = problem["subproblems"]
        problemid = problem["problem-id"]
        overall_turns = problem["overall-turns"]

        # Skip if already processed
        if problemid in filename_list:
            continue

        turn_number = 1
        history = ""
        for subproblem in subproblems:
            # Construct prompt based on turn number
            user_input = get_input_single(subproblem, turn_number, overall_turns, problem_description_now, history)
            turn_number += 1

            if turn_number != overall_turns + 1:
                history += "\n" + user_input
                continue

            print(user_input)

            # Call API for the final turn
            generated = chat_model.generate(user_input)

            # API output structure
            output = generated.choices[0].message.content
            output = ensure_python_code_block(output)

            subproblem.update({"original_output": output})
            code_output = extract_code(output)
            subproblem.update({"prompt": user_input})
            subproblem.update({"generated": code_output})

            print(output)

        # Save output to file
        output_file_path = os.path.join(args.output_dir, f"{problemid}.json")
        with open(output_file_path, "w") as f:
            json.dump(problem, f, ensure_ascii=False, indent=4)

        print(f"Finished: saved to {output_file_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Single-turn code generation using external API")

    parser.add_argument("--model_name", type=str, required=True, help="Model name")
    parser.add_argument("--input_file", type=str, required=True, help="Path to input JSON file")
    parser.add_argument("--output_dir", type=str, required=True, help="Directory to save outputs")
    parser.add_argument("--api_key", type=str, required=True, help="API key for authentication")
    parser.add_argument("--api_url", type=str, required=True, help="API endpoint URL")

    args = parser.parse_args()
    main(args)
