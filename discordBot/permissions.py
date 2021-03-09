import discordUtils

from discord.ext import commands
from discord.utils import get
import pymysql.cursors
import re

class PermissionsClass(commands.Cog, name='Permissions Management'):
    def sqlRemovePermission(self, guildId, roleId, commandName):
        result = False;
        
        connection = pymysql.connect(host = self.settingsMySql.host, user = self.settingsMySql.user, password = self.settingsMySql.password, cursorclass=pymysql.cursors.DictCursor);
        
        try:
            with connection.cursor() as cursor:
                sql = "DELETE FROM discord.commandPermissions WHERE guildId = %s AND roleId = %s AND commandName = %s";
                cursor.execute(sql, (guildId, roleId, commandName));
                connection.commit();
                result = True;
        finally:
            connection.close();
        
        return result;
    
    def sqlAddPermission(self, guildId, roleId, commandName):
        result = False;
        
        self.sqlRemovePermission(guildId, roleId, commandName);
        
        connection = pymysql.connect(host = self.settingsMySql.host, user = self.settingsMySql.user, password = self.settingsMySql.password, cursorclass=pymysql.cursors.DictCursor);
        
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO discord.commandPermissions (guildId, roleId, commandName, isAllowed) VALUES (%s, %s, %s, true)";
                cursor.execute(sql, (guildId, roleId, commandName));
                connection.commit();
                result = True;
        finally:
            connection.close();
        
        return result;
    
    def sqlGetPermissions(self, guildId, commandName):
        result = [];
        
        connection = pymysql.connect(host = self.settingsMySql.host, user = self.settingsMySql.user, password = self.settingsMySql.password, cursorclass=pymysql.cursors.DictCursor);
        
        try:
            with connection.cursor() as cursor:
                sql = "SELECT roleId FROM discord.commandPermissions WHERE guildId = %s AND commandName = %s";
                cursor.execute(sql, (guildId, commandName));
                results = cursor.fetchall();
                for queryResult in results:
                    result.append(int(queryResult["roleId"]));
        finally:
            connection.close();
        
        return result;
    
    def initTables(self):
        result = False;
        
        connection = pymysql.connect(host = self.settingsMySql.host, user = self.settingsMySql.user, password = self.settingsMySql.password, cursorclass=pymysql.cursors.DictCursor);
        
        try:
            with connection.cursor() as cursor:
                cursor.execute("CREATE DATABASE IF NOT EXISTS discord COLLATE utf8mb4_unicode_ci");
                cursor.execute("CREATE TABLE IF NOT EXISTS discord.commandPermissions ( guildId      TEXT    NOT NULL, roleId       TEXT    NOT NULL, commandName  TEXT    NOT NULL, isAllowed    BOOLEAN NOT NULL )");
                result = True;
        finally:
                connection.close();
        
        return result;
    
    def getCommandNames(self):
        commandNames = [];
        for command in self.discordClient.commands:
            commandNames.append(command.name);
        return commandNames;
    
    def __init__(self, discordClient, settingsMySql):
        self.discordClient = discordClient;
        self.settingsMySql = settingsMySql;
        self.initTables();
        
        @discordClient.check
        async def globalPermissionsCheck(ctx):
            if ctx.command.name == "help":
                return True;
            elif ctx.message.author.guild_permissions.administrator:
                return True;
            else:
                discordUserRoles = set(discordUtils.getUserRoleIds(ctx));
                commandPermissions = set(self.sqlGetPermissions(ctx.guild.id, ctx.command.name));
                rolesWithPermission = len(discordUserRoles & commandPermissions);
                if rolesWithPermission > 0:
                    return True;
                else:
                    return False;
    
    @commands.command(brief="Allows a role access to a command", description="Allows a role access to a command")
    async def premissionsAdd(self, ctx, role, command):
        if command in self.getCommandNames():
            roleMatch = re.search("\<\@\&(\d+)\>", role);
            if roleMatch is not None:
                targetRole = get(ctx.guild.roles, id=int(roleMatch.group(1)));
                if targetRole is not None:
                    if self.sqlAddPermission(ctx.guild.id, targetRole.id, command):
                        await ctx.send("Access to {0} added for {1}".format(command, role));
                    else:
                        await ctx.send("Failet to add access to {0} for {1}".format(command, role));
                else:
                    await ctx.send("Could not find role {0}".format(role));
            else:
                await ctx.send("Must provide a valid role");
        else:
            await ctx.send("Command {0} not found".format(command));
    
    @commands.command(brief="Disallows a role access to a command", description="Disallows a role access to a command")
    async def premissionsRemove(self, ctx, role, command):
        if command in self.getCommandNames():
            roleMatch = re.search("\<\@\&(\d+)\>", role);
            if roleMatch is not None:
                targetRole = get(ctx.guild.roles, id=int(roleMatch.group(1)));
                if targetRole is not None:
                    if self.sqlRemovePermission(ctx.guild.id, targetRole.id, command):
                        await ctx.send("Access to {0} removed for {1}".format(command, role));
                    else:
                        await ctx.send("Failet to remove access to {0} for {1}".format(command, role));
                else:
                    await ctx.send("Could not find role {0}".format(role));
            else:
                await ctx.send("Must provide a valid role");
        else:
            await ctx.send("Command {0} not found".format(command));
