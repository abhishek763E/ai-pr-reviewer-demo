from fastapi import APIRouter, Request
from services.pr_service import fetch_pr_files

# create router first
router = APIRouter()

@router.post("/webhook")
async def github_webhook(request: Request):

    try:
        payload = await request.json()
    except Exception:
        return {"message": "Invalid JSON"}

    action = payload.get("action")

    if action == "opened":
        pr_number = payload["pull_request"]["number"]
        print(f"New PR opened: #{pr_number}")

        files = fetch_pr_files(pr_number)
        print(f"Total files changed: {len(files)}")

    return {"message": "Webhook received"}

def addd(a,b,c):
    a+b+c