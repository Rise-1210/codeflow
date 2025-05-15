import json
from collections import defaultdict
import argparse

def main(input_path, output_path):
    data = json.load(open(input_path))
    output_data = []
    pass_count = defaultdict(int)  # Count of all-pass by turn
    depth_count = defaultdict(int)  # Count of all-pass by depth
    pass_depth_count = defaultdict(int)  # Count of all-pass by turn/depth ratio

    for problem in data:
        over_depth = problem["overall-depth"]
        over_turn = problem["overall-turns"]
        subproblems = problem["subproblems"]
        all_pass = 0
        for subproblem in subproblems:
            if not subproblem.get("harness_result"):
                continue
            if all(x == 1 for x in subproblem["harness_result"]):
                all_pass = 1
            else:
                all_pass = 0

            output_data.append({
                "problem-id": problem["problem-id"],
                "all-pass": all_pass,
                "overall-depth": over_depth,
                "overall-turns": over_turn,
            })

        pass_count[f"turn-{over_turn}_pass1"] += all_pass
        pass_count[f"turn-{over_turn}_number"] += 1
        depth_count[f"depth-{over_depth}_pass1"] += all_pass
        depth_count[f"depth-{over_depth}_number"] += 1
        pass_depth_count[f"turn/depth-{over_turn / over_depth:.2f}_pass1"] += all_pass
        pass_depth_count[f"turn/depth-{over_turn / over_depth:.2f}_number"] += 1

    pass_count = {
        key.replace("_pass1", ""): {
            "pass1": pass_count[key] / pass_count.get(key.replace("_pass1", "_number"), 1),
            "number": pass_count.get(key.replace("_pass1", "_number"), 1)
        }
        for key in pass_count if "_pass1" in key
    }
    depth_count = {
        key.replace("_pass1", ""): {
            "pass1": depth_count[key] / depth_count.get(key.replace("_pass1", "_number"), 1),
            "number": depth_count.get(key.replace("_pass1", "_number"), 1)
        }
        for key in depth_count if "_pass1" in key
    }
    pass_depth_count = {
        key.replace("_pass1", ""): {
            "pass1": pass_depth_count[key] / pass_depth_count.get(key.replace("_pass1", "_number"), 1),
            "number": pass_depth_count.get(key.replace("_pass1", "_number"), 1)
        }
        for key in pass_depth_count if "_pass1" in key
    }

    i = 0
    all_pass1_total = 0
    for output in output_data:
        i += 1
        all_pass1_total += output["all-pass"]

    all_pass1 = all_pass1_total / i if i else 0

    summary = {
        "overall": {
            "all_pass1": all_pass1,
            "all_number": i
        },
        "turn": pass_count,
        "depth": depth_count,
        "turn/depth": pass_depth_count,
    }

    with open(output_path, "w") as f:
        json.dump({"summary": summary, "detail": output_data}, f, indent=4)

    print(f"Results saved to {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate and summarize harness results")
    parser.add_argument("--input", type=str, required=True, help="Path to input JSON file")
    parser.add_argument("--output", type=str, required=True, help="Path to output JSON file")

    args = parser.parse_args()
    main(args.input, args.output)
