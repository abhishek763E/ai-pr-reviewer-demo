from github import Github
from config.settings import GITHUB_TOKEN, GITHUB_REPO
import requests
import re

g = Github(GITHUB_TOKEN)
repo = g.get_repo(GITHUB_REPO)

# -------------------------------
# 🔹 Fetch PR Files
# -------------------------------
def fetch_pr_files(pr_number):
    pr = repo.get_pull(pr_number)
    files = pr.get_files()

    pr_changes = []

    for file in files:
        pr_changes.append({
            "filename": file.filename,
            "status": file.status,
            "patch": file.patch
        })

    return pr_changes


# -------------------------------
# 🔹 TinyLlama AI Review
# -------------------------------
def run_ai_review_llm(pr_changes):

    full_code = ""

    for file in pr_changes:
        full_code += f"\n# File: {file['filename']}\n{file['patch']}\n"

    # ⚠️ Limit size (important for TinyLlama)
    full_code = full_code[:3000]

    prompt = f"""
You are a strict senior code reviewer.

Give output in EXACT format:

Score: X/10
Issues:
- ...
Suggestions:
- ...

Rules:
- Score between 1 to 10
- Be strict
- Keep it short

Example:
Score: 8/10
Issues:
- Missing error handling
Suggestions:
- Add try-except

Code:
{full_code}
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "tinyllama",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]


# -------------------------------
# 🔹 Extract Score
# -------------------------------
def extract_score(review_text):
    match = re.search(r"Score:\s*(\d+(\.\d+)?)/10", review_text)

    if match:
        return float(match.group(1))

    return 5  # fallback if model fails


# -------------------------------
# 🔹 Format Final Review
# -------------------------------
def format_review(review_text, score):

    if score >= 9:
        emoji = "🟢 Excellent"
    elif score >= 7:
        emoji = "🟡 Good"
    else:
        emoji = "🔴 Needs Improvement"

    return f"""
### 🤖 AI Code Review

⭐ **Score: {score}/10**  
{emoji}

---

{review_text}
"""


# -------------------------------
# 🔹 Post Comment to GitHub
# -------------------------------
def post_review_comment(pr_number, review):

    pr = repo.get_pull(pr_number)

    pr.create_issue_comment(review)