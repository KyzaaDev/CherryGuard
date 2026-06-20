import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime 

class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="halo", description="Menyapa user")
    async def halo(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Halo juga {interaction.user.mention}! ada yang bisa dibantu?")

    @app_commands.command(name="sapa", description="menyapa teman kamu atau dirimu!")
    async def sapa(self, interaction: discord.Interaction, target: discord.Member | None=None, pesan: str | None = None):
        if pesan is None:
            pesan = "Hallooo"

        if target is None:
            await interaction.response.send_message(f"{pesan} {interaction.user.mention}!")
        else:
            await interaction.response.send_message(f"{pesan} {target.mention}")

async def setup(bot):
    await bot.add_cog(Basic(bot))