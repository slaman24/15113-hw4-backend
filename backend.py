from flask import Flask, request, jsonify
import os
import requests
import json

# Load local secrets from secrets.txt (for local dev)
def load_local_secrets():
    if os.path.exists("secrets.txt"):
        with open("secrets.txt") as f:
            for line in f:
                if "=" in line:
                    key, value = line.strip().split("=", 1)
                    os.environ[key] = value

load_local_secrets()

# Get API key from environment variable
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("Missing OPENAI_API_KEY. Add it to secrets.txt or Render environment variables.")

app = Flask(__name__)

# Your AI assistant context
ABOUT_ME_CONTEXT = """
You are an AI assistant representing Sara Laman.
Sara's skills include front-end development (HTML, CSS, JavaScript, React), Python, and backend coursework.
Projects include MediaPipe hand gesture recognition and portfolio websites.
She enjoys baking, data science, and interactive web design.
Be warm, helpful, and concise.
"""

# OpenAI API endpoint
OPENAI_URL = "https://api.openai.com/v1/chat/completions"

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question", "")

    if not question:
        return jsonify({"error": "No question provided"}), 400

    # Build the request payload
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": ABOUT_ME_CONTEXT},
            {"role": "user", "content": question}
        ],
        "temperature": 0.7
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }

    # Make the request to OpenAI API
    response = requests.post(OPENAI_URL, headers=headers, data=json.dumps(payload))

    if response.status_code != 200:
        return jsonify({"error": f"OpenAI API error: {response.text}"}), 500

    res_json = response.json()
    answer = res_json["choices"][0]["message"]["content"]

    return jsonify({"answer": answer})

@app.route("/")
def home():
    return "Sara's AI backend is running!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
