# import pytest
# import json
# from pathlib import Path


# @pytest.fixture(scope="session")
# def browser_context_args(browser_context_args):
#     return {
#         **browser_context_args,
#         "viewport": {
#             "width": 1280,
#             "height": 720
#         }
#     }

# @pytest.hookimpl(hookwrapper=True)
# def pytest_runtest_makereport(item, call):
#     outcome = yield
#     report = outcome.get_result()

#     if report.when =="call" and report.failed:
#         reports_dir = Path("reports")
#         reports_dir.mkdir(exist_ok=True)

#         failure_data = {
#             "test_name": item.nodeid,
#             "outcome": report.outcome,
#             "longrepr": str(report.longrepr),
#         }

#         failure_files = reports_dir / "latest_failure.json"

#         with open(failure_files, "w", encoding="utf-8") as file:
#             json.dump(
#                 failure_data,
#                 file,
#                 indent=4
#             )


# import json
# import pytest
# from pathlib import Path


# @pytest.fixture(scope="session")
# def browser_context_args(browser_context_args):
#     return {
#         **browser_context_args,
#         "viewport": {
#             "width": 1280,
#             "height": 720
#         }
#     }


# @pytest.hookimpl(hookwrapper=True)
# def pytest_runtest_makereport(item, call):
#     outcome = yield
#     report = outcome.get_result()

#     if report.when == "call" and report.failed:
#         reports_dir = Path("reports")
#         reports_dir.mkdir(exist_ok=True)
#         screenshots_dir = Path("screenshots")
#         screenshots_dir.mkdir(exist_ok=True)

#         # 1. Capture Playwright screenshot if page fixture was used
#         screenshot_file = None
#         page = item.funcargs.get("page")
#         if page:
#             safe_name = item.name.replace("[", "_").replace("]", "_")
#             screenshot_path = screenshots_dir / f"{safe_name}.png"
#             try:
#                 page.screenshot(path=str(screenshot_path))
#                 screenshot_file = str(screenshot_path)
#             except Exception:
#                 screenshot_file = None

#         # 2. Extract structured failure details
#         error_type = call.excinfo.typename if call.excinfo else "UnknownError"
#         error_message = str(call.excinfo.value) if call.excinfo else ""

#         failure_data = {
#             "test_name": item.nodeid,
#             "test_file": str(item.fspath),
#             "outcome": report.outcome,
#             "error_type": error_type,
#             "error_message": error_message,
#             "page_url": page.url if page else None,
#             "screenshot_path": screenshot_file,
#             "longrepr": str(report.longrepr)
#         }

#         failure_file = reports_dir / "latest_failure.json"
#         with open(failure_file, "w", encoding="utf-8") as file:
#             json.dump(failure_data, file, indent=4)

import os
from dotenv import load_dotenv
from pathlib import Path
from google import genai
from google.genai import types
import json

import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from AI_analyzer.failure_parser import FailureParser

def analyze_test_failure():
    parser = FailureParser()
    payload = parser.build_llm_payload()

    prompt = f"""
    You are an expert QA Automation Engineer specialized in Python, Pytest, and Playwright.
Analyze this test failure and return a structured JSON response.

TEST NAME: {payload.get('test_name')}
PAGE URL AT CRASH: {payload.get('failed_url')}
ERROR TYPE: {payload.get('error_type')}
ERROR MESSAGE: {payload.get('error_message')}

CLEANED TRACEBACK:
{payload.get('cleaned_traceback')}

Respond strictly with valid JSON conforming to this schema:
{{
  "root_cause_category": "string (one of: 'Assertion Mismatch', 'Locator/Selector Changed', 'Timeout / Timing Issue', 'Anti-Bot / CAPTCHA', 'Network / API Error', 'Application Bug')",
  "is_flaky_candidate": boolean,
  "confidence_score": "number between 0.0 and 1.0",
  "plain_english_summary": "string explaining what failed and why",
  "suggested_patch": "string containing the exact code change or Playwright auto-wait method to fix it"
}}
"""

print("\n Analyzing failure with AI...\n")

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt,
    config=types.GenerateContentConfig(
        response_mime_type="application/json"
    ),
)

result_json = json.loads(response.text)

reports_dir = Path("reports")
reports_dir.mkdir(exist_ok=True)
report_file = reports_dir / "ai_analysis.json"

with open(report_file, "w", encoding="utf-8") as f:
    json.dump(result_json, f, indent=4)

    print("\n================= AI DIAGNOSTIC REPORT =================")
    print(f"📌 Root Cause   : {result_json.get('root_cause_category')}")
    print(f"⚠️ Flaky Risk   : {'Yes' if result_json.get('is_flaky_candidate') else 'No'}")
    print(f"🎯 Confidence   : {result_json.get('confidence_score') * 100:.0f}%")
    print(f"\n📝 Summary:\n{result_json.get('plain_english_summary')}")
    print(f"\n💡 Suggested Code Fix:\n{result_json.get('suggested_patch')}")
    print("========================================================\n")
    print(f"Full JSON report saved to: {report_file}")


    if __name__ == "__main__":
        abalyze_test_failure()