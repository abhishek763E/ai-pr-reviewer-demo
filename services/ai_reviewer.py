import ollama

def review_code(filename, patch):
    prompt = f"""
You are a senior Python code reviewer.

Review the following pull request change.

File: {filename}

Code diff:
{patch}

Provide:
1. Bugs
2. Code improvements
3. Security issues
4. Best practice suggestions
"""

    response = ollama.chat(
        model="tinyllama",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]