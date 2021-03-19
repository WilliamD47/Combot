from discord.ext import commands
import discord

class FunCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def amogus(self, ctx):
        try:
            await ctx.message.delete()
            channel = ctx.author.voice.channel
            vc = await channel.connect()
            vc.play(discord.FFmpegPCMAudio("music/amongus.mp3"))
        except Exception:
            pass

    @commands.command()
    async def arab(self, ctx):
        try:
            await ctx.message.delete()
            channel = ctx.author.voice.channel
            vc = await channel.connect()
            vc.play(discord.FFmpegPCMAudio("music/arab.mp3"))
        except Exception:
            pass


    @amogus.error
    async def amoguserror(self, ctx, error):
        raise error


def setup(client):
    client.add_cog(FunCog(client))
