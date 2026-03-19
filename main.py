from flask import Flask, request
import requests
import os

app = Flask(__name__)

FEEDBACK_WEBHOOK = os.getenv("FEEDBACK_WEBHOOK_URL")
RESTOCK_WEBHOOK = os.getenv("RESTOCK_WEBHOOK_URL")

@app.route("/")
def home():
    print("HOME HIT", flush=True)
    return "OK", 200

@app.route("/feedback", methods=["POST"])
def feedback():
    data = request.json
    print("FEEDBACK HIT:", data, flush=True)
    print("FEEDBACK WEBHOOK SET:", bool(FEEDBACK_WEBHOOK), flush=True)

    message = {
        "content": f"📝 New feedback:\n{data}"
    }

    r = requests.post(FEEDBACK_WEBHOOK, json=message)
    print("FEEDBACK DISCORD STATUS:", r.status_code, flush=True)
    print("FEEDBACK DISCORD RESPONSE:", r.text, flush=True)

    return "OK", 200

@app.route("/restock", methods=["POST"])
def restock():
    data = request.json
    print("RESTOCK HIT:", data, flush=True)
    print("RESTOCK WEBHOOK SET:", bool(RESTOCK_WEBHOOK), flush=True)

    message = {
        "content": f"📦 Restock:\n{data}"
    }

    r = requests.post(RESTOCK_WEBHOOK, json=message)
    print("RESTOCK DISCORD STATUS:", r.status_code, flush=True)
    print("RESTOCK DISCORD RESPONSE:", r.text, flush=True)

    return "OK", 200
