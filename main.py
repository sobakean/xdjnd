import discord from discord.ext import commands import youtube_dl import os

TOKEN = os.getenv("DISCORD_TOKEN") or "PASTE_YOUR_TOKEN_HERE"

intents = discord.Intents.default() bot = commands.Bot(command_prefix='!', intents=intents)

Настройка youtube_dl

ydl_opts = { 'format': 'bestaudio/best', 'postprocessors': [{ 'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192', }], 'outtmpl': 'song.%(ext)s', }

@bot.command() async def play(ctx, url): if not ctx.author.voice: await ctx.send("Йоу, мафия, ты не в голосовом канале!") return

channel = ctx.author.voice.channel
voice_client = ctx.voice_client
if not voice_client:
    voice_client = await channel.connect()

with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])

voice_client.play(discord.FFmpegPCMAudio("song.mp3"))
await ctx.send("Врубаю музло, брошка!")

@bot.command() async def stop(ctx): if ctx.voice_client: await ctx.voice_client.disconnect() await ctx.send("Музыка остановлена, брат!")

bot.run(TOKEN)

