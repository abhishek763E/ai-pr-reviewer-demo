from fastapi import APIRouter, Request
from services.pr_service import (
    fetch_pr_files,
    run_ai_review_llm,
    extract_score,
    format_review,
    post_review_comment
)

router = APIRouter()

@router.post("/webhook")
async def github_webhook(request: Request):
    payload = await request.json()
    action = payload.get("action")

    # ✅ Handle multiple PR events (important)
    if action in ["opened", "synchronize", "reopened"]:

        pr = payload["pull_request"]
        pr_number = pr["number"]

        base_branch = pr["base"]["ref"]
        head_branch = pr["head"]["ref"]

        print(f"PR #{pr_number}")
        print(f"Base: {base_branch}, Head: {head_branch}")

        # ✅ Only allow test-ai-review → main
        if base_branch == "main" and head_branch == "test-ai-review":

            print("Valid PR direction detected ✅")

            pr_files = fetch_pr_files(pr_number)

            # Filter only Python files with changes
            filtered_files = [
                file for file in pr_files
                if file["filename"].endswith(".py") and file["patch"]
            ]

            if not filtered_files:
                print("No Python files to review ❌")
                return {"status": "no python files"}

            print(f"Reviewing {len(filtered_files)} files...")

            # 🔥 Run TinyLlama AI Review
            review_text = run_ai_review_llm(filtered_files)

            print("AI Review Generated ✅")

            # 🔢 Extract Score
            score = extract_score(review_text)

            # 🧾 Format Final Output
            final_review = format_review(review_text, score)

            # 💬 Post Single Comment
            post_review_comment(pr_number, final_review)

            print("Comment posted to PR 🚀")
            print("---------------------------")

    return {"status": "received"}