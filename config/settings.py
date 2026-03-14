from dotenv import load_dotenv
import os
import base64

load_dotenv()

_token_b64 = os.getenv("GITHUB_TOKEN_B64")
GITHUB_TOKEN = base64.b64decode(_token_b64).decode("utf-8") if _token_b64 else None
GITHUB_REPO = os.getenv("GITHUB_REPO")