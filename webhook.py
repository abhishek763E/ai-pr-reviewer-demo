from fastapi import APIRouter, Request
from services.pr_service import fetch_pr_files

router = APIRouter()

@router.post("/webhook")
async def github_webhook(request: Request):
    payload = await request.json()
    action = payload.get("action")

    # Only react to opened PRs for now
    if action == "opened":
        pr_number = payload["pull_request"]["number"]
        print(f"New PR opened: #{pr_number}")

        pr_files = fetch_pr_files(pr_number)

        for file in pr_files:
            print(f"File: {file['filename']}, Status: {file['status']}")
            print(file['patch'])
            print("--------")

    return {"status": "received"}