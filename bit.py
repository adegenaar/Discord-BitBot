import os
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix="!")
channels = ["commands"]


@bot.event
async def on_ready():
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("------")


@bot.event
async def on_member_join(member):
    for channel in member.server.channels:
        print(channel)
        if channel == "general":
            await member.send(f"""Welcome to the server {member.mention}!""")


@bot.command()
async def joined(ctx, member: discord.Member):
    """Says when a member joined."""
    await ctx.send("{0.name} joined in {0.joined_at}".format(member))


@bot.command()
async def ping(ctx):
    if ctx.channel.name.lower() in channels:
        await ctx.send("pong")


@bot.command()
async def hello(ctx):
    if ctx.channel.name.lower() in channels:
        await ctx.send("Hi!")


@bot.command()
async def users(ctx):
    if ctx.channel.name.lower() in channels:
        await ctx.send(f"""# of members: {ctx.guild.member_count}""")


@bot.command()
async def guild(ctx):
    print(ctx.channel)
    if ctx.channel.name.lower() in channels:
        await ctx.send(f"""guild: {ctx.guild.name}""")


token = os.environ.get("DISCORD_BOT_TOKEN")

bot.run(token)

