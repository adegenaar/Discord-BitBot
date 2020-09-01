import os
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix="!")
channels = ["commands"]


@bot.event
async def on_ready():
    """on_ready Event fired when the bot has connected to Discord
    """
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("------")


@bot.event
async def on_member_join(member: discord.Member):
    """on_member_join Event is fired when a member joins the server

    Args:
        member (discord.Member): member that joined the server
    """
    for channel in member.server.channels:
        print(channel)
        if channel == "general":
            await member.send(f"""Welcome to the server {member.mention}!""")


@bot.command()
async def joined(ctx, member: discord.Member):
    """joined Says when a member joined.

    Args:
        ctx (Discord Context): Discord context object
        member (discord.Member): Member object for the new member
    """
    await ctx.send("{0.name} joined in {0.joined_at}".format(member))


@bot.command()
async def ping(ctx):
    """ping Quick status check

    Args:
        ctx (Discord Context): Context object
    """
    if ctx.channel.name.lower() in channels:
        await ctx.send("pong")


@bot.command()
async def users(ctx):
    """users Reports the number of users in the chat

    Args:
        ctx (context): Discord Context Object
    """

    if ctx.channel.name.lower() in channels:
        await ctx.send(f"""# of members: {ctx.guild.member_count}""")


@bot.command()
async def guild(ctx):
    """guild return the name of the server

    Args:
        ctx (context): Discord Context Object
    """
    print(ctx.channel)
    if ctx.channel.name.lower() in channels:
        await ctx.send(f"""guild: {ctx.guild.name}""")


@bot.command()
async def clear(ctx, messages=5):
    """clear Remove # messages from the current channel

    Args:
        ctx (context): Discord Context Object
        messages (int, optional): Number of message to remove from the current channel. Defaults to 5.
    """
    await ctx.channel.purge(
        limit=messages + 1
    )  # the clear command counts as a message, so be sure to remove it too


@commands.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    """ban Bans a member from the server

    Args:
        ctx (context): Discord Context Object
        member (discord.Member): Member to be banned
        reason (string, optional): reason the member was banned. Defaults to None.
    """
    await member.ban(reason=reason)
    await ctx.send(f"User {member} has been banned")


@commands.command()
@commands.has_permissions(administrator=True)
async def unban(ctx, *, member):
    """unban Unban a user from the chat

    Args:
        ctx (context): Discord Context Object
        member (string): Member that is to be unbanned 
    """
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f"Unbanned {user.mention}")
            return


@commands.command()
@commands.has_permissions(administrator=True)
async def softban(ctx, member: discord.Member, *, reason=None):
    ban(ctx, member=member, reason=reason)
    unban(ctx, member=member.mention)


@commands.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    """kick Kick a member off the server

    Args:
        ctx (context): Discord Context Object
        member (discord.Member): The member that is to be kicked.
        reason (string, optional): Reason the user was kicked. Defaults to None.
    """
    await member.kick(reason=reason)
    await ctx.send(f"User {member} has been kicked")


token = os.environ.get("DISCORD_BOT_TOKEN")

bot.run(token)

