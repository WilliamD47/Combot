import discord
from discord.ext import commands
import os
import json


intents = discord.Intents.default()
intents.members = True
client = commands.Bot(intents=intents, command_prefix=["-", "cb."])
client.remove_command("help")
with open('keys.json') as json_file:
    data = json.load(json_file)
    key = data["discord"]


@client.event
async def on_ready():
    print("Bot running with:")
    print("Username: ", client.user.name)
    print("User ID: ", client.user.id)
    print("\n------------------\n")
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="-help"))

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")


@client.command()
async def help(ctx, page=None):
    if page is None:
        embed = discord.Embed(title="Help",
                              color=0xff0000)
        embed.set_author(name="Combot")
        embed.add_field(name="Guild/Server", value="Do -help guild",
                        inline=True)
        embed.add_field(name="YouTube", value="Do -help youtube",
                        inline=True)
        embed.add_field(name="Minecraft", value="do -help minecraft",
                        inline=True)
        embed.add_field(name="Utility", value="do -help utility", inline=True)
        await ctx.send(embed=embed)

    elif page == "guild":
        embed = discord.Embed(title="Guild Help",
                              description="Gives you help for guild commands such as -ban and -kick.",
                              color=0xff0000)
        embed.set_author(name="Combot")
        embed.add_field(name="-ban member", value="Bans a specified member",
                        inline=True)
        embed.add_field(name="-kick member", value="Kicks a specified member",
                        inline=True)
        embed.add_field(name="-disconnect member", value="Disconnects a specified member",
                        inline=True)
        embed.add_field(name="-clear number", value="Clears a certain number of messages",
                        inline=True)
        await ctx.send(embed=embed)

    elif page == "youtube":
        embed = discord.Embed(title="YouTube Help",
                              description="Gives you help for YouTube commands such as -youtubsearch and -getsubs.",
                              color=0xff0000)
        embed.set_author(name="Combot")
        embed.add_field(name="-getsubs channel-link", value="Gets the Subscriber count of a user",
                        inline=True)
        embed.add_field(name="-youtubesearch searchterm", value="Searches YouTube for a video",
                        inline=True)
        embed.add_field(name="-multisearch searchterm", value="Searches YouTube and gives multiple results",
                        inline=True)
        embed.add_field(name="-videoinfo video-link", value="Gives the info about a YouTube video",
                        inline=True)
        await ctx.send(embed=embed)

    elif page == "minecraft":
        embed = discord.Embed(title="Minecraft Help",
                              description="Gives you help for Minecraft commands such as -playersonline and -hypixelinfo.",
                              color=0xff0000)
        embed.set_author(name="Combot")
        embed.add_field(name="-playersonline serverip:serverport",
                        value="Shows the players online on a specific server and port",
                        inline=True)
        embed.add_field(name="-hypixelstat username", value="Shows the Hypixel Info for a player",
                        inline=True)
        await ctx.send(embed=embed)

    elif page == "utility":
        embed = discord.Embed(title="Utility Help",
                              description="Gives you help for Utility commands such as -joinmessage",
                              color=0xff0000)
        embed.set_author(name="Combot")
        embed.add_field(name="-joinmessage #Channel",
                        value="Sets the channel that the join message will send to.",
                        inline=True)
        embed.add_field(name="-joinrole @Role",
                        value="Sets the role that new members will get.",
                        inline=True)
        embed.add_field(name="-userinfo @User", value="Gives info about a certain user")
        await ctx.send(embed=embed)
    else:
        await ctx.send("Invalid page. Do **-help** for a list of pages.")


@client.command()
async def about(ctx):
    embed = discord.Embed(title="About", description="About this very bot!", color=0xff0000)
    embed.set_author(name="Combot")
    embed.add_field(name="Made by", value="WilliamD47", inline=True)
    embed.add_field(name="Version", value="0.1.2", inline=True)
    embed.add_field(name="Source code", value="Coming soon!", inline=True)
    embed.add_field(name="Servers", value=f"I am in {len(client.guilds)} Server(s)", inline=True)
    await ctx.send(embed=embed)


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        pass


@client.command()
async def joinmessage(ctx, channelid: discord.TextChannel):
    name = "guild_data/" + str(ctx.guild.id) + ".txt"
    f = open(name, "w")
    f.write(str(channelid.id))
    await ctx.send(f"Join message set to **#{channelid}**!")


@client.command()
async def joinrole(ctx, role):
    name = "guild_role_data/" + str(ctx.guild.id) + ".txt"
    f = open(name, "w")
    f.write(str(role))

    await ctx.send(f"Join role set to **{role}**!")


@joinrole.error
async def joinroleerror(ctx, error):
    raise error


@client.event
async def on_member_join(member):
    if os.path.exists(f"guild_data/{str(member.guild.id)}.txt"):
        f = open(f"guild_data/{str(member.guild.id)}.txt", "r")
        channel = client.get_channel(int(f.read()))
        embed = discord.Embed(title="Welcome " + str(member), color=0xff0000)
        embed.set_author(name="Welcome", icon_url=member.avatar_url)
        embed.set_footer(text="Welcome to the server!")
        await channel.send(embed=embed)
    if os.path.exists(f"guild_role_data/{str(member.guild.id)}.txt"):
        f = open(f"guild_role_data/{str(member.guild.id)}.txt", "r")
        id = int(f.read())
        role = member.guild.get_role(role_id=id)
        await member.add_roles(role)


@joinmessage.error
async def joinmessageerror(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(":x: You need to specify a channel E.G **-joinmessage #Welcome**")
    elif isinstance(error, commands.ChannelNotFound):
        await ctx.send(":x: Invalid Channel. E.G **-joinmessage #Welcome**")
    else:
        await ctx.send(f":x: An unknown error has occurred. The error was ```{error}```")
        raise error

client.run(key)
