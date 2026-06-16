import discord
from discord.ext import commands
import asyncio
import datetime
from dotenv import load_dotenv
import io
import os
import aiohttp

load_dotenv()

with open("BLOCK_NAME.txt", "r") as name:
    block_nama = name.readlines()


intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

# bagian command
@bot.command()
async def halo(ctx):
    await ctx.send(f"hallo {ctx.author.mention}!")

# def def biasa
async def give_role(member: discord.Member):
    role = discord.utils.get(member.guild.roles, id=1368739571898122382)
    await member.add_roles(role)
    return

# untuk bagian event
@bot.event
async def on_member_join(member):
    CHANNEL_TESTING = bot.get_channel(1516429156982853682)
    avatar_url = member.display_avatar.url
    username = member.name
    generate_image_url = f"https://api.popcat.xyz/v2/welcomecard?background=https://www.image2url.com/r2/default/images/1781607789319-903d026c-ca07-4c31-b3dd-b31a2adf8d9d.png&text1={username}&text2=Welcome%20di%20selamat%20datang&text3=Semoga%20betah%20mereun&avatar={avatar_url}"

    async with aiohttp.ClientSession() as session:
        async with session.get(generate_image_url) as response:
            if response.status == 200:
                raw_image = await response.read()
                gambar_file = io.BytesIO(raw_image)

                await CHANNEL_TESTING.send(f"Wel wel kam kam welkam {member.mention}", file=discord.File(gambar_file, filename="testing.png"))
                await give_role(member)

@bot.event
async def on_member_remove(member):
    CHANNEL_TESTING = bot.get_channel(1516257116078342255)
    avatar_url = member.display_avatar.url
    username = member.name
    member_count = member.guild.member_count
    generate_image_url = f"https://api.popcat.xyz/v2/welcomecard?background=https://www.image2url.com/r2/default/images/1781607789319-903d026c-ca07-4c31-b3dd-b31a2adf8d9d.png&text1={username}&text2=Selamat%20goodbye&text3=ga%20betah%20ceunah&avatar={avatar_url}"

    async with aiohttp.ClientSession() as session:
        async with session.get(generate_image_url) as response:
            if response.status == 200:
                raw_image = await response.read()
                gambar_file = io.BytesIO(raw_image)

                await CHANNEL_TESTING.send(f"Bye bye {member.mention}", file=discord.File(gambar_file, filename="testing.png"))

@bot.event
async def on_ready():
    print(self_name := f"Mantep nih mantep, {bot.user} udah ongleng")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    pesan_lower = message.content.lower()
    message_author = message.author.mention
    
    if pesan_lower == "p":
        await message.channel.send("https://www.image2url.com/r2/default/images/1781608986059-0130cb64-c5cd-477d-baf5-ce99ebfc0d76.png")
        return

    for daftar_block in block_nama:
        kata_blokir = daftar_block.strip().lower()

        if kata_blokir in pesan_lower:
            await message.delete()
            await message.author.timeout(datetime.timedelta(minutes=5), reason="Stop ngetik K-Word")
            await message.channel.send("https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExd2t0aTZvanA3cm1wdnFzNzFqZGlmbnJ5dDlzb2g2dTJwZXc2OWh5dyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/jaPdCoXpjnI8BLZGwv/giphy.gif")
            await asyncio.sleep(0.1)
            await message.channel.send(f"{message_author} tolong ketikannya lebih dijaga ya!")
            return
        
    await bot.process_commands(message)

bot.run(os.getenv("DISCORD_TOKEN"))
