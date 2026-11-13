import os
import json
from datetime import datetime

def generate_html_report(reports_dir: str = "reports", output_file: str = "ai_test_report.html"):
    if not os.path.exists(reports_dir):
        print(f"[!] Reports directory '{reports_dir}' not found.")
        return

    json_files = [f for f in os.listdir(reports_dir) if f.endswith(".json")]
    if not json_files:
        print("[!] No JSON reports found to compile.")
        return

    reports_data = []
    for file_name in sorted(json_files):
        file_path = os.path.join(reports_dir, file_name)
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                reports_data.append(data)
        except Exception as e:
            print(f"[!] Error reading {file_name}: {e}")

    # Build sleek HTML structure with embedded CSS styling
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Test Failure Diagnostic Dashboard</title>
    <style>
        :root {{
            --bg-color: #0f172a;
            --card-bg: #1e293b;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --accent-red: #ef4444;
            --accent-yellow: #f59e0b;
            --accent-green: #22c55e;
            --border-color: #334155;
        }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-main);
            margin: 0;
            padding: 20px;
        }}
        .container {{
            max-width: 1000px;
            margin: 0 auto;
        }}
        header {{
            text-align: center;
            margin-bottom: 40px;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 20px;
        }}
        h1 {{
            margin: 0;
            font-size: 2rem;
            color: #38bdf8;
        }}
        .subtitle {{
            color: var(--text-muted);
            margin-top: 5px;
        }}
        .card {{
            background-color: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }}
        .card-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 10px;
            margin-bottom: 15px;
        }}
        .timestamp {{
            color: var(--text-muted);
            font-size: 0.9rem;
        }}
        .badge {{
            padding: 4px 10px;
            border-radius: 4px;
            font-size: 0.8rem;
            font-weight: bold;
            text-transform: uppercase;
        }}
        .badge-high {{ background-color: var(--accent-red); color: white; }}
        .badge-medium {{ background-color: var(--accent-yellow); color: black; }}
        .badge-low {{ background-color: var(--accent-green); color: white; }}
        .section-title {{
            font-weight: bold;
            color: #38bdf8;
            margin-top: 10px;
            margin-bottom: 5px;
        }}
        pre {{
            background-color: #090d16;
            padding: 10px;
            border-radius: 6px;
            overflow-x: auto;
            color: #e2e8f0;
            font-size: 0.85rem;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🤖 AI Test Failure Dashboard</h1>
            <div class="subtitle">Generated automatically by AI Test Failure Analyzer</div>
            <div class="timestamp">Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
        </header>
"""

    for report in reports_data:
        severity = report.get("severity", "HIGH").lower()
        badge_class = f"badge-{severity}" if severity in ["high", "medium", "low"] else "badge-high"
        
        html_content += f"""
        <div class="card">
            <div class="card-header">
                <div><strong>Test Error Diagnosis</strong></div>
                <div><span class="badge {badge_class}">Severity: {report.get('severity', 'UNKNOWN')}</span></div>
            </div>
            <div class="section-title">🔍 Root Cause:</div>
            <p>{report.get('root_cause', 'No root cause provided.')}</p>
            
            <div class="section-title">🛠️ Suggested Fix:</div>
            <p>{report.get('suggested_fix', 'No fix provided.')}</p>
            
            <div class="section-title">📋 Raw Traceback Snippet:</div>
            <pre>{report.get('traceback_summary', 'N/A')}</pre>
        </div>
        """

    html_content += """
    </div>
</body>
</html>
"""

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"[+] Gorgeous HTML report generated successfully: {output_file}")