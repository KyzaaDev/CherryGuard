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

        for word in self.lists_block:
            kata_blockir = word.strip().lower()
            if kata_blockir in user_message:
                try:
                    if message.guild.get_role(1368738665165226096) in message.author.roles:
                        pass
                    else:
                        await self.timeout_kword(message = message)
                except discord.Forbidden:
                    print(f"Tidak bisa menghapus pesan {message.author.name}")

    # function broadCast Moderation Log
    async def broadcast_timeout(self, message: discord.Message):
        BROADCAST_CHANNEL = self.bot.get_channel(1517911475707052215)
        
        if BROADCAST_CHANNEL:
            embed_warn = discord.Embed(
                title="**🚨 MODERATION LOG: TIMEOUT**",
                description=f"Maaf yah ditime out {message.author.mention}",
                color=discord.Color.from_str("#ff0000")
            )
            
            user = message.author

            # ini ingfo akurat ini ingfo
            embed_warn.add_field(name="User terhukum", value=user.mention, inline=True)
            embed_warn.add_field(name="Penindak", value=self.bot.user.mention, inline=False)
            embed_warn.add_field(name="Durasi", value="1 Menit", inline=False)
            embed_warn.add_field(name="Alasan", value="Ngapain coba tadi?", inline=False)
            await BROADCAST_CHANNEL.send(embed = embed_warn)

    # function timeout karena K word
    async def timeout_kword(self, message: discord.Message):

        reason = "Stop ngetik K-Word yah!"
        message_author = message

        await message.delete()
        await message.author.timeout(datetime.timedelta(minutes=1), reason=reason)
        await message.channel.send("https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExd2t0aTZvanA3cm1wdnFzNzFqZGlmbnJ5dDlzb2g2dTJwZXc2OWh5dyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/jaPdCoXpjnI8BLZGwv/giphy.gif")
        await asyncio.sleep(0.1)
        await message.channel.send(f"{message_author.author.mention} tolong ketikannya lebih dijaga ya!")
        await self.broadcast_timeout(message=message_author)

async def setup(bot):
    await bot.add_cog(Automod(bot))