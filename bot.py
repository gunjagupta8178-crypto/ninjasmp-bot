import discord
from discord.ext import commands
import os
import json
from flask import Flask
from threading import Thread

# --- BOT SETUP ---
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix=".", intents=intents)

# --- WELCOME CHANNEL SAVE SYSTEM ---
WELCOME_FILE = "welcome_channels.json"
def load_welcome_channels():
    if os.path.exists(WELCOME_FILE):
        with open(WELCOME_FILE, "r") as f:
            return json.load(f)
    return {}
def save_welcome_channels(data):
    with open(WELCOME_FILE, "w") as f:
        json.dump(data, f)
welcome_channels = load_welcome_channels()

# --- EVENTS ---
@bot.event
async def on_ready():
    print(f"{bot.user} is online! Shivam NinjaMC Bot Ready!")

@bot.event
async def on_member_join(member):
    guild_id = str(member.guild.id)
    if guild_id not in welcome_channels:
        return
    channel = bot.get_channel(welcome_channels[guild_id])
    if channel is None:
        return

    embed = discord.Embed(
        title="🥷 Welcome to NinjaMC!",
        description=f"«⚔️ Welcome {member.mention} to **NinjaMC!** ⚔️\n\n"
                    f"The ultimate Lifesteal experience awaits you! ❤️‍🔥\n\n"
                    f"❤️ **Lifesteal SMP**\n"
                    f"⚔️ Fight • Steal Hearts • Survive\n"
                    f"🏆 Build your empire & become the strongest\n\n"
                    f"👥 Community: **{member.guild.member_count} Members**\n\n"
                    f"📜 Read <#{1520411785520218315}> before playing and check <#{1520411786879172618}> for updates! 👀\n\n"
                    f"Your hearts. Your choices. Your legacy. ❤️‍🔥\n\n"
                    f"🔥 Good luck, Ninja — see you in-game! »",
        color=0xff0000
    )
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.set_footer(text=f"NinjaMC • Member #{member.guild.member_count}")
    await channel.send(content=f"{member.mention}", embed=embed)

# --- COMMANDS ---
@bot.command()
@commands.has_permissions(administrator=True)
async def setwelcome(ctx, channel: discord.TextChannel = None):
    if channel is None:
        channel = ctx.channel
    welcome_channels[str(ctx.guild.id)] = channel.id
    save_welcome_channels(welcome_channels)
    await ctx.send(f"✅ Welcome channel set: {channel.mention}")

@bot.command()
async def ping(ctx):
    await ctx.send(f"🏓 Pong! `{round(bot.latency * 1000)}ms`")

@bot.command(name="status")
async def status_cmd(ctx):
    embed = discord.Embed(
        title="🔥 NinjaMC - Lifesteal SMP",
        description="**Server is Online!** ❤️\n\n"
                    f"**IP:** `play.ninjasmp.fun`\n"
                    f"**Version:** 1.19 - 1.21+\n"
                    f"**Mode:** Lifesteal ❤️\n\n"
                    f"Join now and steal hearts! ⚔️",
        color=0x00ff00
    )
    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url)
    await ctx.send(embed=embed)

# --- WEB SERVER FOR RENDER ---
app = Flask('')
@app.route('/')
def home():
    return "NinjaMC Bot is Online!"
def run_web():
    app.run(host='0.0.0.0', port=10000)
Thread(target=run_web).start()

# --- RUN BOT ---
bot.run(os.environ.get("TOKEN") or os.environ.get("DISCORD_TOKEN"))
