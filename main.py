from flask import Flask, request
import requests
import os

app = Flask(__name__)

FEEDBACK_WEBHOOK = os.getenv("FEEDBACK_WEBHOOK_URL")
RESTOCK_WEBHOOK = os.getenv("RESTOCK_WEBHOOK_URL")

@app.route("/")
def home():
    return "OK", 200

# 🔹 FEEDBACK
@app.route("/feedback", methods=["POST"])
def feedback():
    data = request.json

    message = {
        "content": f"📝 New feedback:\n{data}"
    }

    requests.post(FEEDBACK_WEBHOOK, json=message)
    return "OK", 200

# 🔹 RESTOCK
@app.route("/restock", methods=["POST"])
def restock():
    data = request.json

    message = {
        "content": f"📦 Restock:\n{data}"
    }

    requests.post(RESTOCK_WEBHOOK, json=message)
    return "OK", 200
