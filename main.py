from fastapi import FastAPI
from webhook import router

app = FastAPI(title="AI PR Reviewer")

app.include_router(router)

@app.get("/")
def home():
    return {"message": "AI PR Reviewer Running perfectly"}