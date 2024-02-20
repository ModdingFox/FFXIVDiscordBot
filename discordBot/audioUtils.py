import discordUtils;
import re;
import sound;
import vlc;
import youtube_dl

from discord.ext import commands;

ydl_opts = {
    'format': 'bestaudio',
};

class audioUtilsClass(commands.Cog, name='Audio Utilities'):
    def setupFreshPlayer(self):
        self.instance = vlc.Instance('--novideo');
        self.media_list = self.instance.media_list_new();
        self.media_list_player = self.instance.media_list_player_new();
        self.media_player = self.instance.media_player_new();
        
        self.media_list_player.set_media_player(self.media_player);
        self.media_list_player.set_media_list(self.media_list);

    def __init__(self, discordClient):
        self.discordClient = discordClient;
        self.setupFreshPlayer();

    @commands.command(brief="", description="")
    async def add(self, ctx, url):
        youtubeLinkRegex='^http(?:s?):\/\/(?:www\.|music\.)?youtu(?:be\.com\/watch\?v=|\.be\/)([\w\-\_]*)(&(amp;)?‌​[\w\?‌​=]*)?';
        match = re.search(youtubeLinkRegex, url);
        if match is None:
            await ctx.send('Provided link is not valid');
        else:
            ydl = youtube_dl.YoutubeDL(ydl_opts);
            info = ydl.extract_info(url, download=False);
            self.media_list.add_media(info['formats'][0]['url']);
            await ctx.send("Added song to play list");

    @commands.command(brief="", description="")
    async def clear(self, ctx):
        await self.pause(ctx);
        self.setupFreshPlayer();

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

    @commands.command(brief="", description="")
    async def goTo(self, ctx, index):
        self.media_list_player.play_item_at_index(int(index));

    @commands.command(brief="List all sources", description="List all sources")
    async def listSources(self, ctx):
        await ctx.send(sound.query_devices());

    @commands.command(brief="", description="")
    async def next(self, ctx):
        self.media_list_player.next();

    @commands.command(brief="", description="")
    async def pause(self, ctx):
        self.media_list_player.pause();

    @commands.command(brief="", description="")
    async def play(self, ctx):
        self.media_list_player.play();

    @commands.command(brief="", description="")
    async def previous(self, ctx):
        self.media_list_player.previous();

    @commands.command(brief="", description="")
    async def repeatOff(self, ctx):
        self.media_list_player.set_playback_mode(vlc.PlaybackMode.default);

    @commands.command(brief="", description="")
    async def repeatPlaylist(self, ctx):
        self.media_list_player.set_playback_mode(vlc.PlaybackMode.loop);

    @commands.command(brief="", description="")
    async def repeatSong(self, ctx):
        self.media_list_player.set_playback_mode(vlc.PlaybackMode.repeat);

