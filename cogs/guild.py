import discord
from discord.ext import commands


class GuildCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("The Guild Cog is online")
        print("\n------------------\n")
        print("All Cogs Loaded")
        print("\n------------------\n")
        print("All errors will be below:")

    @commands.command()
    @commands.guild_only()
    async def disconnect(self, ctx, member: discord.Member):
        if ctx.message.author.guild_permissions.administrator:
            await member.move_to(channel=None)
            await ctx.send(":white_check_mark: Disconnected " + member.display_name)
        else:
            await ctx.send(
                ":x: You do **NOT** have permissions to disconnect ``" + member.display_name + "`` (You need **Administrator** permission to do this command.)")

    @disconnect.error
    async def disconnect_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(":x: You must specify a member E.G. **-disconnect <@808072863353274438>**")
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send(":x: I do not have permission to do that!")
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send(":x: Invalid Member (if this is your first time running the command, please try it again. It may be bugged)")
        else:
            raise error

    @commands.command()
    @commands.guild_only()
    async def clear(self, ctx, amount: int):
        if ctx.message.author.guild_permissions.administrator or ctx.message.author.guild_permissions.manage_messages:
            if amount != 0 and not amount > 99:
                amount += 1
                await ctx.channel.purge(limit=amount)
                amount -= 1
                await ctx.channel.send(":white_check_mark: Cleared **" + str(amount) + "** messages!", delete_after=5)
            else:
                await ctx.channel.send(":x: You need to specify a number over 0 and less than 100", delete_after=5)
        else:
            await ctx.channel.send(":x: You do not have the permissions!", delete_after=5)

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(":x: You must specify a number E.G. **-clear <@808072863353274438>**")
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send(":x: I do not have permission to do that!")
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send(
                ":x: Invalid Member (if this is your first time running the command, please try it again. It may be bugged)")
        else:
            raise error

    @commands.command()
    @commands.guild_only()
    async def kick(self, ctx, userName: discord.Member, *, reason="No reason specified"):
        if ctx.message.author.guild_permissions.administrator:
            if not userName.bot:
                channel = await userName.create_dm()
                await channel.send(f"You were kicked from **{ctx.guild.name}** for *{reason}*")
            await userName.kick(reason=reason)
            await ctx.send(":mechanical_leg: Kicked **" + str(userName) + "** for " + reason, delete_after=5)
        else:
            await ctx.channel.send(":x: You do not have the permissions!", delete_after=5)

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f":x: You must specify a member E.G. -kick **<@808072863353274438>**")
        if isinstance(error, commands.BotMissingPermissions):
            await ctx.send(":x: I do not have permission to do that!")
        if isinstance(error, commands.MemberNotFound):
            await ctx.send(":x: Invalid Member (if this is your first time running the command, please try it again. It may be bugged)")

    @commands.command()
    @commands.guild_only()
    async def ban(self, ctx, userName: discord.Member, *, reason="No reason specified"):
        if ctx.message.author.guild_permissions.administrator:
            if not userName.bot:
                channel = await userName.create_dm()
                await channel.send(f"You were banned from **{ctx.guild.name}** for *{reason}*")
            await userName.ban(reason=reason)
            await ctx.send(":hammer: Banned **" + str(userName) + "** for " + reason, delete_after=5)

        else:
            await ctx.channel.send(":x: You do not have the permissions!", delete_after=5)

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(":x: You must specify a member E.G. **-ban <@808072863353274438>**")
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send(":x: I do not have permission to do that!")
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send(":x: Invalid Member (if this is your first time running the command, please try it again. It may be bugged)")
        else:
            raise error


def setup(client):
    client.add_cog(GuildCog(client))
