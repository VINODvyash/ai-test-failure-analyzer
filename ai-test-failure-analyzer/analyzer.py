import json
from pathlib import Path


FAILURE_FILE = Path("reports/latest_failure.json")


def load_failure():
    if not FAILURE_FILE.exists():
        print("No failure report found.")
        return None

    with open(FAILURE_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def classify_failure(longrepr):
    if "AssertionError" in longrepr:
        return "Assertion Error"

    if "fixture" in longrepr and "not found" in longrepr:
        return "Missing Pytest Fixture"

    if "ModuleNotFoundError" in longrepr:
        return "Missing Python Module"

    if "NameError" in longrepr:
        return "Undefined Variable"

    if "Timeout" in longrepr or "TimeoutError" in longrepr:
        return "Timeout Error"

    if "404" in longrepr:
        return "HTTP 404 / Endpoint Not Found"

    if "401" in longrepr:
        return "HTTP 401 / Authentication Error"

    if "403" in longrepr:
        return "HTTP 403 / Permission Error"

    return "Unknown Failure"


def analyze_failure(longrepr, failure_type):
    if failure_type == "Assertion Error":

        if "assert" in longrepr and " in " in longrepr:
            return (
                "The actual value did not match the expected value. "
                "The test assertion appears to contain an incorrect "
                "expectation."
            )

        return "The test assertion failed."


    if failure_type == "Missing Pytest Fixture":
        return (
            "Pytest could not find the requested fixture. "
            "Check that the required plugin or fixture is installed "
            "and available."
        )


    if failure_type == "Missing Python Module":
        return (
            "A required Python module is missing. "
            "Check the dependency installation."
        )


    if failure_type == "Undefined Variable":
        return (
            "The test or application references a variable that "
            "has not been defined."
        )


    if failure_type == "Timeout Error":
        return (
            "The operation did not complete within the allowed time. "
            "Check the application response, locator, network, or timeout."
        )


    if failure_type == "HTTP 404 / Endpoint Not Found":
        return (
            "The requested endpoint or page could not be found. "
            "Check the URL and routing configuration."
        )


    if failure_type == "HTTP 401 / Authentication Error":
        return (
            "Authentication failed or credentials/token are missing."
        )


    if failure_type == "HTTP 403 / Permission Error":
        return (
            "The request was understood but access was denied."
        )


    return "The analyzer could not determine the root cause."


def parse_failure():

    failure = load_failure()

    if not failure:
        return

    test_name = failure["test_name"]
    outcome = failure["outcome"]
    longrepr = failure["longrepr"]

    failure_type = classify_failure(longrepr)

    root_cause = analyze_failure(longrepr, failure_type)

    print("\n================ TEST FAILURE ANALYSIS ================")

    print("\nTest:")
    print(test_name)

    print("\nStatus:")
    print(outcome)

    print("\nFailure Type:")
    print(failure_type)

    print("\nRoot Cause Analysis:")
    print(root_cause)

    print("\nOriginal Failure:")
    print(longrepr)

    print("\n========================================================")


if __name__ == "__main__":
    parse_failure()