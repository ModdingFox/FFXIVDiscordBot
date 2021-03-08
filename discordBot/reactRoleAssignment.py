from discord.ext import commands
from discord.ext.commands import has_permissions
from discord.utils import get
import re
import pymysql.cursors

class reactRoleAssignmentClass(commands.Cog, name='React Role Assignment'):
    def sqlEmoteRoleDelete(self, guildId, messageId):
        result = False;
        
        connection = pymysql.connect(host = self.settingsMySql.host, user = self.settingsMySql.user, password = self.settingsMySql.password, cursorclass=pymysql.cursors.DictCursor);
        
        try:
            with connection.cursor() as cursor:
                sql = "DELETE FROM discord.emoteRoles WHERE guildId = %s AND messageId = %s";
                cursor.execute(sql, (guildId, messageId));
                connection.commit();
                result = True;
        finally:
                connection.close();
        
        return result;
    
    def sqlEmoteRoleCreate(self, guildId, messageId, roleId, emote):
        result = False;
        
        self.sqlEmoteRoleDelete(guildId, messageId);
        
        connection = pymysql.connect(host = self.settingsMySql.host, user = self.settingsMySql.user, password = self.settingsMySql.password, cursorclass=pymysql.cursors.DictCursor);
        
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO discord.emoteRoles (guildId, messageId, roleId, emote) VALUES (%s, %s, %s, %s)";
                cursor.execute(sql, (guildId, messageId, roleId, emote));
                connection.commit();
                result = True;
        finally:
                connection.close();
        
        return result;
    
    def sqlEmoteRoleGet(self, guildId, messageId):
        result = None;

        connection = pymysql.connect(host = self.settingsMySql.host, user = self.settingsMySql.user, password = self.settingsMySql.password, cursorclass=pymysql.cursors.DictCursor);

        try:
            with connection.cursor() as cursor:
                sql = "SELECT roleId, emote FROM discord.emoteRoles WHERE guildId = %s AND messageId = %s";
                cursor.execute(sql, (guildId, messageId));
                results = cursor.fetchone();
                if results is not None:
                    result={ "roleId": results["roleId"], "emote": results["emote"] };
        finally:
                connection.close();

        return result;
    
    def initTables(self):
        result = False;
        
        connection = pymysql.connect(host = self.settingsMySql.host, user = self.settingsMySql.user, password = self.settingsMySql.password, cursorclass=pymysql.cursors.DictCursor);
        
        try:
            with connection.cursor() as cursor:
                cursor.execute("CREATE DATABASE IF NOT EXISTS discord COLLATE utf8mb4_unicode_ci");
                cursor.execute("CREATE TABLE IF NOT EXISTS discord.emoteRoles ( guildId   TEXT NOT NULL, messageId TEXT NOT NULL, roleId    TEXT NOT NULL, emote     TEXT NOT NULL )");
                result = True;
        finally:
                connection.close();
        
        return result;
    
    def __init__(self, discordClient, settingsMySql):
        self.discordClient = discordClient;
        self.settingsMySql = settingsMySql;
        self.initTables();
        
        @discordClient.listen()
        async def on_raw_reaction_add(payload):
            roleAssign = self.sqlEmoteRoleGet(payload.member.guild.id, payload.message_id);
            if roleAssign is not None and str(roleAssign["emote"]) == str(payload.emoji.name):
               role = get(payload.member.guild.roles, id=int(roleAssign["roleId"]));
               await payload.member.add_roles(role);
     
    @commands.command(brief="Adds a user to given role when they react to the specified message", description="Adds a user to given role when they react to the specified message")
    @has_permissions(manage_roles=True) 
    async def autoRoleAssignment(self, ctx, messageId, emote, role):
        roleMatch = re.search("\<\@\&(\d+)\>", role);
        if roleMatch is not None:
            highestRolePosition = 0;
            targetRole = get(ctx.guild.roles, id=int(roleMatch.group(1)));
            if targetRole is not None:
                for currentRole in ctx.message.author.roles:
                    if currentRole.position > highestRolePosition:
                        highestRolePosition = currentRole.position;
                if targetRole.position < highestRolePosition:
                    self.sqlEmoteRoleCreate(ctx.guild.id, messageId, targetRole.id, emote);
                    await ctx.send("Assigned {0} to message {1} with emote {2}".format(role, messageId, emote));
                else:
                    await ctx.send("Your role must be higher than the {0} role".format(role));
            else:
                await ctx.send("Could not find specified role");
        else:
            await ctx.send("Must provide a valid role");
