from fastapi import APIRouter, Request
from services.pr_service import fetch_pr_files, post_review_comment
from services.ai_reviewer import review_code

router = APIRouter()

@router.post("/webhook")
async def github_webhook(request: Request):

    payload = await request.json()

    action = payload.get("action")

    if action == "opened":

        pr_number = payload["pull_request"]["number"]

        print(f"New PR opened: {pr_number}")

        pr_files = fetch_pr_files(pr_number)

        for file in pr_files:

            filename = file["filename"]
            patch = file["patch"]

            print("Processing file:", filename)

            if filename.endswith(".py") and patch:

                review = review_code(filename, patch)

                post_review_comment(pr_number, review)

                print("AI review posted to PR")

    return {"status": "received"}