import os
import json
from google import genai


def analyze_test_failure(test_name: str, error_trace: str, screenshot_path: str = None) -> dict:
    """Sends failing test details and screenshot to Gemini for structured JSON root-cause analysis."""
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    # Build the prompt instructing Gemini to return strict JSON
    prompt = f"""
    You are an expert QA automation engineer and debugging assistant. 
    A Playwright/pytest test has failed. Analyze the failure details below and output a JSON object with the following keys:
    - "root_cause": A clear, concise explanation of why the test failed.
    - "probable_fix": Step-by-step instructions on how to fix the code or test.
    - "severity": "Low", "Medium", or "High".

    TEST NAME: {test_name}

    ERROR TRACE:
    {error_trace}

    Return ONLY valid JSON. No extra markdown text outside the JSON block.
    """

    contents = [prompt]

    if screenshot_path and os.path.exists(screenshot_path):
        uploaded_file = client.files.upload(file=screenshot_path)
        contents.append(uploaded_file)
        print(f"[*] Uploaded failure screenshot: {screenshot_path}")

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=contents,
    )

    try:
        raw_text = response.text.strip()
        if raw_text.startswith("```json"):
            raw_text = raw_text[7:-3].strip()
        elif raw_text.startswith("```"):
            raw_text = raw_text[3:-3].strip()

        return json.loads(raw_text)
    except json.JSONDecodeError:
        return {
            "root_cause": "Failed to parse JSON from AI response.",
            "raw_response": response.text
        }


if __name__ == "__main__":
    sample_error = "AssertionError: Expected element 'button#submit' to be visible, but it was not found after 5000ms."
    result = analyze_test_failure("test_user_login", sample_error)
    print(json.dumps(result, indent=2))