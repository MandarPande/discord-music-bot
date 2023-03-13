import logging
import os
import random

import discord
from discord import Member, Message, VoiceProtocol
from discord.ext import commands
from discord.ext.commands import Context
from discord.utils import get
from dotenv import load_dotenv

from beatbot.ytdl import YTDLSource

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)
LOG = logging.getLogger(__name__)

# Basic Bot Events

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connect to Discord!')


@bot.event
async def on_member_join(member: Member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord Server!'
    )


# Bot Join / Leave Activity Commands

@bot.command(name='join', help='Tells the bot to join the voice channel')
async def join(ctx: Context, force: str = None):
    voice_client = get(ctx.bot.voice_clients, guild=ctx.guild)
    if not ctx.message.author.voice:
        await ctx.send(f'{ctx.message.author.voice} is not connected to a voice channel')
        return
    elif voice_client and voice_client.is_connected():
        if force and force.lower() == 'force':
            await voice_client.disconnect(force=True)
            await connect_to_voice_channel(ctx)
        else:
            await ctx.send(
                f'BeatBot is already connect to voice channel. If you want BeatBot to force connect to your channel, please type !join force')
            return
    else:
        await connect_to_voice_channel(ctx)


async def connect_to_voice_channel(ctx: Context):
    channel = ctx.message.author.voice.channel
    await channel.connect()


@bot.command(name='leave', help='Tells the bot to leave the voice channel')
async def leave(ctx: Context):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect(force=True)
    else:
        await ctx.send("The bot is not connected to a voice channel.")


# Bot Music Control Commands


@bot.command(name='play_song', help='Play a song')
async def play(ctx: Context, url: str):
    # try:
    server = ctx.message.guild
    voice_channel = server.voice_client

    async with ctx.typing():
        filename = await YTDLSource.from_url(url, loop=bot.loop)
        voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename))
    await ctx.send(f'**Now Playing:** {filename}')
    # except Exception as e:
    #     LOG.error(f"Following error occurred : {e}")
    #     await ctx.send("The bot is not connect to a voice channel")


@bot.command(name='pause', help='This command pauses the song')
async def pause(ctx: Context):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.pause()
    else:
        await ctx.send("The bot is not playing anything at the moment")


@bot.command(name='resume', help='Resumes the song')
async def resume(ctx: Context):
    voice_client = ctx.message.guild.voice_client
    if voice_client.paused():
        await voice_client.resume()
    else:
        await ctx.send("The bot was not playing anything before this. Use play_song command")


@bot.command(name='stop', help='Stops the song')
async def stop(ctx: Context):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.stop()
    else:
        await ctx.send("The bot is not playing anything at the moment")


bot.run(TOKEN)
