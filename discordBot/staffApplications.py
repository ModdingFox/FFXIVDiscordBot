import discordUtils

import discord
from discord.ext import commands
from discord.ext import tasks
import pymysql.cursors

class staffApplicationsClass(commands.Cog, name='Staff Applications'):
    def sqlGetNewApplicationsId(self, guildId, lastApplicationId):
        result = {};
        
        connection = pymysql.connect(host = self.settingsMySql.host, user = self.settingsMySql.user, password = self.settingsMySql.password, cursorclass=pymysql.cursors.DictCursor);
        
        try:
            with connection.cursor() as cursor:
                sql = "SELECT id, question11 FROM ClubSpectrum.applications WHERE guildId = %s AND id > %s";
                cursor.execute(sql, (str(guildId), lastApplicationId));
                results = cursor.fetchall();
                for queryResult in results:
                    result[queryResult["id"]] = queryResult["question11"];
        finally:
            connection.close();
        
        return result;
    
    def sqlGetLastApplicationId(self, guildId):
        result = 0;
        
        connection = pymysql.connect(host = self.settingsMySql.host, user = self.settingsMySql.user, password = self.settingsMySql.password, cursorclass=pymysql.cursors.DictCursor);
        
        try:
            with connection.cursor() as cursor:
                sql = "SELECT lastId FROM discord.currentStaffApplication WHERE guildId = %s";
                cursor.execute(sql, (guildId));
                results = cursor.fetchall();
                for queryResult in results:
                    result = queryResult["lastId"];
        finally:
            connection.close();
        
        return result;
    
    def sqlSetLastApplicationId(self, guildId, lastId):
        result = False;
        
        connection = pymysql.connect(host = self.settingsMySql.host, user = self.settingsMySql.user, password = self.settingsMySql.password, cursorclass=pymysql.cursors.DictCursor);
        
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO discord.currentStaffApplication (guildId, lastId) VALUES (%s, %s) ON DUPLICATE KEY UPDATE lastId=%s";
                cursor.execute(sql, (guildId, int(lastId), int(lastId)));
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
                cursor.execute("CREATE TABLE IF NOT EXISTS discord.currentStaffApplication ( guildId       BIGINT NOT NULL,    lastId INT  NOT NULL,    PRIMARY KEY (guildId) )");
                result = True;
        finally:
                connection.close();
        
        return result;
    
    async def updateStaffApplicationChannels(self, guild):
        managementRoleIds = discordUtils.getRoleByName(guild, "Management");
        managementRoleId = None;
        if len(managementRoleIds) > 0:
            managementRoleId = "<@&" + str(managementRoleIds[0]) + ">";
        else:
            managementRoleId = "@here"
        lastId = self.sqlGetLastApplicationId(guild.id);
        applications = self.sqlGetNewApplicationsId(guild.id, lastId);
        messageText = "{2}\n{0} submitted an application. To view it https://clubspectrum.us/staff.php/?applicationId={1}#application";
        messages = [];
        highestId = lastId;
        for application in applications.keys():
            if highestId < application:
                highestId = application
            messages.append(messageText.format(applications[application], application, managementRoleId));
        for channelId in discordUtils.getChannelIdsByName(guild, "staff-applications"):
            channel = await discordUtils.fetchChannelById(guild, channelId);
            for message in messages:
                sentMessage = await channel.send(message);
        self.sqlSetLastApplicationId(guild.id, highestId);
    
    @tasks.loop(minutes=5)
    async def updateStaffApplicationsTask(self):
        for guild in self.discordClient.guilds:
            await self.updateStaffApplicationChannels(guild);
    
    def __init__(self, discordClient, settingsMySql):
        self.discordClient = discordClient;
        self.settingsMySql = settingsMySql;
        self.initTables();
        self.updateStaffApplicationsTask.start();
    
    @commands.command(brief="Force an update of the staff-applications channels", description="Force an update of the staff-applications channels")
    async def updateStaffApplication(self, ctx):
        await self.updateStaffApplicationChannels(ctx.guild);

