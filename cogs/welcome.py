import discord
from discord.ext import commands
import aiohttp
import io

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # beri role untuk member baru join
    async def give_role(self, member: discord.Member):
        role_id = member.guild.get_role(1368739571898122382)
        await member.add_roles(role_id)

    # Event kalo ada member yang join
    @commands.Cog.listener()
    async def on_member_join(self, member):
        avatar_url = member.display_avatar.url
        welcome_channel = discord.utils.get(member.guild.text_channels, name="👋welcome-goodbye")
        username = member.name
        generate_image = f"https://api.popcat.xyz/v2/welcomecard?background=https://www.image2url.com/r2/default/images/1781607789319-903d026c-ca07-4c31-b3dd-b31a2adf8d9d.png&text1={username}&text2=Welcome%20di%20selamat%20datang&text3=Semoga%20betah%20mereun&avatar={avatar_url}"

        async with aiohttp.ClientSession() as session:
            async with session.get(generate_image) as response_image:
                if response_image.status == 200:
                    file_raw = await response_image.read()
                    data_image = io.BytesIO(file_raw)
                
                    if welcome_channel and welcome_channel.permissions_for(member.guild.me).send_messages:
                        await welcome_channel.send(f"Wel wel kam kam welkam {member.mention}....", file=discord.File(data_image, filename="welcome.png"))
                        await self.give_role(member)
                    else:
                        pass
    
    # Event kalo ada member yang keluar
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        avatar_url = member.display_avatar.url
        welcome_channel = discord.utils.get(member.guild.text_channels, name="👋welcome-goodbye")
        username = member.name
        generate_image = f"https://api.popcat.xyz/v2/welcomecard?background=https://www.image2url.com/r2/default/images/1781607789319-903d026c-ca07-4c31-b3dd-b31a2adf8d9d.png&text1={username}&text2=Selamat%20goodbye&text3=ga%20betah%20ceunah&avatar={avatar_url}"

        async with aiohttp.ClientSession() as session:
            async with session.get(generate_image) as response_image:
                if response_image.status == 200:
                    file_raw = await response_image.read()
                    data_image = io.BytesIO(file_raw)

                    if welcome_channel and welcome_channel.permissions_for(member.guild.me).send_messages:
                        await welcome_channel.send(f"Yahh masa keluar lee {member.mention}....", file=discord.File(data_image, filename="welcome.png"))
                    else:
                        pass

async def setup(bot):
    await bot.add_cog(Welcome(bot))