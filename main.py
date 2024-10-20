import os, nextcord
from utils.database import Database
from nextcord.ext import commands
from dotenv import load_dotenv

from utils.logs import success, info, error, warning
from utils.database import Database

load_dotenv()

db = Database()

bot = commands.Bot(command_prefix="$$", intents=nextcord.Intents.all())

@bot.event
async def on_ready():
    
    success("Bot is ready!")

    bot.activity = nextcord.Activity(type=nextcord.ActivityType.watching, name=f"{len(bot.guilds)} server | !info")
    await bot.change_presence(activity=bot.activity)

@bot.event
async def on_close():
    info("Closing the bot!")
    db.close()

@bot.event
async def on_guild_join(guild):
    db.execute_query("INSERT INTO guilds (guild_id) VALUES (%s)", (guild.id,))
    success(f"Joined the guild: {guild.name}")

# Loading discord cogs
for root, dirs, files in os.walk("cogs"):
    root = root.replace("\\", ".")
    for file in files:
        if file.endswith(".py"):
            name = file[:-3]
            bot.load_extension(f"{root}.{name}")
            info(f"Loaded cog: {name}")

bot.run(os.getenv("CLIENT_TOKEN"))