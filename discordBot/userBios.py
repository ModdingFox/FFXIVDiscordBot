import discordUtils

import discord
from discord.ext import commands
from discord.ext import tasks
import pymysql.cursors
import re

#ToDo:
#    mySql Table Init

class userBiosClass(commands.Cog, name='Bios'):
    def sqlGetBio(self, guildId, discordUserId):
        result = None;
        
        connection = pymysql.connect(host = self.settingsMySql.host, user = self.settingsMySql.user, password = self.settingsMySql.password, cursorclass=pymysql.cursors.DictCursor);
        
        try:
            with connection.cursor() as cursor:
                sql = "SELECT guildId, bioName, bioImage, bioText FROM discord.bios WHERE guildId = %s AND discordUserId = %s";
                cursor.execute(sql, (guildId, discordUserId));
                results = cursor.fetchall();
                for queryResult in results:
                    result = queryResult;
        finally:
            connection.close();
        
        return result;
    
    def sqlGetBioMessageId(self, guildId, discordUserId, channelId):
        result = None;
        
        connection = pymysql.connect(host = self.settingsMySql.host, user = self.settingsMySql.user, password = self.settingsMySql.password, cursorclass=pymysql.cursors.DictCursor);
        
        try:
            with connection.cursor() as cursor:
                sql = "SELECT messageId FROM discord.biosMessages WHERE guildId = %s AND discordUserId = %s AND channelId = %s";
                cursor.execute(sql, (guildId, discordUserId, channelId));
                results = cursor.fetchall();
                for queryResult in results:
                    result = queryResult["messageId"];
        finally:
            connection.close();
        
        return result;
    
    def sqlGetChannelBioMessageIds(self, guildId, channelId):
        result = [];
        
        connection = pymysql.connect(host = self.settingsMySql.host, user = self.settingsMySql.user, password = self.settingsMySql.password, cursorclass=pymysql.cursors.DictCursor);
        
        try:
            with connection.cursor() as cursor:
                sql = "SELECT discordUserId, messageId FROM discord.biosMessages WHERE guildId = %s AND channelId = %s";
                cursor.execute(sql, (guildId, channelId));
                results = cursor.fetchall();
                for queryResult in results:
                    result.append({ "discordUserId": queryResult["discordUserId"], "messageId": queryResult["messageId"]});
        finally:
            connection.close();
        
        return result;
    
    def sqlDeleteBioMessageId(self, guildId, discordUserId, channelId, messageId):
        result = False;
        
        connection = pymysql.connect(host = self.settingsMySql.host, user = self.settingsMySql.user, password = self.settingsMySql.password, cursorclass=pymysql.cursors.DictCursor);
        
        try:
            with connection.cursor() as cursor:
                sql = "DELETE FROM discord.biosMessages WHERE guildId = %s AND discordUserId = %s AND channelId = %s AND messageId = %s";
                cursor.execute(sql, (guildId, discordUserId, channelId, messageId));
                connection.commit();
                result = True;
        finally:
            connection.close();
        
        return result;
    
    def sqlSetBioMessageId(self, guildId, discordUserId, channelId, messageId):
        result = False;
        
        connection = pymysql.connect(host = self.settingsMySql.host, user = self.settingsMySql.user, password = self.settingsMySql.password, cursorclass=pymysql.cursors.DictCursor);
        
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO discord.biosMessages (guildId, discordUserId, channelId, messageId) VALUES (%s, %s, %s, %s)";
                cursor.execute(sql, (guildId, discordUserId, channelId, messageId));
                connection.commit();
                result = True;
        finally:
            connection.close();
        
        return result;
    
    def sqlSetBioName(self, guildId, discordUserId, bioName):
        result = False;
        
        currentBioInfo = self.sqlGetBio(guildId, discordUserId);
        
        connection = pymysql.connect(host = self.settingsMySql.host, user = self.settingsMySql.user, password = self.settingsMySql.password, cursorclass=pymysql.cursors.DictCursor);
        
        try:
            with connection.cursor() as cursor:
                if currentBioInfo is None:
                    sql = "INSERT INTO discord.bios (guildId, discordUserId, bioName) VALUES (%s, %s, %s)";
                    cursor.execute(sql, (guildId, discordUserId, bioName));
                    connection.commit();
                else:
                    sql = "UPDATE discord.bios SET bioName = %s WHERE guildId = %s AND discordUserId = %s";
                    cursor.execute(sql, (bioName, guildId, discordUserId));
                    connection.commit();
                result = True;
        finally:
            connection.close();
        
        return result;
    
    def sqlSetBioImage(self, guildId, discordUserId, bioImage):
        result = False;
        
        currentBioInfo = self.sqlGetBio(guildId, discordUserId);
        
        connection = pymysql.connect(host = self.settingsMySql.host, user = self.settingsMySql.user, password = self.settingsMySql.password, cursorclass=pymysql.cursors.DictCursor);
        
        try:
            with connection.cursor() as cursor:
                if currentBioInfo is None:
                    sql = "INSERT INTO discord.bios (guildId, discordUserId, bioImage) VALUES (%s, %s, %s)";
                    cursor.execute(sql, (guildId, discordUserId, bioImage));
                    connection.commit();
                else:
                    sql = "UPDATE discord.bios SET bioImage = %s WHERE guildId = %s AND discordUserId = %s";
                    cursor.execute(sql, (bioImage, guildId, discordUserId));
                    connection.commit();
                result = True;
        finally:
            connection.close();
        
        return result;
    
    def sqlSetBioText(self, guildId, discordUserId, bioText):
        result = False;
        
        currentBioInfo = self.sqlGetBio(guildId, discordUserId);
        
        connection = pymysql.connect(host = self.settingsMySql.host, user = self.settingsMySql.user, password = self.settingsMySql.password, cursorclass=pymysql.cursors.DictCursor);
        
        try:
            with connection.cursor() as cursor:
                if currentBioInfo is None:
                    sql = "INSERT INTO discord.bios (guildId, discordUserId, bioText) VALUES (%s, %s, %s)";
                    cursor.execute(sql, (guildId, discordUserId, bioText));
                    connection.commit();
                else:
                    sql = "UPDATE discord.bios SET bioText = %s WHERE guildId = %s AND discordUserId = %s";
                    cursor.execute(sql, (bioText, guildId, discordUserId));
                    connection.commit();
                result = True;
        finally:
            connection.close();
        
        return result;        
   
    async def updateGuildBioChannels(self, guild):
        for role in guild.roles:
            for channelId in discordUtils.getChannelIdsByName(guild, "bio-{0}".format(role.name.lower()).replace(" ", "")):
                channel = await discordUtils.fetchChannelById(guild, channelId);
                userIds = discordUtils.getUserIdsByRoleId(guild, role.id);
                for userId in userIds:
                    bioInfo = self.sqlGetBio(guild.id, userId);
                    if bioInfo is not None and bioInfo["bioName"] is not None and bioInfo["bioText"] is not None and bioInfo["bioImage"] is not None:
                        embedImage = discord.Embed();
                        embedImage.set_image(url=bioInfo["bioImage"]);
                        message = "Name: {0}\nAbout:\n{1}".format(bioInfo["bioName"], bioInfo["bioText"])[:2000];
                        messageId = self.sqlGetBioMessageId(guild.id, userId, channelId);
                        if messageId is None:
                            sentMessage = await channel.send(message, embed=embedImage);
                            self.sqlSetBioMessageId(guild.id, userId, channelId, sentMessage.id);
                        else:
                            targetMessage = await channel.fetch_message(int(messageId));
                            await targetMessage.edit(content=message, embed=embedImage);
                messageUsers = self.sqlGetChannelBioMessageIds(guild.id, channelId);
                for messageUser in messageUsers:
                    if int(messageUser["discordUserId"]) not in userIds:
                        targetMessage = await channel.fetch_message(int(messageUser["messageId"]));
                        await targetMessage.delete();
                        self.sqlDeleteBioMessageId(guild.id, messageUser["discordUserId"], channelId, messageUser["messageId"]);
    
    @tasks.loop(minutes=5)
    async def updateBiosTask(self):
        for guild in self.discordClient.guilds:
            await self.updateGuildBioChannels(guild);
    
    def __init__(self, discordClient, settingsMySql):
        self.discordClient = discordClient;
        self.settingsMySql = settingsMySql;
        self.updateBiosTask.start();
    
    @commands.command(brief="Gets the bio for the target user or bio's for the target role", description="Gets the bio for the target user or bio's for the target role")
    async def getBio(self, ctx, target):
        roleMatch = re.search("\<\@\&(\d+)\>", target);
        userMatch = re.search("\<\@\!?(\d+)\>", target);
        if roleMatch is not None:
            userIds = discordUtils.getUserIdsByRoleId(ctx.guild, roleMatch.group(1));
            for userId in userIds:
                bioInfo = self.sqlGetBio(ctx.guild.id, userId);
                if bioInfo is not None and bioInfo["bioImage"] is not None:
                    embedImage = discord.Embed();
                    embedImage.set_image(url=bioInfo["bioImage"]);
                    await ctx.send("Name: {0}\nAbout:\n{1}".format(bioInfo["bioName"], bioInfo["bioText"])[:2000], embed=embedImage);
        elif userMatch is not None:
            bioInfo = self.sqlGetBio(ctx.guild.id, userMatch.group(1));
            if bioInfo is not None:
                embedImage = discord.Embed();
                embedImage.set_image(url=bioInfo["bioImage"]);
                await ctx.send("Name: {0}\nAbout:\n{1}".format(bioInfo["bioName"], bioInfo["bioText"])[:2000], embed=embedImage);
            else:
                await ctx.send("No bio found for {0}".format(target));
        else:
             await ctx.send("Error {0} is not a valid user or role".format(target));
    
    @commands.command(brief="Sets the name for your bio", description="Sets the name for your bio")
    async def setBioName(self, ctx, name):
        if self.sqlSetBioName(ctx.guild.id, ctx.author.id, name):
            await ctx.send("Set bioName for {0}".format(ctx.author.name));
        else:
            await ctx.send("Could not set bioName for {0}".format(ctx.author.name));
    
    @commands.command(brief="Sets the image for your bio", description="Sets the image for your bio")
    async def setBioImage(self, ctx):
        attachments = discordUtils.getMessageAttachments(ctx.message);
        if len(attachments) != 1:
            await ctx.send("Must attach 1 image to use for your bioImage");
        elif self.sqlSetBioImage(ctx.guild.id, ctx.author.id, attachments[0]):
            await ctx.send("Set bioImage for {0}".format(ctx.author.name));
        else:
            await ctx.send("Could not set bioImage for {0}".format(ctx.author.name));
    
    @commands.command(brief="After the command any text entered into the message will be your bio text. New lines allowed", description="After the command any text entered into the message will be your bio text. New lines allowed")
    async def setBioText(self, ctx, text):
        if self.sqlSetBioText(ctx.guild.id, ctx.author.id, ctx.message.content[12:]):
            await ctx.send("Set bioText for {0}".format(ctx.author.name));
        else:
            await ctx.send("Could not set bioText for {0}".format(ctx.author.name));
    
    @commands.command(brief="Triggers an update to the bio channels", description="Triggers an update to the bio channels")
    async def updateBioChannels(self, ctx):
        await self.updateGuildBioChannels(ctx.guild);
