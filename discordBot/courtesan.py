import discordUtils

from discord.ext import commands
from discord.utils import get
import pymysql.cursors

class courtesanClass(commands.Cog, name='Courtesans'):
    def sqlGetCourtesanAvailability(self, guildId):
        result = {};
        
        connection = pymysql.connect(host = self.settingsMySql.host, user = self.settingsMySql.user, password = self.settingsMySql.password, cursorclass=pymysql.cursors.DictCursor);
        
        try:
            with connection.cursor() as cursor:
                sql = "SELECT discordUserId, isAvaliable FROM discord.courtesanAvailability WHERE guildId = %s";
                cursor.execute(sql, (guildId));
                results = cursor.fetchall();
                for queryResult in results:
                    result[queryResult["discordUserId"]] = queryResult["isAvaliable"];
        finally:
            connection.close();
        
        return result;
    
    def sqlDeleteCourtesanAvailability(self, guildId, discordUserId):
        result = False;
        
        connection = pymysql.connect(host = self.settingsMySql.host, user = self.settingsMySql.user, password = self.settingsMySql.password, cursorclass=pymysql.cursors.DictCursor);
        
        try:
            with connection.cursor() as cursor:
                sql = "DELETE FROM discord.courtesanAvailability WHERE guildId = %s AND discordUserId = %s";
                cursor.execute(sql, (guildId, discordUserId));
                connection.commit();
                result = True;
        finally:
            connection.close();
        
        return result;
    
    def sqlSetCourtesanAvailability(self, guildId, discordUserId, isAvaliable):
        result = False;
        
        self.sqlDeleteCourtesanAvailability(guildId, discordUserId);
        
        connection = pymysql.connect(host = self.settingsMySql.host, user = self.settingsMySql.user, password = self.settingsMySql.password, cursorclass=pymysql.cursors.DictCursor);
        
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO discord.courtesanAvailability (guildId, discordUserId, isAvaliable) VALUES (%s, %s, %s)";
                cursor.execute(sql, (guildId, discordUserId, isAvaliable));
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
                cursor.execute("CREATE TABLE IF NOT EXISTS discord.courtesanAvailability ( guildId       TEXT    NOT NULL, discordUserId TEXT    NOT NULL, isAvaliable   BOOLEAN NOT NULL )");
                result = True;
        finally:
                connection.close();
        
        return result;
    
    def __init__(self, discordClient, settingsMySql):
        self.discordClient = discordClient;
        self.settingsMySql = settingsMySql;
        self.initTables();
    
    @commands.command(brief="Gets a list of all courtesans and their current avaliability", description="Gets a list of all courtesans and their current avaliability")
    async def courtesanList(self, ctx):
        courtesanRoleIds = discordUtils.getRoleByName(ctx.guild, "Courtesan");
        if len(courtesanRoleIds) > 0:
            courtesanRole = get(ctx.guild.roles, id=int(courtesanRoleIds[0]));
            courtesanAvailabilityHeading = "**Courtesan Availability**\nList of our current courtesans and their availability.\n**Courtesan**{0}**Status**\n";
            courtesanAvailabilityLineTemplate = "<@{0}>{1}{2}";
            courtesanAvailabilityLines = [];
            
            courtesanAvailabilityList = self.sqlGetCourtesanAvailability(ctx.guild.id);
            courtesanNameLengths = {};
            
            maxUserNameLength = 10;
            
            for courtesanDiscordId in courtesanAvailabilityList.keys():
                targetDiscordUser = ctx.guild.get_member(int(courtesanDiscordId));
                if targetDiscordUser is None or courtesanRole not in targetDiscordUser.roles:
                    self.sqlDeleteCourtesanAvailability(ctx.guild.id, courtesanDiscordId);
                else:
                    if targetDiscordUser.nick is not None:
                        if len(targetDiscordUser.nick) > maxUserNameLength:
                            maxUserNameLength = len(targetDiscordUser.nick);
                        courtesanNameLengths[courtesanDiscordId] = len(targetDiscordUser.nick);
                    else:
                        if len(targetDiscordUser.name) > maxUserNameLength:
                            maxUserNameLength = len(targetDiscordUser.name);
                        courtesanNameLengths[courtesanDiscordId] = len(targetDiscordUser.name);
            
            for courtesanDiscordId in courtesanNameLengths.keys():
                courtesanAvailabilityLines.append(courtesanAvailabilityLineTemplate.format(courtesanDiscordId, " " * ((maxUserNameLength - courtesanNameLengths[courtesanDiscordId]) + 3) , "Avaliable  " if courtesanAvailabilityList[courtesanDiscordId] else "Unavaliable"));
            
            await ctx.send(courtesanAvailabilityHeading.format(" " * ((maxUserNameLength - 9) + 4)) + "\n".join(courtesanAvailabilityLines));
        else:
           await ctx.send("A Courtesan role is required on the server"); 
    
    @commands.command(brief="Sets own courtesans status as avaliable", description="Sets own courtesans status as avaliable")
    async def courtesanSetAvaliable(self, ctx):
        if self.sqlSetCourtesanAvailability(ctx.guild.id, ctx.author.id, True):
            await ctx.send("Courtesan availability status set");
        else:
            await ctx.send("Failed to set courtesan availability status");
    
    @commands.command(brief="Sets own courtesans status as unavaliable", description="Sets own courtesans status as unavaliable")
    async def courtesanSetUnavaliable(self, ctx):
        if self.sqlSetCourtesanAvailability(ctx.guild.id, ctx.author.id, False):
            await ctx.send("Courtesan availability status set");
        else:
            await ctx.send("Failed to set courtesan availability status");
