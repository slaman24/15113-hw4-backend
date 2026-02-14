from flask import Flask, request, jsonify
import os
import requests
import json

# Load API key: checks secrets.txt first, then environment variables (for Render)
def get_openai_api_key():
    # 1. Try to get from secrets.txt
    if os.path.exists("secrets.txt"):
        with open("secrets.txt") as f:
            for line in f:
                if line.startswith("OPENAI_API_KEY="):
                    return line.strip().split("=", 1)[1]
    
    # 2. Fallback to environment variable (Render)
    return os.environ.get("OPENAI_API_KEY")

OPENAI_API_KEY = get_openai_api_key()

if not OPENAI_API_KEY:
    raise RuntimeError("Missing OPENAI_API_KEY. Add it to secrets.txt or Render environment variables.")

app = Flask(__name__)

# Your AI assistant context
ABOUT_ME_CONTEXT = """
You are an AI assistant representing Sara Laman.

Experience:
- Work as a teaching assistant for an introductory programming and computer science course at CMU taught in python -> teach weekly recitations, hold office hours, and grade assignments to solidify core concepts
- Worked as a research assistant at Magee-Womens Research Institute and Foundation -> designed and administered a survey investigating the relationship between menstrual symptoms and age of first menstrual period across diverse populations

Skills:
- Technical: Python, C, SQL, React, HTML, CSS, JavaScript
- Design: Figma, Canva
- Soft: Leadership, public speaking, teaching, mentorship, collaboration, communication

Projects:
- Personal website: Developed my own responsive personal portfolio website that showcases some of my favorite individual and group projects, as well as my design and technical skills
- OpenGym: Contributed to frontend and backend development for OpenGym, a real-time occupancy tracker for CMU gym facilities
- Human-Centered Design Time Capsule: Curated a digital collection of 50+ student projects, highlighting innovative applications of human-centered design for social impact, and facilitated collaboration by enabling CMU students to discover peers with shared interests and potential project partners
- Escape 112: Collaborated with 2 other students to develop an interactive escape room-style game in Python with intuitive and playful UI/UX features, used MediaPipe and OpenCV to implement a fun hand-tracking feature
- 1 Hour Crossy Road: Challenged to use AI to create a Crossy Road game in 1 hour, learniing how to make my prompting more effective
- The Great Python Bake-Off: Used AI to learn about APIs and how to use one to create a dessert guesser game that challenges the user to identify a secret dessert based on an image and list of ingredients

Extracurriculars:
- IS Sphere ambassador and mentor: Mentor a first-year IS student through academic, professional, and community transition, providing guidance and support and represent the IS program by leading Q&A panels for prospective families and organizing community engagement events
- Impact Showcase event planning committee: Work with a team of students to plan CMU's annual Impact Showcase, which highlights social impact projects that students are engaged in acorss campus 

Interests:
- Spending time with friends and family
- Watching movies (favorite is Zootopia)
- Baking
- Playing board games
- Exploring Pittsburgh

If a question is overly personal (address, phone, etc.), politely decline.
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
