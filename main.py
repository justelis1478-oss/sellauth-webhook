from flask import Flask, request
import requests
import os
import time

app = Flask(__name__)

FEEDBACK_WEBHOOK = os.getenv("FEEDBACK_WEBHOOK_URL")
RESTOCK_WEBHOOK = os.getenv("RESTOCK_WEBHOOK_URL")


def send_to_discord(webhook_url, content, label):
    if not webhook_url:
        print(f"{label}: webhook URL missing", flush=True)
        return

    try:
        response = requests.post(
            webhook_url,
            json={"content": content},
            timeout=15
        )

        print(f"{label}: discord status = {response.status_code}", flush=True)
        print(f"{label}: discord response = {response.text}", flush=True)

        if response.status_code == 429:
            retry_after = 5
            try:
                data = response.json()
                retry_after = float(data.get("retry_after", 5))
            except Exception:
                pass

            print(f"{label}: rate limited, retrying after {retry_after} seconds", flush=True)
            time.sleep(retry_after)

            retry_response = requests.post(
                webhook_url,
                json={"content": content},
                timeout=15
            )
            print(f"{label}: retry status = {retry_response.status_code}", flush=True)
            print(f"{label}: retry response = {retry_response.text}", flush=True)

    except Exception as e:
        print(f"{label}: error sending to Discord: {e}", flush=True)


@app.route("/")
def home():
    print("HOME HIT", flush=True)
    return "OK", 200


@app.route("/feedback", methods=["POST"])
def feedback():
    data = request.json
    print("FEEDBACK HIT:", data, flush=True)

    content = f"📝 New feedback:\n```{data}```"
    send_to_discord(FEEDBACK_WEBHOOK, content, "FEEDBACK")

    return "OK", 200


@app.route("/restock", methods=["POST"])
def restock():
    data = request.json
    print("RESTOCK HIT:", data, flush=True)

    content = f"📦 Restock:\n```{data}```"
    send_to_discord(RESTOCK_WEBHOOK, content, "RESTOCK")

    return "OK", 200
