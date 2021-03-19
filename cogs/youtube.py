import discord
from discord.ext import commands
import requests
import json
from youtube_search import YoutubeSearch
import urllib.request
import urllib.parse as urlparse

with open('keys.json') as json_file:
    data = json.load(json_file)
    key = data["youtube"]


class YouTubeCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("The YouTube Cog is online")

    @commands.command()
    async def getsubs(self, ctx, channelink):
        try:
            ytId = channelink.rsplit('/', 1)[1]
        except Exception:
            await ctx.send("Invalid YouTube URL")
        try:
            data = urllib.request.urlopen(
                "https://www.googleapis.com/youtube/v3/channels?part=statistics&id=" + ytId + "&fields=items/statistics/subscriberCount&key=" + key).read()
            subs = json.loads(data)["items"][0]["statistics"]["subscriberCount"]
            await ctx.send(":white_check_mark: That person has " + str("{:,}".format(int(subs))) + " Subscribers")
        except Exception:
            await ctx.send(
                "Invalid YouTube URL. Do NOT input a custom URL. You must input the URL with the long random string afterwards.")

    @getsubs.error
    async def getsubs_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                ":x: You must specify a Channel Link E.G. **-getsubs https://www.youtube.com/channel/UCgx3cwTPCFWEe7GAe_X8-1Q**")
        else:
            ctx.send(f":x: An unknown error has occurred. The error was ```{error}```")

    @commands.is_nsfw()
    @commands.command(pass_context=True)
    async def videoinfo(self, ctx, videoid="https://www.youtube.com/watch?v=M-yuW_gifxg"):
        try:
            url_data = urlparse.urlparse(videoid)
            query = urlparse.parse_qs(url_data.query)
            video = query["v"][0]
            data = requests.get(
                f"https://www.googleapis.com/youtube/v3/videos?part=contentDetails,statistics&id={video}&key={key}").json()
            views = data["items"][0]["statistics"]["viewCount"]
            likes = data["items"][0]["statistics"]["likeCount"]
            dislikes = data["items"][0]["statistics"]["dislikeCount"]
            comments = data["items"][0]["statistics"]["commentCount"]
            embed = discord.Embed(title="Video info", description="Shows the info about a video", color=0xff0000)
            embed.add_field(name="Likes", value="This video has **" + "{:,}".format(int(likes)) + "** likes",
                            inline=True)
            embed.add_field(name="Dislikes", value="This video has **" + "{:,}".format(int(dislikes)) + "** dislikes",
                            inline=True)
            embed.add_field(name="Views", value="This video has **" + "{:,}".format(int(views)) + "** views",
                            inline=True)
            embed.add_field(name="Comments", value="This video has **" + "{:,}".format(int(comments)) + "** comments",
                            inline=True)
            await ctx.send(embed=embed)
        except Exception:
            await ctx.send(":x: Invalid YouTube link")

    @videoinfo.error
    async def videoinfo_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                ":x: You must specify a search E.G. **-videoinfo https://www.youtube.com/watch?v=M-yuW_gifxg**")
        elif isinstance(error, commands.NSFWChannelRequired):
            await ctx.send(":x: This has to be used in a NSFW channel")
        else:
            ctx.send(f":x: An unknown error has occurred. The error was ```{error}```")

    @commands.guild_only()
    @commands.is_nsfw()
    @commands.command(pass_context=True, aliases=["ytsearch", "yts"])
    async def youtubesearch(self, ctx, *, searchterm):
        try:
            apikey = key
            results = YoutubeSearch(searchterm, max_results=10).to_json()
            thingy = json.loads(results)["videos"][0]["id"]
            thumbnail = json.loads(results)["videos"][0]["thumbnails"][0]
            link = f"https://www.youtube.com/watch?v={thingy}"
            data = requests.get(
                f"https://www.googleapis.com/youtube/v3/videos?part=contentDetails,statistics&id={thingy}&key={apikey}").json()
            try:
                views = data["items"][0]["statistics"]["viewCount"]
            except Exception:
                views = 0

            try:
                likes = data["items"][0]["statistics"]["likeCount"]
            except Exception:
                likes = 0
            try:
                dislikes = data["items"][0]["statistics"]["dislikeCount"]
            except Exception:
                dislikes = 0
            descriptiondata = requests.get(
                f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={thingy}&key={apikey}").json()
            try:
                description = descriptiondata["items"][0]["snippet"]["description"]
                if len(description) > 1500:
                    description = "Description is too long to display"
            except Exception:
                description = "No Description"
            title = descriptiondata["items"][0]["snippet"]["title"]
            embed = discord.Embed(title=title, url=link, description=description, color=0xff0000)
            embed.set_thumbnail(url=thumbnail)
            embed.add_field(name="Stats",
                            value=f"This video ({title}) has **" + str(f"{int(views):,}") + "** views, **" + str(
                                f"{int(likes):,}") + "** likes and **" + str(f"{int(dislikes):,}") + "** dislikes")
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send("An error occurred `" + str(e) + "`")

    @youtubesearch.error
    async def youtubesearch_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.send(":x: This command can only be used in a server")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                ":x: You must specify a search E.G. **-youtubesearch WilliamD47 PVPRush**")
        elif isinstance(error, commands.NSFWChannelRequired):
            await ctx.send(":x: This has to be used in a NSFW channel")
        else:
            ctx.send(f":x: An unknown error has occurred. The error was ```{error}```")

    @commands.guild_only()
    @commands.is_nsfw()
    @commands.command(pass_context=True, aliases=["ls", "longsearch", "ms", "multis"])
    async def multisearch(self, ctx, *, searchterm):
        apikey = key
        results = YoutubeSearch(searchterm, max_results=10).to_json()
        thumbnail = json.loads(results)["videos"][0]["thumbnails"][0]
        embed = discord.Embed(title="Search Results", color=0xff0000)
        embed.set_thumbnail(url=thumbnail)
        amounttoreturn = 6
        i = 0
        while i != amounttoreturn:
            id = json.loads(results)["videos"][i]["id"]
            link = f"https://www.youtube.com/watch?v={id}"
            data = requests.get(
                f"https://www.googleapis.com/youtube/v3/videos?part=contentDetails,statistics&id={id}&key={apikey}").json()
            try:
                views = data["items"][0]["statistics"]["viewCount"]
            except Exception:
                views = 0

            try:
                likes = data["items"][0]["statistics"]["likeCount"]
            except Exception:
                likes = 0
            try:
                dislikes = data["items"][0]["statistics"]["dislikeCount"]
            except Exception:
                dislikes = 0
            descriptiondata = requests.get(
                f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={id}&key={apikey}").json()
            title = descriptiondata["items"][0]["snippet"]["title"]
            embed.add_field(name=title, value=str(f"{int(views):,}") + " views :thumbsup: " + str(
                f"{int(likes):,}") + " :thumbsdown: " + str(f"{int(dislikes):,}") + f" [Watch]({link})", inline=False)
            embed.set_footer(text="SafeSearch was enabled on the i")
            i += 1
        await ctx.send(embed=embed)

    @multisearch.error
    async def multisearch_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.send(":x: This command can only be used in a server")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                ":x: You must specify a search E.G. **-multisearch WilliamD47**")
        elif isinstance(error, commands.NSFWChannelRequired):
            await ctx.send(":x: This has to be used in a NSFW channel")
        else:
            await ctx.send(f":x: An unknown error has occurred. The error was ```{error}```")
            raise error


def setup(client):
    client.add_cog(YouTubeCog(client))
