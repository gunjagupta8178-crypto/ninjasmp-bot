import discord
from discord.ext import commands
import os
from flask import Flask
from threading import Thread

app = Flask('')
@app.route('/')
def home():
    return "Bot is Online!"

def run_web():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=".", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} is online!")

@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong! {round(bot.latency*1000)}ms")

@bot.command()
async def status(ctx):
    members = ctx.guild.member_count
    embed = discord.Embed(
        title="⚡ NinjaSMP - Server Status",
        description=f"**Server is ONLINE**\nTotal Members: **{members}**",
        color=0x2ecc71
    )
    embed.add_field(name="🌐 Java IP", value="`play.ninjasmp.in`", inline=True)
    embed.add_field(name="💬 Discord Members", value=f"**{members}**", inline=True)
    embed.add_field(name="🎮 Mode", value="`Lifesteal SMP`", inline=True)
    embed.set_footer(text="NinjaSMP • Live Count")
    await ctx.send(embed=embed)

Thread(target=run_web).start()
bot.run(os.environ.get("TOKEN") or os.environ.get("DISCORD_TOKEN"))
