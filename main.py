import os
import asyncio
from dotenv import load_dotenv
import discord
from discord.ext import commands
from pytube import YouTube

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Ма бой {bot.user} подключился к Discord!')

@bot.command()
async def play(ctx, url):
    voice_channel = ctx.author.voice.channel
    if not voice_channel:
        await ctx.send("Ты не в войсе, мафия!")
        return

    vc = await voice_channel.connect()
    yt = YouTube(url)
    audio = yt.streams.filter(only_audio=True).first()
    file_path = audio.download(filename="song.mp4")

    vc.play(discord.FFmpegPCMAudio("song.mp4"), after=lambda e: print("Проигралось!"))
    await ctx.send(f"Врубаю для тебя, браза: {yt.title}")

@bot.command()
async def stop(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("Музон остановлен, мафия.")
    else:
        await ctx.send("Я даже не в войсе, тип!")

bot.run(TOKEN)
