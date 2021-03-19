import discord
from discord.ext import commands
import requests
import json
from mcstatus import MinecraftServer
from username_to_uuid import UsernameToUUID

with open('keys.json') as json_file:
    data = json.load(json_file)
    key = data["hypixel"]


class MinecraftCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("The Minecraft Cog is online")

    @commands.command(pass_context=True)
    async def hypixelstat(self, ctx, username):
        message = await ctx.send("Getting Hypixel info...")
        try:
            data = requests.get(f"https://api.hypixel.net/player?key={key}&name={username}").json()
            converter = UsernameToUUID(username)
            mcid = converter.get_uuid()
        except Exception:
            await ctx.send(":x: Invalid player")
            return

        try:
            try:
                karma = data["player"]["karma"]
            except Exception:
                karma = 0

            if "rank" in data["player"] and data["player"]["rank"] != "NORMAL":
                rank = data["player"]["rank"]
            elif "newPackageRank" in data["player"]:
                rank = data["player"]["newPackageRank"]
            elif "packageRank" in data["player"]:
                rank = data["player"]["packageRank"]
            else:
                rank = "Non-Donor"
            if rank == "VIP_PLUS":
                rank = "VIP+"
            if rank == "MVP_PLUS":
                rank = "MVP+"
            try:
                if data["player"]["monthlyPackageRank"] == "SUPERSTAR":
                    rank = "MVP++"
            except Exception:
                pass
            try:
                skywarswins = data["player"]["stats"]["SkyWars"]["wins"]
            except Exception:
                skywarswins = 0

            skywarsgames = data["player"]["stats"]["SkyWars"]["games_played_skywars"]
            try:
                bedwarswins = data["player"]["stats"]["Bedwars"]["wins_bedwars"]

            except Exception:
                bedwarswins = 0

            bedwarsgames = data["player"]["stats"]["Bedwars"]["games_played_bedwars"]
            embed = discord.Embed(title="Player Info", description="The Hypixel info about a certain player")
            embed.set_author(name=f"{username}'s Hypixel Info", icon_url=f"https://crafatar.com/avatars/{mcid}?overlay")
            embed.set_image(url=f"https://crafatar.com/renders/body/{mcid}?overlay")
            embed.add_field(name="Karma", value=f"**{username}** has **" + str("{:,}".format(karma)) + "** Karma.",
                            inline=False)
            embed.add_field(name="Bedwars", value=f"**{username}** has played **" + str(
                "{:,}".format(bedwarsgames)) + "** and won **" + str("{:,}".format(bedwarswins)) + "**",
                            inline=False)
            embed.add_field(name="Skywars", value=f"**{username}** has played **" + str(
                "{:,}".format(skywarsgames)) + "** and won **" + str("{:,}".format(skywarswins)) + "**",
                            inline=False)
            embed.add_field(name="Rank", value=f"**{username}** has **" + rank + "**",
                            inline=False)
            await message.delete()
            await ctx.send(embed=embed)
        except Exception:
            await message.delete()
            await ctx.send(":x: Invalid Player")

    @hypixelstat.error
    async def hypixelstat_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                ":x: You must specify a user E.G. **-hypixelstat WilliamD47**")
        elif isinstance(error, UnboundLocalError):
            await ctx.send(":x: Invalid Player")
        else:
            await ctx.send(f":x: An unknown error has occurred. The error was ```{error}```")
            raise error

    @commands.command(pass_context=True)
    async def playersonline(self, ctx):
        server = MinecraftServer.lookup("mc.williamd47.net:25565")
        status = server.status()
        await ctx.send(f"There are **{status.players.online}** members online right now.")

    @playersonline.error
    async def playersonline_error(self, ctx, error):
        await ctx.send(f"An unknown error has occurred. The error was ```{error}```")
        raise error


def setup(client):
    client.add_cog(MinecraftCog(client))
