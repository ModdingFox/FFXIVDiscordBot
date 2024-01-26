import discordUtils;
import sound;

from discord.ext import commands;

class audioUtilsClass(commands.Cog, name='Audio Utilities'):
    def __init__(self, discordClient):
        self.discordClient = discordClient;

    @commands.command(brief="Join audio channel", description="Join audio channel")
    async def joinChannel(self, ctx, deviceId, channelId):
        stream = sound.PCMStream();
        stream.change_device(int(deviceId));
        channel = await discordUtils.fetchChannelById(ctx.guild, channelId);
        voice_client = await channel.connect();
        voice_client.play(stream);       

    @commands.command(brief="Disconnect from audio channel", description="Disconnect from audio channel")
    async def disconnectChannel(self, ctx):
        await ctx.voice_client.disconnect();

    @commands.command(brief="List all sources", description="List all sources")
    async def listSources(self, ctx):
        await ctx.send(sound.query_devices());
