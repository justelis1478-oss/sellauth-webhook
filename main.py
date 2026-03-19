from flask import Flask, request
import requests
import os

app = Flask(__name__)

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
FEEDBACK_CHANNEL_ID = os.getenv("FEEDBACK_CHANNEL_ID")
RESTOCK_CHANNEL_ID = os.getenv("RESTOCK_CHANNEL_ID")


def send_bot_message(channel_id, content, label):
    if not DISCORD_BOT_TOKEN:
        print(f"{label}: missing DISCORD_BOT_TOKEN", flush=True)
        return

    if not channel_id:
        print(f"{label}: missing channel_id", flush=True)
        return

    url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
    headers = {
        "Authorization": f"Bot {DISCORD_BOT_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "content": content
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        print(f"{label}: discord status = {response.status_code}", flush=True)
        print(f"{label}: discord response = {response.text}", flush=True)
    except Exception as e:
        print(f"{label}: error sending message: {e}", flush=True)


@app.route("/")
def home():
    return "OK", 200


@app.route("/feedback", methods=["POST"])
def feedback():
    data = request.json
    print("FEEDBACK HIT:", data, flush=True)

    content = f"📝 New feedback:\n```{data}```"
    send_bot_message(FEEDBACK_CHANNEL_ID, content, "FEEDBACK")

    return "OK", 200


@app.route("/restock", methods=["POST"])
def restock():
    data = request.json
    print("RESTOCK HIT:", data, flush=True)

    content = f"📦 Restock:\n```{data}```"
    send_bot_message(RESTOCK_CHANNEL_ID, content, "RESTOCK")

    return "OK", 200
