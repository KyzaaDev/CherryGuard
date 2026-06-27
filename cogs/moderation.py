import discord
from discord.ext import commands
from discord import app_commands
from datetime import timedelta

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # function broadcast log moderation
    async def broadcast_timeout(self, interaction: discord.Interaction, member: discord.Member, reason: str, time: int):
        BROADCAST_CHANNEL = discord.utils.get(interaction.guild.text_channels, name="log-moderasi")
        
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
        else:
            pass

    # function untuk ngasih timeout member yang di tag
    async def timeout_member(self, interaction: discord.Interaction , member: discord.Member, reason: str,time: int):
        pesan = f"{member.mention} terkena timeout selama {time} menit oleh {interaction.user.mention} "
        pesan += f" karena {reason}" if reason is not None else ""
        timeout_console_message_failure = f"[Timeout Log] gagal memberi timeout {member.name}: "

        try:
            await member.timeout(timedelta(minutes=time), reason=pesan)

            # kasih pesan ke log moderation
            await self.broadcast_timeout(interaction, member=member, reason=reason, time=time)
            await interaction.followup.send(pesan)
            print(f"[Timeout Log] berhasil memberi timeout {member.name}")

        except discord.Forbidden as dF:
            await interaction.followup.send(f"Gagal memberi timeout kepada {member.mention} dikarenakan tidak memiliki permission!", ephemeral=True)
            print(timeout_console_message_failure + f"{dF}")

        except Exception as e:
            await interaction.followup.send(f"Gagal memberi timeout karena terjadi kesalahan:\n{e}")
            print(timeout_console_message_failure + f"{e}")            

    # core function
    @app_commands.command(name="timeout", description="Memberikan timeout kepada member (hanya admin atau pemilik server)!")
    async def timeout(self, interaction: discord.Interaction, member: discord.Member, reason: str | None=None, waktu: int = 5):
        # cek yang jalanin command owner apa bukan
        if interaction.user.id != interaction.guild.owner_id:
            await interaction.response.send_message(f"Command ini hanya bisa digunakan oleh {interaction.guild.owner.mention}!", ephemeral=True)
            return
            
        # cek apakah owner mencoba timeout dirinya sendiri
        if interaction.user.id == member.id:
            await interaction.response.send_message("Bang, masa lu mau ngetime out akun lu sendiri sih", ephemeral=True)
            return
            
        # cek apakah owner mencoba timeout bot discord
        if interaction.guild.me.id == member.id:
            await interaction.response.send_message("Serius bang lu mau ngetime out gua?", ephemeral=True)
            return
        
        await interaction.response.defer(ephemeral=True)
        await self.timeout_member(interaction=interaction, member=member, reason=reason, time=waktu)

async def setup(bot):
    await bot.add_cog(Moderation(bot=bot))