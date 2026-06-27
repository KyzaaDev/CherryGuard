import discord
from discord.ext import commands
from discord import app_commands

class SetupBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ngatur role ke channel yang dibuat
    async def role_setting(self, guild: discord.Guild):
        role_everyone = guild.default_role
        role_author = guild.owner
        role_bot = guild.me


        overwrite_everyone = discord.PermissionOverwrite(view_channel=True, send_messages=False, manage_channels=False)
        overwrite_author = discord.PermissionOverwrite(view_channel=True, send_messages=True, manage_channels=True)
        overwrite_bot = discord.PermissionOverwrite(view_channel=True, send_messages=True, manage_channels=False)

        overwrites = {
            role_everyone: overwrite_everyone,
            role_author: overwrite_author,
            role_bot: overwrite_bot
        }

        return overwrites

    # ini buat ngebikin channel nya bang wlee
    async def create_channel(self, guild: discord.Guild,category: discord.CategoryChannel):
        try:
            role_permissions_channel = await self.role_setting(guild=guild)
            owner = guild.owner or await guild.fetch_owner()

            log_channel = await guild.create_text_channel("log-info", category=category, overwrites=role_permissions_channel)
            welcome_channel = await guild.create_text_channel("👋welcome-goodbye", category=category, overwrites=role_permissions_channel)

            try:
                pesan_dm = (
                f"**Notifikasi Pembuatan Channel**\n"
                f"Berhasil membuat channel berikut di server **{guild.name}** (Kategori: **{category.name}**):\n"
                f"1. {welcome_channel.mention}\n"
                f"2. {log_channel.mention}\n"
                f"**<----SETUP {guild.name.upper()} SELESAI---->**"
                )
                await owner.send(pesan_dm)

            except discord.Forbidden as df:
                print(f"[DM Log] Gagal mengirim DM ke owner {owner.name} karena DM dikunci/ditutup.")

        except discord.Forbidden as df:
            print(f"[Create Channel Log] Gagal membuat channel: {df}")
        except Exception as e:
            print(f"[Create Channel Log] Gagal membuat channel: {e}")


    # Logic and function setup guild 
    async def create_category(self, guild: discord.Guild):
        owner = guild.owner or await guild.fetch_owner()

        try:
            if not guild.me.guild_permissions.manage_channels:
                try:
                    await owner.send(f"Bos role yang lebih tinggi boss")
                    await owner.send(f"Jalankan !setup setelah memberi bot role yang lebih tinggi!")
                except discord.Forbidden:
                    print(f"[{guild.name}] Gagal memberi tahu owner {owner.name}")
                return

            kategori = await guild.create_category("--enterance--")

            try:
                await owner.send(f"**<----MEMULAI SETUP {guild.name.upper()}---->**")
                await owner.send(f"Berhasil membuat category **{kategori.name}** di server **{guild.name}**!")
                await owner.send(f"Membuat channel pada category **{kategori.name}** di server **{guild.name}**!")
                await self.create_channel(guild=guild, category=kategori)
            except discord.Forbidden:
                print(f"[{guild.name}] Kategori dibuat, tapi gagal DM owner {owner.name}.")

        except discord.Forbidden as dF:
            print(f"[Create Category Log] Gagal membuat kategori: {dF}")
        except Exception as e:
            print(f"[Create Category Log] Gagal membuat kategori: {e}")

    @commands.is_owner()
    @commands.command(name="setup_bot")
    async def nasi_goreng_pak_slamet(self, ctx):
        if discord.utils.get(ctx.guild.categories, name="--enterance--") is None:
            await self.create_category(ctx.guild)
        else:
            print(f"[Setup Log] Setup guild {ctx.guild.name} sudah selesai dilakukan!")


    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        KATEGORI = discord.utils.get(guild.categories, name="--enterance--")

        if KATEGORI is None:
            await self.create_category(guild=guild)
        else:
            owner = guild.owner or await guild.fetch_owner()
            await owner.send(f"Categorynya udah ada bang!")

async def setup(bot):
    await bot.add_cog(SetupBot(bot=bot))