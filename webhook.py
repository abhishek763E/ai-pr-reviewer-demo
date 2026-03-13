from fastapi import APIRouter, Request
from services.pr_service import fetch_pr_files

router = APIRouter()

@router.post("/webhook")
async def github_webhook(request: Request):

    payload = await request.json()

    action = payload.get("action")

    # Trigger when PR is opened
    if action == "opened":

        pr_number = payload["pull_request"]["number"]

        print("\n🔥 NEW PULL REQUEST RECEIVED")
        print(f"PR Number: {pr_number}")
        print("Fetching changed files...\n")

        pr_files = fetch_pr_files(pr_number)

        for file in pr_files:

            print("================================")
            print(f"File: {file['filename']}")
            print(f"Status: {file['status']}")
            print("Code Changes:\n")

            print(file["patch"])
            print("================================\n")

    return {"status": "received"}