import discordUtils

from discord.ext import commands
from discord.ext import tasks
import pymysql.cursors

#ToDo:
#    Work for any # of guilds

class textLoggingClass(commands.Cog, name='Text Logging'):
    def logMessage(self, authorId, authorName, channelId, channelName, messageId, messageContent, attachmentUrls):
        result = False;
        
        connection = pymysql.connect(host = self.settingsMySql.host, user = self.settingsMySql.user, password = self.settingsMySql.password, cursorclass=pymysql.cursors.DictCursor);
        
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO discord.textChatLog (authorId, authorName, channelId, channelName, messageId, messageContent, attachmentUrls) VALUES (%s, %s, %s, %s, %s, %s, %s)";
                cursor.execute(sql, (authorId, authorName, channelId, channelName, messageId, messageContent, ", ".join(attachmentUrls)));
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
                cursor.execute("CREATE TABLE IF NOT EXISTS discord.textChatLog ( id               INT       NOT NULL AUTO_INCREMENT, messageTimestamp TIMESTAMP     NULL, authorId         TEXT      NOT NULL, authorName       TEXT      NOT NULL, channelId        TEXT      NOT NULL, channelName      TEXT      NOT NULL, messageContent   TEXT      NOT NULL, attachmentUrls   TEXT          NULL, PRIMARY KEY (id))");
                cursor.execute("DROP TRIGGER IF EXISTS discord.discord_textChatLog_timestamps");
                cursor.execute("CREATE TRIGGER discord.discord_textChatLog_timestamps BEFORE INSERT ON discord.textChatLog FOR EACH ROW SET NEW.messageTimestamp = IFNULL(NEW.messageTimestamp , NOW())");
                result = True;
        finally:
                connection.close();
        
        return result;
    
    def __init__(self, discordClient, settingsMySql):
        self.settingsMySql = settingsMySql;
        self.initTables();
        
        @discordClient.listen()
        async def on_message(message):
            #Normalize Quotes in messages. Some devices send wierd ones
            message.content = message.content.replace("“", "\"");
            message.content = message.content.replace("”", "\"");
            
            authorUserTag="{0}({1})".format(message.author.name, message.author.nick);
            
            attachmentUrls = discordUtils.getMessageAttachments(message);
            self.logMessage(message.author.id, authorUserTag, message.channel.id, message.channel.name, message.id, message.content, attachmentUrls);
