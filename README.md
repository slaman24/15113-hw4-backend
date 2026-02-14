# 15113-hw4-backend

This is the backend code for my personal website's Q&A chat bubble, powered by OpenAI's GPT-4o-mini.

Render deployment link: https://one5113-hw4-project.onrender.com

This backend acts as a proxy between my personal portfolio website and the OpenAI API. It provides an AI assistant and handles conversation processing. POST /ask is the main Q&A endpoint. It takes in parameters in the form {"question": "string"} (JSON body) and either returns {"answer": "string"} or {"error": "message"}. The frontend communicates with the backend by sending a POST request to the /ask endpoint at my Render deployment link (or at http://localhost:5001/ask if run locally). I used a virtual environment to install the flask, reuqests, flask-cors, and gunicorn modules (all listed in my requirements.txt file). Since the OpenAI API requires a private API key, I created an environment variable called OPENAI_API_KEY in Render to store it. I also stored my API key in secrets.txt (which I listed in .gitignore so I would not commit my API key to GitHub) to be used locally. As a result, my API keyis never exposed to the frontend code for users to see.
