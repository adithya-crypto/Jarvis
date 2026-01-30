import requests
import yaml
import os


def load_api_key():
    with open("config/settings.yaml", "r") as f:
        config = yaml.safe_load(f)
    return config["gemini_api_key"]


def generate_code(prompt):
    """Generate a code snippet using Gemini API."""
    api_key = load_api_key()
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"

    system_prompt = (
        "You are a code generation assistant. Write clean, concise code based on the user's request. "
        "Only output the code with brief comments. No markdown formatting. "
        "Keep it short and practical."
    )

    data = {
        "contents": [{
            "parts": [{"text": f"{system_prompt}\n\nUser request: {prompt}"}]
        }]
    }

    try:
        response = requests.post(url, json=data, headers={"Content-Type": "application/json"})
        response.raise_for_status()
        result = response.json()
        code = result['candidates'][0]['content']['parts'][0]['text'].strip()

        # Save to snippets directory
        os.makedirs("data/snippets", exist_ok=True)
        snippet_path = "data/snippets/latest_snippet.txt"
        with open(snippet_path, "w") as f:
            f.write(code)

        print(f"Code saved to {snippet_path}")
        return f"Code generated and saved to {snippet_path}. Here's a summary: {code[:100]}..."

    except Exception as e:
        print(f"Code generation error: {e}")
        return "I encountered an error generating code."
