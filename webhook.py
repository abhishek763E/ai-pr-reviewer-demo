from fastapi import APIRouter, Request
from services.pr_service import fetch_pr_files, post_review_comment
from services.ai_reviewer import review_code

router = APIRouter()

@router.post("/webhook")
async def github_webhook(request: Request):
    payload = await request.json()
    action = payload.get("action")

    # Only react when a PR is opened
    if action == "opened":
        pr_number = payload["pull_request"]["number"]
        print(f"New PR opened: #{pr_number}")

        pr_files = fetch_pr_files(pr_number)

        for file in pr_files:
            filename = file["filename"]
            patch = file["patch"]

            # Only review Python files
            if filename.endswith(".py") and patch:

                print(f"Reviewing file: {filename}")

                # Send code diff to AI
                review = review_code(filename, patch)

                print("AI Review Generated")
                print(review)

                # Post AI review comment on the PR
                post_review_comment(pr_number, f"""
### 🤖 AI Code Review

**File:** `{filename}`

{review}

---
_AI review generated using local model via Ollama_
""")

                print("Comment posted to PR")
                print("---------------------------")

    return {"status": "received"}

def sub(a,b):
    return a-b
