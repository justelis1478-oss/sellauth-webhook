from flask import Flask, request, jsonify
import os
import requests
import traceback

app = Flask(__name__)

DISCORD_WEBHOOK_URL = os.getenv("https://discord.com/api/webhooks/1483873834024304772/T9bbCviBm_sJRZH3NMpYGBSQ3ErN5V7X_j1SYaAUCfQEHqLwB0gCpXA7yL8EqEB3UBFh")

@app.route("/")
def home():
    return "OK", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        print("===== WEBHOOK HIT =====", flush=True)

        # 🔥 NEBENAUDOJAM get_json
        raw = request.get_data(as_text=True)
        print("RAW:", raw, flush=True)

        if not DISCORD_WEBHOOK_URL:
            print("NO WEBHOOK URL", flush=True)
            return "error", 500

        msg = {
            "content": f"📦 Stock update:\n```{raw[:1500]}```"
        }

        r = requests.post(DISCORD_WEBHOOK_URL, json=msg)
        print("DISCORD:", r.status_code, flush=True)

        return "ok", 200

    except Exception as e:
        print("ERROR:", str(e), flush=True)
        print(traceback.format_exc(), flush=True)
        return "fail", 500
