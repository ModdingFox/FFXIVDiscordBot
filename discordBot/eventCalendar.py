import discord
from discord.ext import commands
from discord.ext import tasks
import pymysql.cursors
import re
from datetime import datetime

class eventCalendarClass(commands.Cog, name='Event Calendar'):
    def sqlGetEventMessageId(self, guildId, eventName, channelId):
        result = None;
        
        connection = pymysql.connect(host = self.settingsMySql.host, user = self.settingsMySql.user, password = self.settingsMySql.password, cursorclass=pymysql.cursors.DictCursor);
        
        try:
            with connection.cursor() as cursor:
                sql = "SELECT messageId FROM discord.eventCalendarMessages WHERE guildId = %s AND eventName = %s AND channelId = %s";
                cursor.execute(sql, (guildId, eventName, channelId));
                results = cursor.fetchall();
                for queryResult in results:
                    result = queryResult["messageId"];
        finally:
            connection.close();
        
        return result;
    
    def sqlGetChannelEventMessageIds(self, guildId, channelId):
        result = [];
        
        connection = pymysql.connect(host = self.settingsMySql.host, user = self.settingsMySql.user, password = self.settingsMySql.password, cursorclass=pymysql.cursors.DictCursor);
        
        try:
            with connection.cursor() as cursor:
                sql = "SELECT eventName, messageId FROM discord.eventCalendarMessages WHERE guildId = %s AND channelId = %s";
                cursor.execute(sql, (guildId, channelId));
                results = cursor.fetchall();
                for queryResult in results:
                    result.append({ "eventName": queryResult["eventName"], "messageId": queryResult["messageId"]});
        finally:
            connection.close();
        
        return result;
    
    def sqlDeleteEventMessageId(self, guildId, eventName, channelId, messageId):
        result = False;
        
        connection = pymysql.connect(host = self.settingsMySql.host, user = self.settingsMySql.user, password = self.settingsMySql.password, cursorclass=pymysql.cursors.DictCursor);
        
        try:
            with connection.cursor() as cursor:
                sql = "DELETE FROM discord.eventCalendarMessages WHERE guildId = %s AND eventName = %s AND channelId = %s AND messageId = %s";
                cursor.execute(sql, (guildId, eventName, channelId, messageId));
                connection.commit();
                result = True;
        finally:
            connection.close();
        
        return result;
    
    def sqlSetEventMessageId(self, guildId, eventName, channelId, messageId):
        result = False;
        
        connection = pymysql.connect(host = self.settingsMySql.host, user = self.settingsMySql.user, password = self.settingsMySql.password, cursorclass=pymysql.cursors.DictCursor);
        
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO discord.eventCalendarMessages (guildId, eventName, channelId, messageId) VALUES (%s, %s, %s, %s)";
                cursor.execute(sql, (guildId, eventName, channelId, messageId));
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
                cursor.execute("CREATE TABLE IF NOT EXISTS discord.eventCalendar (  guildId       TEXT     NOT NULL, eventDateTime DATETIME NOT NULL, eventReminder INT      NOT NULL, eventName     TEXT, eventText     TEXT )");
                cursor.execute("CREATE TABLE IF NOT EXISTS discord.eventCalendarMessages ( guildId       TEXT NOT NULL, eventName TEXT NOT NULL, channelId     TEXT NOT NULL, messageId     TEXT NOT NULL )");
                result = True;
        finally:
                connection.close();
        
        return result;
    
    def sqlGetEvents(self, guildId):
        result = [];
        
        connection = pymysql.connect(host = self.settingsMySql.host, user = self.settingsMySql.user, password = self.settingsMySql.password, cursorclass=pymysql.cursors.DictCursor);
        
        try:
            with connection.cursor() as cursor:
                sql = "SELECT eventDateTime, eventReminder, eventName, eventText FROM discord.eventCalendar WHERE guildId = %s";
                cursor.execute(sql, (guildId));
                results = cursor.fetchall();
                for queryResult in results:
                    result.append({"eventDateTime": queryResult["eventDateTime"], "eventReminder": queryResult["eventReminder"], "eventName": queryResult["eventName"], "eventText": queryResult["eventText"]});
        finally:
            connection.close();
        
        return result;
    
    def sqlRemoveEvent(self, guildId, eventName):
        result = False
        
        connection = pymysql.connect(host = self.settingsMySql.host, user = self.settingsMySql.user, password = self.settingsMySql.password, cursorclass=pymysql.cursors.DictCursor);
        
        try:
            with connection.cursor() as cursor:
                sql = "DELETE FROM discord.eventCalendar WHERE guildId = %s AND eventName = %s";
                cursor.execute(sql, (guildId, eventName));
                connection.commit();
                result = True;
        finally:
                connection.close();
        
        return result;
    
    def sqlCreateEvent(self, guildId, eventDateTime, eventReminder, eventName, eventText):
        result = False;
        
        self.sqlRemoveEvent(guildId, eventName);
        
        connection = pymysql.connect(host = self.settingsMySql.host, user = self.settingsMySql.user, password = self.settingsMySql.password, cursorclass=pymysql.cursors.DictCursor);
        
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO discord.eventCalendar (guildId, eventDateTime, eventReminder, eventName, eventText) VALUES (%s, %s, %s, %s, %s)";
                cursor.execute(sql, (guildId, eventDateTime, eventReminder, eventName, eventText));
                connection.commit();
                result = True;
        finally:
            connection.close();
        
        return result;
    
    async def updateGuildEventChannels(self, guild):
        pass;
    
    @tasks.loop(minutes=5)
    async def updateEventsTask(self):
        for guild in self.discordClient.guilds:
            await self.updateGuildEventChannels(ctx.guild);
    
    def __init__(self, discordClient, settingsMySql):
        self.discordClient = discordClient;
        self.settingsMySql = settingsMySql;
        self.initTables();
        self.updateEventsTask.start();
    
    @commands.command(brief="Creates an event in the events channel and will send a reminder in the current-events text channel some period before the event", description="Creates an event in the events channel and will send a reminder in the current-events text channel some period before the event")
    async def createEvent(self, ctx, ISO8601DateTime, preEventReminderInMin, eventName, eventText):
        timeDateMatch = re.search("^\d{4}-\d{2}-\d{2}T\d{2}\:\d{2}Z$", ISO8601DateTime);
        preEventReminderInMinMatch = re.search("^\d+$", preEventReminderInMin);
        
        if timeDateMatch is not None and preEventReminderInMinMatch is not None and int(preEventReminderInMin) >= 0:
            try:
                currentTime = datetime.utcnow();
                eventTime = datetime.strptime(ISO8601DateTime,'%Y-%m-%dT%H:%MZ');
                if currentTime < eventTime:
                    self.sqlCreateEvent(ctx.guild.id, eventTime, preEventReminderInMin, eventName, eventText);
                    await ctx.send("Created event");
                else:
                    await ctx.send("Event time provided is in the past");
            except:
                await ctx.send("The provided time is invalid");
        elif timeDateMatch is None:
            await ctx.send("Time format must be YYYY-MM-DDThh:mmZ");
        elif preEventReminderInMinMatch is None:
            await ctx.send("Preevent Reminder In Min must be a number 0 or greater");
        else:
            await ctx.send("Bad things happened report this to your admin");
    
    @commands.command(brief="Deletes an event", description="Deletes an event")
    async def deleteEvent(self, ctx, eventNameeventList):
        print("Not implimented");
    
    @commands.command(brief="Lists all future events", description="Lists all future events")
    async def listEvents(self, ctx):
        eventList = self.sqlGetEvents(ctx.guild.id);
        eventTemplate = "{1}\nWhen: {0} Server Time\n{2}";
        for event in eventList:
            await ctx.send(eventTemplate.format(event["eventDateTime"], event["eventName"], event["eventText"]));
        if len(eventList):
            await ctx.send("No upcoming events")
    
    @commands.command(brief="Triggers updates to event channels", description="Triggers updates to event channels")
    async def updateEvents(self, ctx):
        await self.updateGuildEventChannels(ctx.guild);
