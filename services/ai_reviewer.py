import requests

def review_code(filename, patch):

    prompt = f"""
You are a senior Python code reviewer.

Review the following code changes and give feedback.

File: {filename}

Changes:
{patch}

Provide:
- Bugs
- Code improvements
- Security issues
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "tinyllama",
            "prompt": prompt,
            "stream": False
        }
    )

    result = response.json()

    return result["response"]