import json
from pathlib import Path

FAILURE_FILE = Path("reports/latest_failure.json")


class FailureParser:
    def __init__(self, failure_file=FAILURE_FILE):
        self.failure_file = Path(failure_file)

    def load_failure(self):
        if not self.failure_file.exists():
            print("No failure report found.")
            return None

        with open(self.failure_file, "r", encoding="utf-8") as file:
            return json.load(file)

    def parse_failure(self):
        failure = self.load_failure()

        if not failure:
            return None

        print("\n================= TEST FAILURE ANALYSIS=============\n")

        print("Test:")
        print(failure["test_name"])

        print("\nStatus:")
        print(failure["outcome"])

        print("\nFailure Details")
        print(failure["longrepr"])

        print("\n==============================================")
        return failure

    def build_llm_payload(self):
        failure = self.load_failure() or {}
        traceback_text = failure.get("longrepr") or ""
        return {
            "test_name": failure.get("test_name"),
            "failed_url": failure.get("page_url"),
            "error_type": failure.get("error_type"),
            "error_message": failure.get("error_message"),
            "cleaned_traceback": traceback_text.strip(),
        }


def load_failure():
    return FailureParser().load_failure()


def parse_failure():
    return FailureParser().parse_failure()


if __name__ == "__main__":
    parse_failure()
