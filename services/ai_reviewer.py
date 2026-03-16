import ollama

def review_code(filename, patch):

    prompt = f"""
You are a senior Python code reviewer.

Review this pull request change.

File: {filename}

Code diff:
{patch}

Give:
- Bugs
- Improvements
- Security issues
- Best practices
"""

    response = ollama.chat(
        model="tinyllama",
        messages=[{
            "role": "user",
            "content": prompt
        }]
    )

    return response["message"]["content"]