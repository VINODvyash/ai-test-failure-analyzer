import pytest
import json
from pathlib import Path


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {
            "width": 1280,
            "height": 720
        }
    }

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when =="call" and report.failed:
        reports_dir = Path("reports")
        reports_dir.mkdir(exist_ok=True)

        failure_data = {
            "test_name": item.nodeid,
            "outcome": report.outcome,
            "longrepr": str(report.longrepr),
        }

        failure_files = reports_dir / "latest_failure.json"

        with open(failure_files, "w", encoding="utf-8") as file:
            json.dump(
                failure_data,
                file,
                indent=4
            )