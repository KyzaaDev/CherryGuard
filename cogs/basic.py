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

    @app_commands.command(name="profile", description="Melihat profile kamu ataupun temanmu!")
    @app_commands.guild_only()
    async def profile(self, interaction: discord.Interaction, member: discord.Member | None = None):
        user = member if member is not None else interaction.user
        embed_profile = discord.Embed(
            title=f"{user.name} Profile",
            color=user.color
        )
        
        embed_profile.description = f" **Informasi Member {user.mention}**"
        embed_profile.add_field(name="User ID", value=f"`{user.id}`")
        embed_profile.set_thumbnail(url=user.avatar.url)

        embed_profile.set_footer(text=f"{self.bot.user.name} © 2026", icon_url=self.bot.user.avatar.url)
        embed_profile.add_field(name="\u200b", value="\u200b", inline=True)

        await interaction.response.send_message(embed=embed_profile)
        
async def setup(bot):
    await bot.add_cog(Basic(bot))