from discord.ext import commands
import discord


class UtilityCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("The Utility Cog is online")

    @commands.command()
    async def membercount(self, ctx):
        member_count = len(ctx.guild.members)
        await ctx.send(f"Member count is **{member_count}**")

    @commands.command()
    async def invite(self, ctx, member: discord.Member = None):
        if member == None:
            member = ctx.message.author
            channel = await member.create_dm()
            await channel.send(
                "Here is a link \n https://discord.com/oauth2/authorize?client_id=808072863353274438&scope=bot&permissions=805314622")
        else:
            channel = await member.create_dm()
            await channel.send(
                "Here is a link \n https://discord.com/oauth2/authorize?client_id=808072863353274438&scope=bot&permissions=805314622")

    @commands.command(pass_context=True)
    async def userinfo(self, ctx, username: discord.Member = 618349286614106122):
        try:
            embed = discord.Embed(title="User info", color=0xff0000)
            embed.set_thumbnail(url=username.avatar_url)
            join_time = username.joined_at.strftime("%b %d, %Y")
            embed.add_field(name="Username", value=str(username))
            embed.add_field(name="Display Name", value=username.display_name)
            embed.add_field(name="Main Role", value=f"This member has the role **{username.top_role}**")
            embed.add_field(name="Time Joined", value=f"This member joined on **{str(join_time)}**")
            if username.guild_permissions.manage_messages:
                is_staff = "This member **is** staff"
            else:
                is_staff = "This member **is not** staff"
            if username in ctx.message.guild.premium_subscribers:
                is_boost = f"This member has been boosting since " + username.premium_since.strftime("%b %d, %Y")
            else:
                is_boost = "This member **is not** boosting"
            embed.add_field(name="Are they boosting this server?", value=is_boost)
            roles = []
            for role in username.roles:
                roles.append(role.name)

            formattedroles = '[%s]' % ', '.join(map(str, roles))
            formatrole2 = formattedroles.replace('[', '')
            formatrole3 = formatrole2.replace(']', '')
            embed.add_field(name="What roles do they have?", value=formatrole3)
            embed.add_field(name="What is their ID?", value="**" + str(username.id) + "**")
            embed.add_field(name="Are they staff?", value=is_staff)
            created_at = username.created_at.strftime("%b %d, %Y")
            embed.add_field(name="Joined Discord", value=f"This member's Discord was created on **{str(created_at)}**")
            await ctx.send(embed=embed)
        except UnboundLocalError:
            await ctx.send(":x: Invalid Player")

    @userinfo.error
    async def user_info_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                ":x: Invalid usage. Please do **-userinfo username** and replace username with the username of who you want to see info about.")
        if isinstance(error, commands.UserNotFound):
            await ctx.send(":x: Invalid Username")
        if isinstance(error, commands.MemberNotFound):
            await ctx.send(":x: Invalid Username")
        else:
            await ctx.send(f":x: An unknown error has occurred. The error was ```{error}```")
            raise error


def setup(client):
    client.add_cog(UtilityCog(client))
