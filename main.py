from flask import Flask, request
import os
import discord
from discord.ext import commands

app = Flask(__name__)

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
GUILD_ID = int(os.getenv("DISCORD_GUILD_ID"))
REVIEWS_CHANNEL_ID = int(os.getenv("REVIEWS_CHANNEL_ID"))
SALES_CHANNEL_ID = int(os.getenv("SALES_CHANNEL_ID"))
STOCK_CHANNEL_ID = int(os.getenv("STOCK_CHANNEL_ID"))

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

def run_bot():
    import threading
    def _run():
        bot.run(DISCORD_BOT_TOKEN)
    threading.Thread(target=_run, daemon=True).start()

@app.route("/")
def home():
    return {"status": "ok"}

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    print("SELLAUTH EVENT:", data)

    event = data.get("event")

    if event == "order:completed":
        product = data.get("product_name", "Unknown")
        price = data.get("price", "0")

        channel = bot.get_channel(SALES_CHANNEL_ID)
        if channel:
            embed = discord.Embed(
                title="💰 New Purchase",
                description=f"**{product}** bought for **${price}**",
                color=0x00ff00
            )
            bot.loop.create_task(channel.send(embed=embed))

    elif event == "review:created":
        review = data.get("review", "No text")
        rating = data.get("rating", "0")

        channel = bot.get_channel(REVIEWS_CHANNEL_ID)
        if channel:
            embed = discord.Embed(
                title="⭐ New Review",
                description=review,
                color=0xffff00
            )
            embed.add_field(name="Rating", value=f"{rating}/5")
            bot.loop.create_task(channel.send(embed=embed))

    elif event == "product:stock_updated":
        product = data.get("product_name", "Unknown")

        channel = bot.get_channel(STOCK_CHANNEL_ID)
        if channel:
            embed = discord.Embed(
                title="📦 Stock Updated",
                description=f"**{product}** stock updated",
                color=0x3498db
            )
            bot.loop.create_task(channel.send(embed=embed))

    return {"status": "ok"}, 200

if __name__ == "__main__":
    run_bot()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
