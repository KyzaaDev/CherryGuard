import discord
from discord.ext import commands

class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def halo(self, ctx):
        await ctx.channel.send(f"Halo juga {ctx.author.mention}! ada yang bisa dibantu?")
        
async def setup(bot):
    await bot.add_cog(Basic(bot))