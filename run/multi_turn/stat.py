import json
import argparse
from collections import defaultdict

def main(input_path, output_path):
    data = json.load(open(input_path))
    output_data = []
    pass_count = defaultdict(int)  # Store all-pass counts by "overall-turns"
    depth_count = defaultdict(int)  # Store pass-depth counts by "overall-depth"
    pass_depth_count = defaultdict(int)  # Store all-pass counts by turn/depth ratio

    for problem in data:
        over_depth = problem["overall-depth"]
        over_turn = problem["overall-turns"]
        subproblems = problem["subproblems"]
        right_turn = 0
        right_depth = 0
        for subproblem in subproblems:
            if not subproblem.get("harness_result"):
                continue
            if all(x == 1 for x in subproblem["harness_result"]):
                right_turn += 1
                right_depth = over_depth - subproblem["depth"]
            else:
                if right_depth == over_depth - subproblem["depth"]:
                    right_depth -= 1
                break
        if right_turn == over_turn:
            all_pass = 1
            wrong_turn = None
        else:
            all_pass = 0
            wrong_turn = right_turn + 1

        output_data.append({
            "problem-id": problem["problem-id"],
            "all-pass": all_pass,
            "pass-depth": right_depth,
            "wrong-turn": wrong_turn,
            "overall-depth": over_depth,
            "overall-turns": over_turn,
        })

        pass_count[f"turn-{over_turn}_pass1"] += all_pass
        pass_count[f"turn-{over_turn}_number"] += 1
        pass_depth_count[f"turn/depth-{over_turn / over_depth:.2f}_pass1"] += all_pass
        pass_depth_count[f"turn/depth-{over_turn / over_depth:.2f}_number"] += 1
        depth_count[f"depth-{over_depth}_pass-depth"] += right_depth
        depth_count[f"depth-{over_depth}_number"] += 1

    depth_count = {
        key.replace("_pass-depth", ""): {
            "pass-depth": depth_count[key] / depth_count.get(key.replace("_pass-depth", "_number"), 1),
            "number": depth_count.get(key.replace("_pass-depth", "_number"), 1)
        }
        for key in depth_count if "_pass-depth" in key
    }

    pass_count = {
        key.replace("_pass1", ""): {
            "pass1": pass_count[key] / pass_count.get(key.replace("_pass1", "_number"), 1),
            "number": pass_count.get(key.replace("_pass1", "_number"), 1)
        }
        for key in pass_count if "_pass1" in key
    }

    pass_depth_count = {
        key.replace("_pass1", ""): {
            "pass1": pass_depth_count[key] / pass_depth_count.get(key.replace("_pass1", "_number"), 1),
            "number": pass_depth_count.get(key.replace("_pass1", "_number"), 1)
        }
        for key in pass_depth_count if "_pass1" in key
    }

    i = len(output_data)
    all_pass1_total = sum(o["all-pass"] for o in output_data)
    all_depth_total = sum(o["pass-depth"] for o in output_data)

    all_pass1 = all_pass1_total / i
    all_depth = all_depth_total / i

    summary = {
        "overall": {
            "all_pass1": round(all_pass1, 8),
            "all_depth": round(all_depth, 8),
            "all_number": i
        },
        "turn": {**pass_count},
        "depth": {**depth_count},
        "turn/depth": {**pass_depth_count},
    }

    with open(output_path, "w") as f:
        json.dump({"summary": summary, "detail": output_data}, f, indent=4)

    print(f"Results saved to {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Summarize harness results.")
    parser.add_argument('--input', type=str, required=True, help="Path to input JSON file")
    parser.add_argument('--output', type=str, required=True, help="Path to output JSON file")
    args = parser.parse_args()

    main(args.input, args.output)
