import discord
from discord.ext import commands
from discord import app_commands

class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def halo(self, ctx):
        await ctx.channel.send(f"Halo juga {ctx.author.mention}! ada yang bisa dibantu?")

    @app_commands.command(name="halo", description="Menyapa user")
    async def halo(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Halo juga {interaction.user.mention}! ada yang bisa dibantu?")
        
async def setup(bot):
    await bot.add_cog(Basic(bot))