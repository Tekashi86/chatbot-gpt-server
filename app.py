
from flask import Flask, request, jsonify
import openai
import os
import json

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Load reply flow
with open("reply_flow.json", "r", encoding="utf-8") as f:
    REPLY_FLOW = json.load(f)

def detect_category(message):
    msg = message.lower()
    for category, content in REPLY_FLOW.items():
        if any(trigger in msg for trigger in content["trigger"]):
            return category
    return "follow_up"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    user_message = data.get("message", "")
    tone = data.get("tone", "soft")  # default to soft tone

    category = detect_category(user_message)
    prompt = REPLY_FLOW[category][tone]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{ "role": "user", "content": prompt }]
    )
    reply = response.choices[0].message["content"]
    return jsonify({ "reply": reply })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
