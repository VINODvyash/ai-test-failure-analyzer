import json
from pathlib import Path

FAILURE_FILE = Path("reports/latest_failure.json")

def load_failure():
    if not FAILURE_FILE.exists():
        print("No failure report found.")
        return None

    with open(FAILURE_FILE, "r", encoding="utf-8") as file:
        return json.load(file)

def parse_failure():
    failure = load_failure()

    if not failure:
        return

    print("\n================= TEST FAILURE ANALYSIS=============\n")

    print("Test:")
    print(failure["test_name"])

    print("\nStatus:")
    print(failure["outcome"])

    print("\nFailure Details")
    print(failure["longrepr"])

    print("\n==============================================")

if __name__ == "__main__":
    parse_failure()