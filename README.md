# Hi there, I'm Vinod Vyash 👋

### 🐍 Python Backend Developer & QA Automation Engineer

Passionate about building scalable backend architectures, automated testing pipelines, and AI-powered developer tooling. I specialize in Django REST Framework APIs, automated test frameworks, and integrating generative AI to eliminate tedious developer workflows.

## 🛠️ Tech Stack & Skills
* **Languages:** Python 3.13, SQL
* **Backend & APIs:** Django, Django REST Framework (DRF), Serverless APIs
* **Automation & Testing:** Pytest, Playwright, Automated QA Security Tools
* **AI & SDKs:** Google GenAI SDK (`google-genai`), Gemini Multimodal Integration
* **DevOps & CI/CD:** Docker, GitHub Actions, Git, SQLite, PowerShell, Linux

---

## 🚀 Flagship Project: AI Test Failure Analyzer
An open-source developer tool that automates UI test diagnosis using Python, Playwright, and Google Gemini AI. It intercepts test failures, captures browser screenshots, and performs multimodal analysis to generate instant JSON root-cause reports.

* **Repository:** [VINODvyash/ai-test-failure-analyzer](https://github.com/VINODvyash/ai-test-failure-analyzer)

### Quickstart Guide (Run it locally):
```bash
# 1. Clone the repository
git clone [https://github.com/VINODvyash/ai-test-failure-analyzer.git](https://github.com/VINODvyash/ai-test-failure-analyzer.git)
cd ai-test-failure-analyzer

# 2. Install dependencies
pip install pytest playwright google-genai
playwright install chromium

# 3. Set your Gemini API key (PowerShell)
$env:GEMINI_API_KEY="your_actual_api_key_here"

# 4. Run the test suite with AI failure diagnosis
pytest -v
