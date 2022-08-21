#!/bin/python3.9

from settings import discordSettings, mySqlSettings, ldapSettings

import botManagement
import clubMenu
import courtesan
import eventCalendar
import extraStuff
import lodestone
import manageChatHistory
import normalizeMessages
import permissions
import privateCategories
import radarList
import reactRoleAssignment
import staffApplications
import textLogging
import userBios
import voiceLogging

import asyncio
import discord
from discord.ext import commands
from discord.ext import tasks

async def main():
    settingsDiscord = discordSettings.discordSettingsClass("conf/discord.json");
    settingsMySql = mySqlSettings.mySqlSettingsClass("conf/mySql.json");
    settingsLdap = ldapSettings.ldapSettingsClass("conf/ldap.json");
    
    intents = discord.Intents.default();
    intents.members = True;
    intents.message_content = True;
    
    client = commands.Bot(command_prefix=settingsDiscord.commandPrefix, intents=intents);
    
    #Load Cogs
    await client.add_cog(botManagement.botManagementClass(client));
    await client.add_cog(courtesan.courtesanClass(client, settingsMySql));
    await client.add_cog(clubMenu.clubMenuClass(client, settingsMySql));
    #await client.add_cog(eventCalendar.eventCalendarClass(client, settingsMySql));
    await client.add_cog(extraStuff.extraStuffClass(client));
    await client.add_cog(lodestone.lodestoneClass(client));
    await client.add_cog(manageChatHistory.manageChatHistoryClass(client, settingsMySql));
    await client.add_cog(normalizeMessages.normalizeMessagesClass(client));
    await client.add_cog(permissions.PermissionsClass(client, settingsMySql));
    await client.add_cog(privateCategories.privateCategoriesClass(client, settingsMySql));
    await client.add_cog(radarList.radarListClass(client, settingsMySql));
    await client.add_cog(reactRoleAssignment.reactRoleAssignmentClass(client, settingsMySql));
    await client.add_cog(staffApplications.staffApplicationsClass(client, settingsMySql));
    await client.add_cog(textLogging.textLoggingClass(client, settingsMySql));
    await client.add_cog(userBios.userBiosClass(client, settingsMySql));
    await client.add_cog(voiceLogging.voiceLoggingClass(client, settingsMySql));
    
    @client.event
    async def on_ready():
        print(f'{client.user} has connected to Discord!');
    
    await client.start(settingsDiscord.token);

asyncio.run(main());
