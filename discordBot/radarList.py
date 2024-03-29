import discordUtils

import discord
from discord.ext import commands
from discord.ext import tasks
import pymysql.cursors
import re
from random import seed
from random import randint
import time
from kazoo.client import KazooClient

class radarListClass(commands.Cog, name='Radar Plugin'):
    def zkGetInRangeUsers(self):
        result = [];
        zookeeper = KazooClient(hosts='127.0.0.1:2181');
        zookeeper.start();
        children = zookeeper.get_children("/radar/players");
        for childName in children:
            result.append(childName);
        zookeeper.stop();
        return result;
    
    def sqlGetChannelRadarMessageIds(self, guildId, channelId):
        result = [];
        
        connection = pymysql.connect(host = self.settingsMySql.host, user = self.settingsMySql.user, password = self.settingsMySql.password, cursorclass=pymysql.cursors.DictCursor);
        
        try:
            with connection.cursor() as cursor:
                sql = "SELECT messageId FROM discord.radarMessages WHERE guildId = %s AND channelId = %s";
                cursor.execute(sql, (guildId, channelId));
                results = cursor.fetchall();
                for queryResult in results:
                    result.append(queryResult["messageId"]);
        finally:
            connection.close();
        
        return result;
    
    def sqlDeleteChannelRadarMessageIds(self, guildId, channelId, messageId):
        result = False;
        
        connection = pymysql.connect(host = self.settingsMySql.host, user = self.settingsMySql.user, password = self.settingsMySql.password, cursorclass=pymysql.cursors.DictCursor);
        
        try:
            with connection.cursor() as cursor:
                sql = "DELETE FROM discord.radarMessages WHERE guildId = %s AND channelId = %s AND messageId = %s";
                cursor.execute(sql, (guildId, channelId, messageId));
                connection.commit();
                result = True;
        finally:
            connection.close();
        
        return result;
    
    def sqlSetChannelRadarMessageId(self, guildId, channelId, messageId):
        result = False;
        
        connection = pymysql.connect(host = self.settingsMySql.host, user = self.settingsMySql.user, password = self.settingsMySql.password, cursorclass=pymysql.cursors.DictCursor);
        
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO discord.radarMessages (guildId, channelId, messageId) VALUES (%s, %s, %s)";
                cursor.execute(sql, (guildId, channelId, messageId));
                connection.commit();
                result = True;
        finally:
            connection.close();
        
        return result;
    
    async def updateGuildRadarChannels(self, guild):
        users = self.zkGetInRangeUsers();
        messages = [];
        currentMessage = "";
        messages.append("We currently have {0} players in the club".format(len(users)));
        for user in users:
            currentMessage += user + "\n";
            if len(currentMessage) > 1500:
                messages.append(currentMessage);
                currentMessage = "";
        if len(currentMessage) > 0:
             messages.append(currentMessage);
        for channelId in discordUtils.getChannelIdsByName(guild, "radar"):
            channel = await discordUtils.fetchChannelById(guild, channelId);
            for messageId in self.sqlGetChannelRadarMessageIds(guild.id, channelId):
                targetMessage = await channel.fetch_message(int(messageId));
                await targetMessage.delete();
                self.sqlDeleteChannelRadarMessageIds(guild.id, channelId, messageId);
            for message in messages:
                sentMessage = await channel.send(message);
                self.sqlSetChannelRadarMessageId(guild.id, channelId, sentMessage.id);
    
    def initTables(self):
        result = False;
        
        connection = pymysql.connect(host = self.settingsMySql.host, user = self.settingsMySql.user, password = self.settingsMySql.password, cursorclass=pymysql.cursors.DictCursor);
        
        try:
            with connection.cursor() as cursor:
                cursor.execute("CREATE DATABASE IF NOT EXISTS discord COLLATE utf8mb4_unicode_ci");
                cursor.execute("CREATE TABLE IF NOT EXISTS discord.radarMessages ( guildId       TEXT NOT NULL, channelId     TEXT NOT NULL, messageId     TEXT NOT NULL )");
                result = True;
        finally:
                connection.close();
        
        return result;
    
    @tasks.loop(minutes=5)
    async def updateRadarTask(self):
        for guild in self.discordClient.guilds:
            await self.updateGuildRadarChannels(guild);
    
    def __init__(self, discordClient, settingsMySql):
        self.discordClient = discordClient;
        self.settingsMySql = settingsMySql;
        self.initTables();
        self.updateRadarTask.start();
    
    @commands.command(brief="Triggers an update to the radar channels", description="Triggers an update to the radar channels")
    async def updateRadarChannels(self, ctx):
        await self.updateGuildRadarChannels(ctx.guild);

    @commands.command(brief="Randomly selects someone from the radar list", description="Randomly selects someone from the radar list")
    async def randomPlayerFromRadar(self, ctx):
        players = self.zkGetInRangeUsers();
        if len(players) == 0:
            await ctx.send("No players in radar to select from");
        else:
            seed(time.time());
            selectedPlayer = randint(0, len(players) - 1);
            await ctx.send("{0} was selected.".format(players[selectedPlayer]));
