import discordUtils

from discord.ext import commands
from discord.ext import tasks
import pymysql.cursors

#ToDo:
#    mySql Table Init
#    Work for any # of guilds

class voiceLoggingClass(commands.Cog, name='Voice Logging'):
    def insertVoiceChatLog(self, discordUserId, userName, channelId, channelName):
        result = False;
        
        connection = pymysql.connect(host = self.settingsMySql.host, user = self.settingsMySql.user, password = self.settingsMySql.password, cursorclass=pymysql.cursors.DictCursor);
        
        try:
            with connection.cursor() as cursor:
                if channelId is not None:
                    sql = "INSERT INTO discord.voiceChatLog (discordUserId, userName, channelId, channelName) VALUES (%s, %s, %s, %s)";
                    cursor.execute(sql, (discordUserId, userName, channelId, channelName));
                else:
                    sql = "INSERT INTO discord.voiceChatLog (discordUserId, userName, channelName) VALUES (%s, %s, %s)";
                    cursor.execute(sql, (discordUserId, userName, channelName));
                
                connection.commit();
                result = True;
        finally:
            connection.close();
        
        return result;
    
    def updateVoiceChatLog(self, discordId):
        result = False;
        
        connection = pymysql.connect(host = self.settingsMySql.host, user = self.settingsMySql.user, password = self.settingsMySql.password, cursorclass=pymysql.cursors.DictCursor);
        
        try:
            with connection.cursor() as cursor:
                sql = "UPDATE discord.voiceChatLog SET leaveChannelTimestamp = now() WHERE discordUserId = %s AND leaveChannelTimestamp is NULL";
                cursor.execute(sql, (discordId));
                connection.commit();
                result = True;
        finally:
            connection.close();
        
        return result;
    
    def __init__(self, discordClient, settingsMySql):
        self.settingsMySql = settingsMySql;
        
        @discordClient.listen()
        async def on_voice_state_update(member, before, after):
            userNameAndNick = "{0}({1})".format(member.name, member.nick)
            
            self.updateVoiceChatLog(member.id)
            
            if after.channel is not None:
                self.insertVoiceChatLog(member.id, userNameAndNick, after.channel.id, after.channel.name)
            else:
                self.insertVoiceChatLog(member.id, userNameAndNick, None, "None")
