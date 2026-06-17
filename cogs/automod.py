import discord
from discord.ext import commands
import asyncio
import datetime
import os

class Automod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        with open(os.path.join(os.path.dirname(__file__), "BLOCK_NAME.txt"), "r") as blacklist_words:
            self.lists_block = blacklist_words.readlines()
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        user_message = message.content.lower()
        message_author = message.author

        for word in self.lists_block:
            kata_blockir = word.strip().lower()
            if kata_blockir in user_message:
                try:
                    if message.guild.get_role(1368738665165226096) in message.author.roles:
                        pass
                    else:
                        await message.delete()
                        await message.author.timeout(datetime.timedelta(minutes=1), reason="Stop yh ngasih K-word")
                        await message.channel.send("https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExd2t0aTZvanA3cm1wdnFzNzFqZGlmbnJ5dDlzb2g2dTJwZXc2OWh5dyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/jaPdCoXpjnI8BLZGwv/giphy.gif")
                        await asyncio.sleep(0.1)
                        await message.channel.send(f"{message_author.mention} tolong ketikannya lebih dijaga ya!")
                except discord.Forbidden:
                    print(f"Tidak bisa menghapus pesan {message.author.name}")

async def setup(bot):
    await bot.add_cog(Automod(bot))