import discord
from discord.ext import commands
from discord import app_commands
from datetime import timedelta

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def timeout_member(self, interaction: discord.Interaction , member: discord.Member, reason: str,time: int = 5):
        pesan = f"{member.mention} terkena timeout selama {time} oleh {interaction.user.mention} "
        if reason is not None:
            pesan += f"karena {reason}"
        
        await member.timeout(timedelta(minutes=time), reason=pesan)
        await interaction.response.send_message(pesan)

    @app_commands.command(name="timeout", description="Memberikan timeout kepada member (hanya admin)!")
    async def timeout(self, interaction: discord.Interaction, member: discord.Member, waktu: int, reason: str | None=None):
        if interaction.user.get_role(1368738665165226096) not in interaction.user.roles:
            await interaction.response.send_message(f"Command ini hanya bisa digunakan oleh {interaction.guild.owner.mention}!")
        else:
            await self.timeout_member(interaction=interaction, member = member, reason=reason, time=waktu)
                


async def setup(bot):
    await bot.add_cog(Moderation(bot=bot))