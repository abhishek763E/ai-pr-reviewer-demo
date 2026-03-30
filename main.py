from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from webhook import router

app = FastAPI(title="AI PR Reviewer")
print("testing AI reviewer PR")

app.include_router(router)

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <head><title>AI PR Reviewer</title></head>
        <body>
            <h1>AI PR Reviewer Running s ✅</h1>
            # test change for AI reviewer
            <p>Waiting for Pull Request events from GitHub...</p>
             
        </body>
    </html>
    """
def add(a,b):
    return a+b

    print("i am not a robot")

def multi(a,b):
    return a*b
    print("this is common  multiplication")


def multiplication(a,b,c):
    return a*b*c
    print("this is common  multiplication")


