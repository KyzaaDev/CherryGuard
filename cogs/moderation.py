import discord
from discord.ext import commands
from discord import app_commands
from datetime import timedelta

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # function broadcast log moderation
    async def broadcast_timeout(self, interaction: discord.Interaction, member: discord.Member, reason: str, time: int):
        BROADCAST_CHANNEL = self.bot.get_channel(1517911475707052215)
        
        if BROADCAST_CHANNEL:
            embed_warn = discord.Embed(
                title="**🚨 MODERATION LOG: TIMEOUT**",
                description=f"Maaf yah ditime out {member.mention}",
                color=discord.Color.from_str("#ff0000")
            )        

            # ini ingfo akurat ini ingfo
            embed_warn.add_field(name="User terhukum", value=member.mention, inline=True)
            embed_warn.add_field(name="Penindak", value=interaction.user.mention, inline=False)
            embed_warn.add_field(name="Durasi", value=f"{time} Menit", inline=False)
            embed_warn.set_thumbnail(url=member.display_avatar.url)

            if reason is not None:
                embed_warn.add_field(name="Alasan", value=reason, inline=False)
            await BROADCAST_CHANNEL.send(embed = embed_warn)


    async def timeout_member(self, interaction: discord.Interaction , member: discord.Member, reason: str,time: int):
        pesan = f"{member.mention} terkena timeout selama {time} menit oleh {interaction.user.mention} "
        pesan += f" karena {reason}" if reason is not None else ""
        await member.timeout(timedelta(minutes=time), reason=pesan)

        # kasih pesan ke log moderation
        await self.broadcast_timeout(interaction, member=member, reason=reason, time=time)
        await interaction.response.send_message(pesan)

    @app_commands.command(name="timeout", description="Memberikan timeout kepada member (hanya admin)!")
    async def timeout(self, interaction: discord.Interaction, member: discord.Member, reason: str | None=None, waktu: int = 5):
        if interaction.user.get_role(1368738665165226096) not in interaction.user.roles:
            await interaction.response.send_message(f"Command ini hanya bisa digunakan oleh {interaction.guild.owner.mention}!", ephemeral=True)
        else:
            await self.timeout_member(interaction=interaction, member = member, reason=reason, time=waktu)

async def setup(bot):
    await bot.add_cog(Moderation(bot=bot))