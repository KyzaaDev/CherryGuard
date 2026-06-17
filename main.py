import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.messages = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(self_name := f"Bot {bot.user.name} sudah aktif!")

async def setup_hook():
    print("Memuat Cogs!")
    for cog in os.listdir("./cogs"):
        if cog.endswith(".py"):
            try:
                await bot.load_extension(f"cogs.{cog[:-3]}")
                print(f"Berhasil memuat cogs: {cog[:-3]}")
            except Exception as e:
                print(f"Gagal memuat cogs: {e}")
    print("Berhasil memuat semua cogs!")            

bot.setup_hook = setup_hook
bot.run(os.getenv("DISCORD_TOKEN"))    