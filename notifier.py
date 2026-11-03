import os
import requests
import json

def send_failure_alert(report_data: dict, webhook_url: str = None):
    """
    Sends the AI test failure diagnosis to a Slack or Discord webhook.
    """
    url = webhook_url or os.getenv("AI_ANALYZER_WEBHOOK_URL")
    if not url:
        print("[*] No webhook URL configured. Skipping chat notification.")
        return

    # Format the message payload
    error_summary = report_data.get("root_cause", "Unknown error")
    fix_steps = report_data.get("suggested_fix", "No fix provided")
    severity = report_data.get("severity", "HIGH")

    message = {
        "text": f"🚨 *AI Test Failure Alert* (Severity: `{severity}`)\n"
                f"*Root Cause:* {error_summary}\n"
                f"*Suggested Fix:* {fix_steps}"
    }

    try:
        response = requests.post(url, json=message)
        if response.status_code == 200 or response.status_code == 204:
            print("[+] Failure notification successfully sent to chat channel!")
        else:
            print(f"[!] Failed to send notification. Status code: {response.status_code}")
    except Exception as e:
        print(f"[!] Error sending webhook notification: {e}")