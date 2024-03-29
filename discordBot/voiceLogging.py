import discordUtils

from discord.ext import commands
from discord.ext import tasks
import pymysql.cursors

class voiceLoggingClass(commands.Cog, name='Voice Logging'):
    def insertVoiceChatLog(self, discordUserId, userName, guildId, channelId, channelName):
        result = False;
        
        connection = pymysql.connect(host = self.settingsMySql.host, user = self.settingsMySql.user, password = self.settingsMySql.password, cursorclass=pymysql.cursors.DictCursor);
        
        try:
            with connection.cursor() as cursor:
                if channelId is not None:
                    sql = "INSERT INTO discord.voiceChatLog (discordUserId, userName, guildId, channelId, channelName) VALUES (%s, %s, %s, %s, %s)";
                    cursor.execute(sql, (discordUserId, userName, guildId, channelId, channelName));
                else:
                    sql = "INSERT INTO discord.voiceChatLog (discordUserId, userName, guildId, channelName) VALUES (%s, %s, %s, %s)";
                    cursor.execute(sql, (discordUserId, userName, guildId, channelName));
                
                connection.commit();
                result = True;
        finally:
            connection.close();
        
        return result;
    
    def updateVoiceChatLog(self, discordId, guildId):
        result = False;
        
        connection = pymysql.connect(host = self.settingsMySql.host, user = self.settingsMySql.user, password = self.settingsMySql.password, cursorclass=pymysql.cursors.DictCursor);
        
        try:
            with connection.cursor() as cursor:
                sql = "UPDATE discord.voiceChatLog SET leaveChannelTimestamp = now() WHERE discordUserId = %s AND guildId = %s AND leaveChannelTimestamp is NULL";
                cursor.execute(sql, (discordId, guildId));
                connection.commit();
                result = True;
        finally:
            connection.close();
        
        return result;
    
    def initTables(self):
        result = False;
        
        connection = pymysql.connect(host = self.settingsMySql.host, user = self.settingsMySql.user, password = self.settingsMySql.password, cursorclass=pymysql.cursors.DictCursor);
        
        try:
            with connection.cursor() as cursor:
                cursor.execute("CREATE DATABASE IF NOT EXISTS discord COLLATE utf8mb4_unicode_ci");
                cursor.execute("CREATE TABLE IF NOT EXISTS discord.voiceChatLog ( id                    INT       NOT NULL AUTO_INCREMENT, discordUserId         TEXT      NOT NULL, userName              TEXT      NOT NULL, guildId               TEXT      NOT NULL, channelId             TEXT          NULL, channelName           TEXT      NOT NULL, joinChannelTimeStamp  TIMESTAMP     NULL, leaveChannelTimestamp TIMESTAMP     NULL, PRIMARY KEY (id) )");
                cursor.execute("DROP TRIGGER IF EXISTS discord.discord_voiceChatLog_dates");
                cursor.execute("CREATE TRIGGER discord.discord_voiceChatLog_dates BEFORE INSERT ON discord.voiceChatLog FOR EACH ROW SET     NEW.joinChannelTimeStamp      = IFNULL(NEW.joinChannelTimeStamp      , NOW())");
                result = True;
        finally:
                connection.close();
        
        return result;
    
    def __init__(self, discordClient, settingsMySql):
        self.settingsMySql = settingsMySql;
        self.initTables();
        
        @discordClient.listen()
        async def on_voice_state_update(member, before, after):
            userNameAndNick = "{0}({1})".format(member.name, member.nick);
            
            self.updateVoiceChatLog(member.id, member.guild.id);
            
            if after.channel is not None:
                self.insertVoiceChatLog(member.id, userNameAndNick, member.guild.id, after.channel.id, after.channel.name);
            else:
                self.insertVoiceChatLog(member.id, userNameAndNick, member.guild.id, None, "None");
