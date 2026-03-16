import requests

def review_code(filename, patch):

    prompt = f"""
You are a senior software engineer reviewing a pull request.

Review the following code changes and provide:

1. Bugs or logical issues
2. Code improvements
3. Security issues
4. Performance improvements
5. Best practice suggestions

File: {filename}

Code changes:
{patch}

Respond with clear bullet points.
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

    return result.get("response", "No review generated.")