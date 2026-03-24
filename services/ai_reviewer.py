import ollama
def review_code(filename, patch):
    prompt = f"""
You are a STRICT senior Python code reviewer.

Your task is to review the given code diff.

DO NOT say:
- "I cannot review"
- "Here is an example"
- "I am unable"

You MUST review the code.

File: {filename}

Code diff:
{patch}

Format EXACTLY like this:

Line: <code line>
Issue: <problem>
Suggestion: <fix>

- Only include lines with issues
- Keep answers short and precise
"""

    response = ollama.chat(
        model="tinyllama",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]