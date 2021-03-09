import discordPermissions

from discord.ext import commands

class botManagementClass(commands.Cog, name='Bot Management'):
    def __init__(self, discordClient):
        self.discordClient = discordClient;
    
    @commands.command(brief="Echos messages to the server console", description="Echos messages to the server console")
    async def serverEcho(self, ctx, arg):
        print("Server Echo message:\n{0}\n{1}".format(ctx, arg));

    @commands.command(brief="Halts the bots server process", description="Halts the bots server process")
    async def murderTheBot(self, ctx):
       message = "Bot killed by {0}(<@!{1}>)".format(ctx.author.name, ctx.author.id);
       print(message);
       await ctx.send(message);
       await self.discordClient.close();
       exit(0);
