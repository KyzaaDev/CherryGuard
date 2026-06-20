import discord
from discord.ext import commands
from discord import app_commands

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="profile", description="Melihat profile kamu ataupun temanmu!")
    @app_commands.guild_only()
    async def profile(self, interaction: discord.Interaction, member: discord.Member | None = None):
        user = member if member is not None else interaction.user
        embed_profile = discord.Embed(
            title=f"{user.name} Profile",
            color=user.color
        )
        
        # variable timestamp
        created_at = int(user.created_at.timestamp())
        join_at = int(user.joined_at.timestamp())

        # info dasar member 
        embed_profile.description = f" **Informasi Member {user.mention}**"
        embed_profile.add_field(name="User ID", value=f"`{user.id}`", inline=False)

        # thumbnail pake profile user
        embed_profile.set_thumbnail(url=user.display_avatar)

        # footer discord
        embed_profile.set_footer(text=f"{self.bot.user.name} © 2026", icon_url=self.bot.user.avatar.url)


        # info akun member, mencakup kapan dibuat, dan kapan gabung ke server
        embed_profile.add_field(name="Akun dibuat", value=f"<t:{created_at}:D>\n(<t:{created_at}:R>)")
        embed_profile.add_field(name="\u200b", value="\u200b", inline=True)
        embed_profile.add_field(name="Bergabung ke server", value=f"<t:{join_at}:D>\n(<t:{join_at}:R>)")

        # ambil semua role user
        roles = [role.mention for role in user.roles if not role.is_default()]
        embed_profile.add_field(name="Roles", value=f"{(', ').join(roles)}")

        await interaction.response.send_message(embed=embed_profile)
        

async def setup(bot):
    await bot.add_cog(Info(bot=bot))