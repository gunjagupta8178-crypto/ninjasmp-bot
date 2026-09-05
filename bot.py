import os
import threading
from flask import Flask
import discord
from discord.ext import commands

app = Flask(__name__)
@app.route('/')
def home():
    return "NinjaSMP Bot is Online!"

def run_web():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} is online!')

@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(bot.latency*1000)}ms')

threading.Thread(target=run_web).start()
bot.run(os.environ.get("TOKEN"))
