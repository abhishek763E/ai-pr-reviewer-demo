def review_code(filename, patch):
    prompt = f"""
You are a senior Python code reviewer.

Review the following code diff line by line.

File: {filename}

Code diff:
{patch}

Instructions:
- Show the actual code line in your response
- Then give issue and suggestion
- Format strictly like this:

Line: <code line>
Issue: <problem>
Suggestion: <fix>

- Only include lines that need improvement
- Keep response clean and readable
- Do NOT skip code lines in output
"""

    response = ollama.chat(
        model="tinyllama",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]