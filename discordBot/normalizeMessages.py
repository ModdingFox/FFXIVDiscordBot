from discord.ext import commands

class normalizeMessagesClass(commands.Cog, name='Message Normalization'):
    def __init__(self, discordClient):
        self.discordClient = discordClient;
        
        @discordClient.event
        async def on_message(message):
            if message.content is not None:
                message.content = message.content.replace("“", "\"");
                message.content = message.content.replace("”", "\"");
                message.content = message.content.replace("’", "'");
            await discordClient.process_commands(message);
