import os
import random

import discord
from discord import Member, Message, VoiceProtocol
from discord.ext import commands
from discord.ext.commands import Context
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

brooklyn_99_quotes = [
    'I\'m the human form of the 💯 emoji.',
    'Bingpot!',
    (
        'Cool. Cool cool cool cool cool cool cool, '
        'no doubt no doubt no doubt no doubt.'
    ),
]


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connect to Discord!')


@bot.event
async def on_member_join(member: Member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord Server!'
    )


@bot.command(name='99', help='Responds with a random quote from Brooklyn 99')
async def nine_nine(ctx: Context):
    response = random.choice(brooklyn_99_quotes)
    await ctx.send(response)


@bot.command(name='join', help='Tells the bot to join the voice channel')
async def join(ctx: Context):
    # todo : check if bot is already connected to the same vc
    voice_client = ctx.message.guild.voice_client
    if not ctx.message.author.voice:
        await ctx.send(f'{ctx.message.author.voice} is not connected to a voice channel')
        return
    elif voice_client.is_connected():
        await ctx.send(f'{ctx.message.author.voice} is already connect to voice channel')
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()


@bot.command(name='leave', help='Tells the bot to leave the voice channel')
async def leave(ctx: Context):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")


bot.run(TOKEN)
