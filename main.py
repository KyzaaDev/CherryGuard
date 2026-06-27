import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.messages = True
intents.guilds = True

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

@bot.event
async def on_command_error(ctx, error):
    app_info = await bot.application_info()
    owner = app_info.owner

    if isinstance(error, commands.NotOwner):
        await ctx.send(f"Maaf bang ownernya {owner.mention}")

#  sync slash commands
@bot.command()
@commands.is_owner()
async def sync(ctx):
    guild = ctx.guild

    await ctx.send(f"Memulai sync server: {guild.name}")

    try:
        bot.tree.copy_global_to(guild=guild)
        synced = await bot.tree.sync(guild=guild)

        await ctx.send(f"Berhasil sync {len(synced)} command slash!")
    except Exception as e:
        await ctx.send(f"Gagal sync slash command: {e}")

bot.setup_hook = setup_hook
bot.run(os.getenv("DISCORD_TOKEN"))    