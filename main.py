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
        raw_body = request.get_data(as_text=True)
        print("===== WEBHOOK HIT =====", flush=True)
        print("RAW BODY:", raw_body, flush=True)

        data = request.get_json(silent=True)
        print("PARSED JSON:", data, flush=True)

        if not DISCORD_WEBHOOK_URL:
            print("ERROR: DISCORD_WEBHOOK_URL is missing", flush=True)
            return jsonify({"error": "DISCORD_WEBHOOK_URL missing"}), 500

        payload = {
            "content": f"SellAuth webhook received:\n```{raw_body[:1500]}```"
        }

        resp = requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=15)
        print("DISCORD STATUS:", resp.status_code, flush=True)
        print("DISCORD RESPONSE:", resp.text, flush=True)

        return jsonify({"ok": True}), 200

    except Exception as e:
        print("EXCEPTION:", str(e), flush=True)
        print(traceback.format_exc(), flush=True)
        return jsonify({"error": str(e)}), 500
