import os
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv

# ==========================
# LOAD ENV
# ==========================

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

if TOKEN is None:
    raise ValueError("DISCORD_TOKEN belum ditemukan di file .env")

# ==========================
# CONFIG
# ==========================

WELCOME_CHANNEL_ID = 1468641218660667582
ROLE_ID = 1438554888845000784
VERIFY_CHANNEL_ID = 1470498490818756877
GOODBYE_CHANNEL_ID = 1468314237372993749
BOOST_CHANNEL_ID = 1470219129465208905
GUILD_ID = 1438554317647904952

WELCOME_IMAGE_URL = (
    "https://cdn.discordapp.com/attachments/"
    "1438554318260146331/1493329315344154796/standard_1.gif"
)

GOODBYE_IMAGE_URL = (
    "https://cdn.discordapp.com/attachments/"
    "1438554318260146331/1493336428321574955/standard_3.gif"
)

BOOST_IMAGE_URL = (
    "https://cdn.discordapp.com/attachments/"
    "1438554318260146331/1493557946729365564/standard_4.gif"
)

# ==========================
# INTENTS
# ==========================

intents = discord.Intents.default()

intents.members = True
intents.message_content = True
intents.voice_states = True

# ==========================
# BOT
# ==========================

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    help_command=None
)

# ==========================
# READY
# ==========================

@bot.event
async def on_ready():

    print("=" * 50)
    print(f"Login sebagai : {bot.user}")
    print(f"ID Bot        : {bot.user.id}")
    print(f"discord.py    : {discord.__version__}")
    print("=" * 50)

    if not update_status.is_running():
        update_status.start()

# ==========================
# AUTO STATUS
# ==========================

@tasks.loop(minutes=1)
async def update_status():

    guild = bot.get_guild(GUILD_ID)

    if guild is None:
        return

    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name=f"{guild.member_count} Members"
        )
    )

@update_status.before_loop
async def before_update_status():
    await bot.wait_until_ready()
# ==========================
# MEMBER JOIN
# ==========================

@bot.event
async def on_member_join(member: discord.Member):

    channel = bot.get_channel(WELCOME_CHANNEL_ID)

    if channel is None:
        print("❌ Welcome channel tidak ditemukan.")
        return

    embed = discord.Embed(
        title="👋 WELCOME",
        description=(
            "°───────── . 𖥔 ݁ ˖\n\n"
            f"➤ **Welcome** : {member.mention}\n"
            f"➤ **Server** : **{member.guild.name}**\n"
            f"➤ **Member Ke** : **{member.guild.member_count}**\n\n"
            f"Silakan ambil role di <#{VERIFY_CHANNEL_ID}>.\n"
            f"Role yang tersedia adalah <@&{ROLE_ID}>.\n\n"
            "Selamat bergabung dan semoga betah ya! 💜\n\n"
            "°───────── . 𖥔 ݁ ˖"
        ),
        color=discord.Color.purple()
    )

    embed.set_thumbnail(url=member.display_avatar.url)
    embed.set_image(url=WELCOME_IMAGE_URL)

    embed.set_footer(
        text=f"Welcome • {member.guild.name}",
        icon_url=member.guild.icon.url if member.guild.icon else None
    )

    await channel.send(
        content=f"Welcome {member.mention} 🎉",
        embed=embed
    )


# ==========================
# MEMBER LEAVE
# ==========================

@bot.event
async def on_member_remove(member: discord.Member):

    channel = bot.get_channel(GOODBYE_CHANNEL_ID)

    if channel is None:
        print("❌ Goodbye channel tidak ditemukan.")
        return

    embed = discord.Embed(
        title="👋 GOODBYE",
        description=(
            "°───────── . 𖥔 ݁ ˖\n\n"
            f"➤ **User** : **{member}**\n"
            f"➤ **Server** : **{member.guild.name}**\n"
            f"➤ **Sisa Member** : **{member.guild.member_count}**\n\n"
            "Terima kasih sudah pernah menjadi bagian dari server ini.\n"
            "Semoga sukses selalu! 💜\n\n"
            "°───────── . 𖥔 ݁ ˖"
        ),
        color=discord.Color.red()
    )

    embed.set_thumbnail(url=member.display_avatar.url)
    embed.set_image(url=GOODBYE_IMAGE_URL)

    embed.set_footer(
        text="Goodbye...",
        icon_url=member.guild.icon.url if member.guild.icon else None
    )

    await channel.send(embed=embed)


# ==========================
# SERVER BOOST
# ==========================

