import discord
from discord.ext import commands
import youtube_dl
import asyncio

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

queues = {}

def check_queue(ctx, id):
    if queues.get(id) != []:
        voice = ctx.guild.voice_client
        source = queues[id].pop(0)
        voice.play(source, after=lambda x=None: check_queue(ctx, id))

@bot.command()
async def join(ctx):
    if ctx.author.voice:
        await ctx.author.voice.channel.connect()

@bot.command()
async def play(ctx, url):
    if ctx.voice_client is None:
        await ctx.invoke(join)

    ydl_opts = {'format': 'bestaudio'}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        URL = info['url']
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    voice = ctx.guild.voice_client
    source = discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS)

    if voice.is_playing():
        guild_id = ctx.message.guild.id
        if guild_id in queues:
            queues[guild_id].append(source)
        else:
            queues[guild_id] = [source]
        await ctx.send("Добавлено в очередь!")
    else:
        voice.play(source, after=lambda x=None: check_queue(ctx, ctx.message.guild.id))
        await ctx.send("Врубаю, мафия!")

@bot.command()
async def stop(ctx):
    await ctx.voice_client.disconnect()
    queues[ctx.message.guild.id] = []

bot.run("ТВОЙ_ТОКЕН_ОТСЮДА https://discord.com/developers/applications")
