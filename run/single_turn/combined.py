import json
import os
import argparse
import shutil


def main(args):
    model_name = args.model_name
    folder_path = args.combined_dir
    harness=args.harness
    if harness:
        dir_output="harness"
    else:
        dir_output="inference"

    print(f"Read Path: {folder_path}")

    merged_data = []

    # Iterate over all JSON files in a folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            file_path = os.path.join(folder_path, filename)
            print(f"Reading: {filename}")
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                merged_data.append(data)

    with open(f"output/{dir_output}/{model_name}_single_turn.json", 'w', encoding='utf-8') as f:
        json.dump(merged_data, f, ensure_ascii=False, indent=4)

    if merged_data:
        print(f"Deleting folder: {folder_path}")
        shutil.rmtree(folder_path)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Merge JSON outputs")
    parser.add_argument("--model_name", type=str, required=True, help="Name of the model")
    parser.add_argument("--combined_dir", type=str, required=True, help="folder needed to combine")
    parser.add_argument("--harness", action="store_true", help="Flag for harness evaluation results")


    args = parser.parse_args()
    main(args)
