import pytest
import os
from analyzer import analyze_test_failure


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Execute all other hooks to obtain the report object
    outcome = yield
    report = outcome.get_result()

    # We only care when a test actually FAILS during the 'call' phase
    if report.when == "call" and report.failed:
        test_name = item.name
        error_trace = str(report.longrepr)

        # Check if a Playwright page fixture is available to snap a screenshot
        screenshot_path = None
        if "page" in item.funcargs:
            page = item.funcargs["page"]
            os.makedirs("failures", exist_ok=True)
            screenshot_path = os.path.join("failures", f"{test_name}.png")
            page.screenshot(path=screenshot_path)
            print(f"\n[!] Test failed! Captured screenshot at: {screenshot_path}")

        print(f"\n[*] Sending failure details of '{test_name}' to Gemini AI...")
        analysis = analyze_test_failure(test_name, error_trace, screenshot_path)

        # Print structured JSON report right into your terminal
        print("\n--- AI ROOT CAUSE DIAGNOSIS ---")
        import json
        print(json.dumps(analysis, indent=2))
        print("-------------------------------\n")