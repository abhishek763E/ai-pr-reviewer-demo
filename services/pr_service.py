from github import Github
from config.settings import GITHUB_TOKEN, GITHUB_REPO

g = Github(GITHUB_TOKEN)
repo = g.get_repo(GITHUB_REPO)

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


def post_review_comment(pr_number, review):

    pr = repo.get_pull(pr_number)

    pr.create_issue_comment(
        f"### 🤖 AI Code Review\n\n{review}"
    )

def sub(a,b):
    return a-b




