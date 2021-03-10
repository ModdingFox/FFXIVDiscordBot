from discord.ext import commands

class courtesanClass(commands.Cog, name='Courtesans'):
    def initTables(self):
        return True;
    
    def __init__(self, discordClient, settingsMySql):
        self.discordClient = discordClient;
        self.settingsMySql = settingsMySql;
        self.initTables();
    
    @commands.command(brief="Gets a list of all courtesans and their current avaliability", description="Gets a list of all courtesans and their current avaliability")
    async def courtesanList(self, ctx):
        await ctx.send("Not Implimented Yet");
    
    @commands.command(brief="Sets own courtesans status as avaliable", description="Sets own courtesans status as avaliable")
    async def courtesanSetAvaliable(self, ctx):
        await ctx.send("Not Implimented Yet");
    
    @commands.command(brief="Sets own courtesans status as unavaliable", description="Sets own courtesans status as unavaliable")
    async def courtesanSetUnavaliable(self, ctx):
        await ctx.send("Not Implimented Yet");
