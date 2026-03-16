from fastapi import APIRouter, Request
from services.pr_service import fetch_pr_files, post_review_comment
from services.ai_reviewer import review_code

router = APIRouter()

@router.post("/webhook")
async def github_webhook(request: Request):

    payload = await request.json()
    action = payload.get("action")

    # Trigger only when PR is opened
    if action == "opened":

        pr_number = payload["pull_request"]["number"]
        print(f"\n New PR opened: #{pr_number}")

        # Get changed files
        pr_files = fetch_pr_files(pr_number)

        print(f" Total files changed: {len(pr_files)}")

        for file in pr_files:

            filename = file["filename"]
            patch = file["patch"]

            print(f"\n Processing file: {filename}")

            # Only review python files
            if filename.endswith(".py"):

                print(" Python file detected → Running AI Review")

                try:
                    review = review_code(filename, patch)

                    print("\n AI Review Generated:\n", review)

                    # Post comment on PR
                    post_review_comment(pr_number, review)

                    print(" Review comment posted to PR")

                except Exception as e:
                    print(" AI Review failed:", str(e))

            else:
                print(" Skipping non-python file")

    return {"status": "received"}