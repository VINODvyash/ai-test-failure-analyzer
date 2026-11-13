import argparse
import os
import json


def main():
    parser = argparse.ArgumentParser(
        description="AI Test Failure Analyzer CLI - Run and inspect AI-driven test diagnostics."
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # 'reports' command to list recent diagnostic files
    # reports_parser = subparsers.add_parser("reports", help="List all generated JSON diagnostic reports.")

    subparsers.add_parser("reports", help="List all generated JSON diagnostic reports.")

    # 'analyze' command to view a specific report or run a quick text analysis
    analyze_parser = subparsers.add_parser("analyze", help="Display details of a specific JSON report.")
    analyze_parser.add_argument("--file", required=True, help="Path to the JSON report file.")

    html_parser = subparsers.add_parser("report", help="Generate an interactive HTML visual dashboard from reports.")
    html_parser.add_argument("--html", action="store_true", help="Compile JSON reports into an HTML dashboard.")

    args = parser.parse_args()

    if args.command == "reports":
        reports_dir = "reports"
        if not os.path.exists(reports_dir):
            print("[!] No 'reports/' directory found yet. Run some tests first!")
            return

        files = [f for f in os.listdir(reports_dir) if f.endswith(".json")]
        if not files:
            print("[!] No JSON reports found in the reports/ folder.")
            return

        print(f"\n[*] Found {len(files)} diagnostic report(s):")
        for f in sorted(files):
            print(f"  - {os.path.join(reports_dir, f)}")
        print()

    elif args.command == "analyze":
        if not os.path.exists(args.file):
            print(f"[!] Error: Report file '{args.file}' not found.")
            return

        with open(args.file, "r", encoding="utf-8") as f:
            data = json.load(f)

        print("\n========================================")
        print(f"📄 REPORT DETAILS: {args.file}")
        print("========================================")
        print(json.dumps(data, indent=2))
        print("========================================\n")

    elif args.command == "report":
        if args.html:
            generate_html_report()
        else:
            print("[!] Please specify --html flag.")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()