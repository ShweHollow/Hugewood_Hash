import argparse
import os
from hugewood_hash import build_canonical_input, compute_hugewood_hash, compute_diff
import json

SAVE_PATH = "hugewood_hash_output.json"
PREVIOUS_PATH = "hugewood_hash_prev.json"
DIFF_PATH = "hugewood_hash_diff.json"

def init():
    print("Initializing Hugewood Hash...")
    canonical_input = build_canonical_input()
    hugewood_hash = compute_hugewood_hash(canonical_input)
    with open(SAVE_PATH, "w") as f:
        json.dump({"timestamp": canonical_input["timestamp"], "hash": hugewood_hash, "input_tree": canonical_input}, f, indent=2)
    with open(PREVIOUS_PATH, "w") as f:
        json.dump({"timestamp": canonical_input["timestamp"], "hash": hugewood_hash, "input_tree": canonical_input}, f, indent=2)
    print("Initial hash:", hugewood_hash)

def update():
    print("Updating Hugewood Hash...")
    canonical_input = build_canonical_input()
    hugewood_hash = compute_hugewood_hash(canonical_input)
    with open(SAVE_PATH, "w") as f:
        json.dump({"timestamp": canonical_input["timestamp"], "hash": hugewood_hash, "input_tree": canonical_input}, f, indent=2)
    print("New hash:", hugewood_hash)

    if os.path.exists(PREVIOUS_PATH):
        with open(PREVIOUS_PATH, "r") as f:
            previous_data = json.load(f)
        diff = compute_diff(canonical_input, previous_data.get("input_tree", {}))
        with open(DIFF_PATH, "w") as f:
            json.dump(diff, f, indent=2)
        print("\nChanges detected:")
        print(json.dumps(diff, indent=2))

    with open(PREVIOUS_PATH, "w") as f:
        json.dump({"timestamp": canonical_input["timestamp"], "hash": hugewood_hash, "input_tree": canonical_input}, f, indent=2)

def diff():
    if not os.path.exists(DIFF_PATH):
        print("No diff file found. Please run `hugewood update` first.")
        return
    with open(DIFF_PATH, "r") as f:
        diff_data = json.load(f)
    print("\nCurrent diff:")
    print(json.dumps(diff_data, indent=2))

def main():
    parser = argparse.ArgumentParser(description="Hugewood Hash CLI")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("init", help="Initialize the Hugewood Hash")
    subparsers.add_parser("update", help="Update the Hugewood Hash")
    subparsers.add_parser("diff", help="View the current diff")

    args = parser.parse_args()

    if args.command == "init":
        init()
    elif args.command == "update":
        update()
    elif args.command == "diff":
        diff()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