@bot.event
async def on_member_update(before: discord.Member, after: discord.Member):

    booster_role = after.guild.premium_subscriber_role

    if booster_role is None:
        return

    if booster_role not in before.roles and booster_role in after.roles:

        channel = bot.get_channel(BOOST_CHANNEL_ID)

        if channel is None:
            print("❌ Boost channel tidak ditemukan.")
            return

        boost_count = after.guild.premium_subscription_count
        boost_level = after.guild.premium_tier

        embed = discord.Embed(
            title="💜 NEW SERVER BOOSTER",
            description=(
                f"Terima kasih {after.mention} telah melakukan **Server Boost!**\n\n"
                f"✨ **Total Boost** : **{boost_count}**\n"
                f"🏆 **Server Level** : **Level {boost_level}**\n\n"
                "Dukunganmu sangat berarti untuk perkembangan server ini!"
            ),
            color=discord.Color.magenta()
        )

        embed.set_thumbnail(url=after.display_avatar.url)
        embed.set_image(url=BOOST_IMAGE_URL)

        embed.set_footer(
            text=after.guild.name,
            icon_url=after.guild.icon.url if after.guild.icon else None
        )

        await channel.send(
            content=f"Terima kasih {after.mention} 💜",
            embed=embed
        )
# ==========================
# AUTO REPLY
# ==========================

AUTO_REPLY = {
    "oi": "# APA WOI",
    "alo": "# SO ASIK AH",
}


@bot.event
async def on_message(message: discord.Message):

    if message.author.bot:
        return

    pesan = message.content.lower().strip()

    if pesan in AUTO_REPLY:
        await message.channel.send(AUTO_REPLY[pesan])

    await bot.process_commands(message)


# ==========================
# JOIN VOICE
# ==========================

@bot.command(
    name="join",
    help="Bot join ke Voice Channel."
)
@commands.has_permissions(administrator=True)
async def join(ctx):

    if ctx.author.voice is None:

        embed = discord.Embed(
            title="❌ Gagal",
            description="Kamu harus masuk ke Voice Channel terlebih dahulu.",
            color=discord.Color.red()
        )

        return await ctx.send(embed=embed)

    channel = ctx.author.voice.channel

    try:

        if ctx.voice_client:

            if ctx.voice_client.channel == channel:

                embed = discord.Embed(
                    title="ℹ️ Informasi",
                    description=f"Bot sudah berada di **{channel.name}**.",
                    color=discord.Color.orange()
                )

                return await ctx.send(embed=embed)

            await ctx.voice_client.move_to(channel)

        else:

            await channel.connect(reconnect=True)

        embed = discord.Embed(
            title="🔊 Voice Connected",
            description=f"Berhasil bergabung ke **{channel.name}**",
            color=discord.Color.green()
        )

        await ctx.send(embed=embed)

    except Exception as e:

        embed = discord.Embed(
            title="❌ Error",
            description=f"```{e}```",
            color=discord.Color.red()
        )

        await ctx.send(embed=embed)


# ==========================
# LEAVE VOICE
# ==========================

@bot.command(
    name="leave",
    help="Bot keluar dari Voice Channel."
)
@commands.has_permissions(administrator=True)
async def leave(ctx):

    if ctx.voice_client is None:

        embed = discord.Embed(
            title="❌ Gagal",
            description="Bot sedang tidak berada di Voice Channel.",
            color=discord.Color.red()
        )

        return await ctx.send(embed=embed)

    nama_channel = ctx.voice_client.channel.name

    await ctx.voice_client.disconnect()

    embed = discord.Embed(
        title="👋 Voice Disconnected",
        description=f"Keluar dari **{nama_channel}**",
        color=discord.Color.green()
    )

    await ctx.send(embed=embed)


# ==========================
# COMMAND ERROR
# ==========================

@join.error
@leave.error
async def voice_error(ctx, error):

    if isinstance(error, commands.MissingPermissions):

        embed = discord.Embed(
            title="❌ Permission Ditolak",
            description="Hanya **Administrator** yang dapat menggunakan command ini.",
            color=discord.Color.red()
        )

        return await ctx.send(embed=embed)

    raise error


# ==========================
# START BOT
# ==========================

if __name__ == "__main__":

    try:
        bot.run(TOKEN)

    except discord.LoginFailure:
        print("❌ DISCORD_TOKEN tidak valid.")

    except KeyboardInterrupt:
        print("\n🛑 Bot dihentikan.")

    except Exception as e:
        print(f"❌ Terjadi error: {e}")