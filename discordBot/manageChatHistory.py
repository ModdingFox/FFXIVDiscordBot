import discordUtils

import discord
from discord.ext import commands
from discord.ext import tasks
import pymysql.cursors
from datetime import datetime, timedelta
import re

class manageChatHistoryClass(commands.Cog, name='Manage Chat History'):
    def initTables(self):
        result = False;
        
        connection = pymysql.connect(host = self.settingsMySql.host, user = self.settingsMySql.user, password = self.settingsMySql.password, cursorclass=pymysql.cursors.DictCursor);
        
        try:
            with connection.cursor() as cursor:
                cursor.execute("CREATE DATABASE IF NOT EXISTS discord COLLATE utf8mb4_unicode_ci");
                cursor.execute("CREATE TABLE IF NOT EXISTS discord.chatHistoryRules ( guildId           TEXT NOT NULL, channelId         TEXT NOT NULL, retentionMinutes INT NOT NULL )");
                result = True;
        finally:
                connection.close();
        
        return result;

    def sqlGetChannelsWithRetention(self, guildId):
        result = [];
        
        connection = pymysql.connect(host = self.settingsMySql.host, user = self.settingsMySql.user, password = self.settingsMySql.password, cursorclass=pymysql.cursors.DictCursor);
        
        try:
            with connection.cursor() as cursor:
                sql = "SELECT channelId FROM discord.chatHistoryRules WHERE guildId = %s";
                cursor.execute(sql, (guildId));
                results = cursor.fetchall();
                for queryResult in results:
                    result.append(queryResult);
        finally:
            connection.close();
        
        return result;

    def sqlGetChannelRetention(self, guildId, channelId):
        result = None;
        
        connection = pymysql.connect(host = self.settingsMySql.host, user = self.settingsMySql.user, password = self.settingsMySql.password, cursorclass=pymysql.cursors.DictCursor);
        
        try:
            with connection.cursor() as cursor:
                sql = "SELECT retentionMinutes FROM discord.chatHistoryRules WHERE guildId = %s AND channelId = %s";
                cursor.execute(sql, (guildId, channelId));
                results = cursor.fetchall();
                for queryResult in results:
                    result = queryResult;
        finally:
            connection.close();
        
        return result;

    def sqlSetChannelRetention(self, guildId, channelId, retentionMinutes):
        result = False;
        
        currentChannelRetention = self.sqlGetChannelRetention(guildId, channelId);
        
        connection = pymysql.connect(host = self.settingsMySql.host, user = self.settingsMySql.user, password = self.settingsMySql.password, cursorclass=pymysql.cursors.DictCursor);
        
        try:
            with connection.cursor() as cursor:
                if currentChannelRetention is None:
                    sql = "INSERT INTO discord.chatHistoryRules (guildId, channelId, retentionMinutes) VALUES (%s, %s, %s)";
                    cursor.execute(sql, (guildId, channelId, retentionMinutes));
                    connection.commit();
                else:
                    sql = "UPDATE discord.chatHistoryRules SET retentionMinutes = %s WHERE guildId = %s AND channelId = %s";
                    cursor.execute(sql, (retentionMinutes, guildId, channelId));
                    connection.commit();
                result = True;
        finally:
            connection.close();
        
        return result;

    def sqlDeleteChannelRetention(self, guildId, channelId):
        result = False;
        
        connection = pymysql.connect(host = self.settingsMySql.host, user = self.settingsMySql.user, password = self.settingsMySql.password, cursorclass=pymysql.cursors.DictCursor);
        
        try:
            with connection.cursor() as cursor:
                sql = "DELETE FROM discord.chatHistoryRules WHERE guildId = %s AND channelId = %s";
                cursor.execute(sql, (guildId, channelId));
                connection.commit();
                result = True;
        finally:
            connection.close();
        
        return result;

    async def updateChannel(self, guild, channelId):
        channelRetention = self.sqlGetChannelRetention(guild.id, channelId);
        if channelRetention is not None and channelRetention["retentionMinutes"] is not None:
            retentionMinutes = channelRetention["retentionMinutes"];
            minMessageDateTime = datetime.utcnow() - timedelta(days=14);
            maxMessageDateTime = datetime.utcnow() - timedelta(minutes=retentionMinutes);
            channel = await discordUtils.fetchChannelById(guild, channelId);
            if channel is not None:
                messages = [ message async for message in channel.history(after=minMessageDateTime, before=maxMessageDateTime, limit=100, oldest_first=True)];
                if len(messages) > 0:
                    try:
                        await channel.delete_messages(messages);
                        return len(messages);
                    except ClientException:
                        print("Somehow tried to delete to many messages");
                    except Forbidden:
                        print("Bot doesnt have permission to delete messages in <#{0}>".format(channelId));
                    except NotFound:
                        print("Message deleted before bot could delete it");
                    except HTTPException:
                        print("Delete message failed");
            else:
                print("Could not find channelId {0}".format(channelId));
        return 0;

    async def updateChannels(self, guild):
        channelsWithRetention = self.sqlGetChannelsWithRetention(guild.id);
        clearedMessages = 0;
        for channelWithRetention in channelsWithRetention:
          clearedMessages += await self.updateChannel(guild, channelWithRetention["channelId"]);
        return clearedMessages;
    
    @tasks.loop(minutes=5)
    async def updateChannelsTask(self):
        for guild in self.discordClient.guilds:
            await self.updateChannels(guild);
    
    def __init__(self, discordClient, settingsMySql):
        self.discordClient = discordClient;
        self.settingsMySql = settingsMySql;
        self.initTables();
        self.updateChannelsTask.start();

    async def channelExtract(self, ctx, channel):
        channelMatch = re.search("\<\#(\d+)\>", channel);
        if channelMatch is not None:
            return channelMatch.group(1);           
        else:
            await ctx.send("{0} is not valid".format(channel));
            return None;

    @commands.command(brief="Sets channel message expiration in minutes", description="Sets channel message expiration in minutes")
    async def setMessageExpiration(self, ctx, channel, retentionMinutes):
        if re.match("^(\d+)$", retentionMinutes) is None:
            await ctx.send("Expiration must be a number");
        elif int(retentionMinutes) < 5:
            await ctx.send("Expiration must be greater than 5 minutes");
        elif int(retentionMinutes) > 20160:
            await ctx.send("Expiration must be less than 20160 minutes");
        else:
            channelId = await self.channelExtract(ctx, channel);
            if channelId is not None:
                result = self.sqlSetChannelRetention(ctx.guild.id, channelId, retentionMinutes);
                if result == True:
                    await ctx.send("Set message expiration for {0} to {1} minute(s)".format(channel, retentionMinutes));
                else:
                    await ctx.send("Failed to set message expiration for {0} to {1} minute(s)".format(channel, retentionMinutes));

    @commands.command(brief="Sets channel message expiration in minutes", description="Gets channel message expiration in minutes")
    async def getMessageExpiration(self, ctx, channel):
        channelId = await self.channelExtract(ctx, channel);
        if channelId is not None:
            result = self.sqlGetChannelRetention(ctx.guild.id, channelId);
            if result is None:
                await ctx.send("Message expiration for {0} is not currently set".format(channel));
            else:
                await ctx.send("Message expiration for {0} is {1} minute(s)".format(channel, result["retentionMinutes"]));

    @commands.command(brief="Deletes a channels message expiration", description="Deletes a channels message expiration")
    async def deleteMessageExpiration(self, ctx, channel):
        channelId = await self.channelExtract(ctx, channel);
        if channelId is not None:
            result = self.sqlDeleteChannelRetention(ctx.guild.id, channelId);
            if result == True:
                await ctx.send("Deleted message expiration for {0}".format(channel));
            else:
                await ctx.send("Failed to delete message expiration for {0}".format(channel));

    @commands.command(brief="Run channel message expiration cleanup", description="Run channel message expiration cleanup. Only removes 100 messages at a time.")
    async def runMessageCleanup(self, ctx):
        await ctx.send("Running message cleanup this may take sometime");
        result = await self.updateChannels(ctx.guild);
        await ctx.send("Removed {0} messages".format(result));

    @commands.command(brief="Run channel message expiration cleanup", description="Run channel message expiration cleanup. Only removes 100 messages at a time.")
    async def runChannelMessageCleanup(self, ctx, channel):
        channelId = await self.channelExtract(ctx, channel);
        if channelId is not None:
            result = await self.updateChannel(ctx.guild, channelId);
            await ctx.send("Removed {0} messages from {1}".format(result, channel));
