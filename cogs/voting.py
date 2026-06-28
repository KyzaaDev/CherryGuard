import discord
from discord.ext import commands
from discord import app_commands
import time

class VoteView(discord.ui.View):
    def __init__(self, *, timeout = 180, topik: str, deskripsi: str, opsi1: str, opsi2: str):
        super().__init__(timeout=timeout)
        
        # variable topik, deskripsi dan opsi
        self.topik = topik
        self.deskripsi = deskripsi
        self.pilihan1 = opsi1
        self.pilihan2 = opsi2

        # simpan daftar pemilih
        self.pemilih = set()

        # encounter pilihan
        self.pilihan1_enjoyer = 0
        self.pilihan2_enjoyer = 0

        # ubah nama opsi berdasarkan opsi yang tersedia
        self.tombol_opsi1.label = opsi1
        self.tombol_opsi2.label = opsi2
    
    def get_embed(self, interaction: discord.Interaction):
        second_time = int(time.time() + self.timeout)

        embed = discord.Embed(
            title=f"📊  {self.topik.upper()}", 
            description="-" * 42 +f"\n⏳**Status**: berakhir <t:{second_time}:R>",
            color=discord.Colour.purple()
        )

        embed.add_field(
            name=f"Tim {self.pilihan1}",
            value=f"**{self.pilihan1_enjoyer}** suara",
            inline=True
        )
        
        # Field kosong tengah dikecilkan spacernya biar gak terlalu renggang
        embed.add_field(
            name="\u200b",
            value="\u200b",
            inline=True
        )

        embed.add_field(
            name=f"Tim {self.pilihan2}",
            value=f"**{self.pilihan2_enjoyer}** suara",
            inline=True
        )

        embed.set_footer(text="Gunakan tombol di bawah untuk memberikan suara!")
        embed.set_author(name=interaction.user.display_name,icon_url=interaction.user.display_avatar.url)

        return embed

    @discord.ui.button(label="Opsi 1", style=discord.ButtonStyle.primary)
    async def tombol_opsi1(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id in self.pemilih:
            return await interaction.response.send_message("Maaf ga bisa milih lagi lee", ephemeral=True)

        # update encounter
        self.pilihan1_enjoyer += 1

        # update embed
        self.pemilih.add(interaction.user.id)
        await interaction.response.edit_message(embed=self.get_embed(interaction), view=self)
        await interaction.followup.send(f"{interaction.user.mention} memilih {self.pilihan1}")

    @discord.ui.button(label="Opsi 2", style=discord.ButtonStyle.secondary)
    async def tombol_opsi2(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id in self.pemilih:
            return await interaction.response.send_message("Maaf ga bisa milih lagi lee", ephemeral=True)
        # update encounter
        self.pilihan2_enjoyer += 1
        
        # update embed
        self.pemilih.add(interaction.user.id)
        await interaction.response.edit_message(embed=self.get_embed(interaction), view=self)
        await interaction.followup.send(f"{interaction.user.mention} memilih {self.pilihan2}")

class Voting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="voting", description="Mulai polling cepat untuk menentukan suatu pilihan atau topik.")
    async def vote_start(self, interaction: discord.Interaction, topik: str, deskripsi: str, opsi1: str, opsi2: str):
        await interaction.response.defer()

        vote = VoteView(topik = topik, deskripsi = deskripsi, opsi1 = opsi1, opsi2 = opsi2)

        await interaction.followup.send(f"**{interaction.user.mention} MEMULAI VOTING**", embed = vote.get_embed(interaction), view=vote)


async def setup(bot):
    await bot.add_cog(Voting(bot=bot))

