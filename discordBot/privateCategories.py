import discordUtils

import discord
from discord.ext import commands
from discord.ext import tasks
import pymysql.cursors
import re
import time
import datetime
from datetime import datetime

#ToDo:
#    mySql Table Init

class privateCategoriesClass(commands.Cog, name='Private Categories'):
    def sqlPrivateCategoryCreate(self, guildId, discordId, userName, categoryId):
        result = False;
        
        connection = pymysql.connect(host = self.settingsMySql.host, user = self.settingsMySql.user, password = self.settingsMySql.password, cursorclass=pymysql.cursors.DictCursor);
        
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO discord.privateRooms (guildId, ownerDiscordUserId, userName, categoryId) VALUES (%s, %s, %s, %s)";
                cursor.execute(sql, (guildId, discordId, userName, categoryId));
                connection.commit();
                result = True;
        finally:
                connection.close();
        
        return result;
    
    def sqlPrivateCategoryGetOwnerDiscordId(self, guildId, categoryId):
        result = None;
        
        connection = pymysql.connect(host = self.settingsMySql.host, user = self.settingsMySql.user, password = self.settingsMySql.password, cursorclass=pymysql.cursors.DictCursor);
        
        try:
            with connection.cursor() as cursor:
                sql = "SELECT distinct ownerDiscordUserId FROM discord.privateRooms WHERE guildId = %s AND categoryId = %s";
                cursor.execute(sql, (guildId, categoryId));
                results = cursor.fetchone();
                if results is not None:
                    result=results["ownerDiscordUserId"];
        finally:
                connection.close();
        
        return result;
    
    def sqlPrivateCategoryDelete(self, guildId, categoryId):
        result = False;
        
        connection = pymysql.connect(host = self.settingsMySql.host, user = self.settingsMySql.user, password = self.settingsMySql.password, cursorclass=pymysql.cursors.DictCursor);
        
        try:
            with connection.cursor() as cursor:
                sql = "DELETE FROM discord.privateRooms WHERE guildId = %s AND categoryId = %s";
                cursor.execute(sql, (guildId, categoryId));
                connection.commit();
                result = True;
        finally:
                connection.close();
        
        return result;
    
    def sqlPrivateCategoryList(self, guildId):
        result = [];
        
        connection = pymysql.connect(host = self.settingsMySql.host, user = self.settingsMySql.user, password = self.settingsMySql.password, cursorclass=pymysql.cursors.DictCursor);
        
        try:
            with connection.cursor() as cursor:
                sql = "SELECT distinct ownerDiscordUserId, categoryId FROM discord.privateRooms WHERE guildId = %s";
                cursor.execute(sql, (guildId));
                results = cursor.fetchall();
                for queryResult in results:
                    result.append(queryResult);
        finally:
                connection.close();
        
        return result;
    
    @tasks.loop(minutes=30)
    async def cleanPrivateChats(self):
        for guild in self.discordClient.guilds:
            privateCategories = self.sqlPrivateCategoryList(guild.id);
            categories = guild.categories;
            categoryIds = {};
            for category in categories:
                categoryIds[str(category.id)] = category;
            for privateCategory in privateCategories:
                if privateCategory["categoryId"] in list(categoryIds):
                    category = categoryIds[privateCategory["categoryId"]];
                    shouldDelete = True;
                    for textChannel in category.text_channels:
                        last_message_id = textChannel.last_message_id;
                        if last_message_id is not None:
                            lastMessage = None;
                            try:
                                lastMessage = await textChannel.fetch_message(last_message_id);
                            except discord.errors.NotFound as e:
                                lastMessage = None;
                            if lastMessage is not None:
                                timeDelta = (datetime.utcnow() - lastMessage.created_at).total_seconds();
                                if timeDelta < 3600:
                                    shouldDelete=False;
                    member = await guild.fetch_member(privateCategory["ownerDiscordUserId"]);
                    if member is not None and member.voice is not None and member.voice.channel is not None and member.voice.channel.id is not None:
                        for voiceChannel in category.voice_channels:
                            if member.voice.channel.id == voiceChannel.id:
                                shouldDelete = False;
                    if shouldDelete == True:
                        for textChannel in category.text_channels:
                            await textChannel.delete();
                        for voiceChannel in category.voice_channels:
                            await voiceChannel.delete();
                        await category.delete();
                        self.sqlPrivateCategoryDelete(guild.id, privateCategory["categoryId"]);
    
    def __init__(self, discordClient, settingsMySql):
        self.discordClient = discordClient;
        self.settingsMySql = settingsMySql;
        self.cleanPrivateChats.start();
        
    @commands.command(brief="Creates a private category with voice and text", description="Creates a private category with voice and text")
    async def privateCategoryCreate(self, ctx, users):
        commandMatchs = re.findall("\<\@\!?(\d+)\>", ctx.message.content);
        if len(commandMatchs) > 0 :
            users=[];
            for commandMatch in commandMatchs:
                targetUserDiscordId = int(commandMatch);
                targetDiscordUser = ctx.guild.get_member(targetUserDiscordId);
                if targetDiscordUser.id == ctx.message.author.id:
                    await ctx.send("The requestor is automatically added please do not include yourself in the list");
                elif targetDiscordUser is not None:
                    users.append(targetDiscordUser);
            if len(users) > 0 and len(users) == len(commandMatchs):
                moderatorRoleIds = discordUtils.getRoleByName(ctx.guild, "Moderator");
                if len(moderatorRoleIds) > 0:
                    moderatorRoleId = moderatorRoleIds[0];
                    overwrites = {
                        ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                        ctx.message.author: discord.PermissionOverwrite(add_reactions=True, read_messages=True, view_channel=True, send_messages=True, send_tts_messages=True, embed_links=True, attach_files=True, read_message_history=True, connect=True, speak=True, mute_members=True, deafen_members=True, use_voice_activation=True),
                        ctx.guild.get_role(moderatorRoleId): discord.PermissionOverwrite(manage_channels=True, add_reactions=True, read_messages=True, view_channel=True, send_messages=True, send_tts_messages=True, embed_links=True, attach_files=True, read_message_history=True, connect=True, speak=True, mute_members=True, deafen_members=True, use_voice_activation=True)
                    };
                    newCategory = await ctx.guild.create_category("Private Room", overwrites=overwrites);
                    newTextChannel = await ctx.guild.create_text_channel("private-text", overwrites=None, category=newCategory);
                    await newTextChannel.send("This private category will exist as long as the creator is in the voice chat otherwise it be deleted after 30 min of inactivity in the text chat.");
                    newVoiceChannel = await ctx.guild.create_voice_channel("Private Voice", overwrites=None, category=newCategory);
                    self.sqlPrivateCategoryCreate(ctx.guild.id, ctx.message.author.id, ctx.message.author.name, newCategory.id);
                    for user in users:
                        await newCategory.set_permissions(user, add_reactions=True, read_messages=True, view_channel=True, send_messages=True, send_tts_messages=True, embed_links=True, attach_files=True, read_message_history=True, connect=True, speak=True, use_voice_activation=True);
                else:
                    await ctx.send("A Moderator role is required on the server");
            else:
                await ctx.send("{0} users could not be added to the category".format(len(commandMatchs) - len(users)));
        else:
             await ctx.send("You must provide a list of users");
    
    @commands.command(brief="Removes a user from the current private category. Only usable in the private chat by the creator", description="Removes a user from the current private category. Only usable in the private chat by the creator")
    async def privateCategoryKick(self, ctx, user):
        categoryOwnerDiscordId = self.sqlPrivateCategoryGetOwnerDiscordId(ctx.guild.id, ctx.message.channel.category.id);
        if str(ctx.message.author.id) == categoryOwnerDiscordId:
            commandMatch = re.search("\<\@\!?(\d+)\>", user);
            if commandMatch is not None:
                 targetUserDiscordId = int(commandMatch.group(1));
                 targetDiscordUser = ctx.guild.get_member(targetUserDiscordId);
                 if targetDiscordUser is not None:
                     if ctx.message.author.id is not targetDiscordUser.id:
                         await ctx.message.channel.category.set_permissions(targetDiscordUser, overwrite=None);
                         await ctx.message.channel.send("User premissions removed");
                     else:
                         await ctx.message.channel.send("You can't remove yourself");
                 else:
                     await ctx.message.channel.send("Could not find user");
            else:
                 await ctx.message.channel.send("You must provide a valid user to remove from the private chat");
        elif categoryOwnerDiscordId is not None:
             await ctx.message.channel.send("Only the chat creator can do that");
    
    @commands.command(brief="Leaves the category. If you are the owner it destroys the current private category", description="Leaves the category. If you are the owner it destroys the current private category")
    async def privateCategoryExit(self, ctx):
        categoryOwnerDiscordId = self.sqlPrivateCategoryGetOwnerDiscordId(ctx.guild.id, ctx.message.channel.category.id);
        if str(ctx.message.author.id) == categoryOwnerDiscordId:
             categoryId = ctx.message.channel.category.id;
             for channel in ctx.message.channel.category.channels:
                 await channel.delete();
             await ctx.message.channel.category.delete();
             self.sqlPrivateCategoryDelete(ctx.guild.id, categoryId);
        elif categoryOwnerDiscordId is not None:
              await ctx.message.channel.category.set_permissions(ctx.message.author, overwrite=None);
