from flask import Flask, request
import requests
import os

app = Flask(__name__)

FEEDBACK_WEBHOOK = os.getenv("https://discord.com/api/webhooks/1484192884214468810/sim7ykN4Cj9F3xXsSZflIkB_nQbFMxgaXo30vQocL891dN6EWRub4B_xJHd0hYn4DOXb")
RESTOCK_WEBHOOK = os.getenv("https://discord.com/api/webhooks/1483873834024304772/T9bbCviBm_sJRZH3NMpYGBSQ3ErN5V7X_j1SYaAUCfQEHqLwB0gCpXA7yL8EqEB3UBFh")

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
