import discordUtils

from discord.ext import tasks
import pymysql.cursors

#ToDo:
#    mySql Table Init
#    Work for any # of guilds

class textLoggingClass:
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

    def __init__(self, discordClient, settingsMySql):
        print("textLoggingClass: Init Start");
        self.settingsMySql = settingsMySql;
        
        @discordClient.event
        async def on_message(message):
            #Normalize Quotes in messages. Some devices send wierd ones
            message.content = message.content.replace("“", "\"");
            message.content = message.content.replace("”", "\"");
            
            authorUserTag="{0}({1})".format(message.author.name, message.author.nick);
            
            attachmentUrls = discordUtils.getMessageAttachments(message);
            self.logMessage(message.author.id, authorUserTag, message.channel.id, message.channel.name, message.id, message.content, attachmentUrls);
            
            await discordClient.process_commands(message);
        print("textLoggingClass: Init Complete");

class voiceLoggingClass:
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
        print("voiceLoggingClass: Init Start");
        self.settingsMySql = settingsMySql;
        
        @discordClient.event
        async def on_voice_state_update(member, before, after):
            userNameAndNick = "{0}({1})".format(member.name, member.nick)
            
            self.updateVoiceChatLog(member.id)
            
            if after.channel is not None:
                self.insertVoiceChatLog(member.id, userNameAndNick, after.channel.id, after.channel.name)
            else:
                self.insertVoiceChatLog(member.id, userNameAndNick, None, "None")
        print("voiceLoggingClass: Init Complete");
