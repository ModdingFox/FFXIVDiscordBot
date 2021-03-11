#!/bin/python3

from settings import discordSettings, mySqlSettings, ldapSettings

import botManagement
import clubMenu
import courtesan
import extraStuff
import lodestone
import normalizeMessages
import permissions
import privateCategories
import reactRoleAssignment
import textLogging
import userBios
import voiceLogging

import discord
from discord.ext import commands
from discord.ext import tasks

settingsDiscord = discordSettings.discordSettingsClass("conf/discord.json");
settingsMySql = mySqlSettings.mySqlSettingsClass("conf/mySql.json");
settingsLdap = ldapSettings.ldapSettingsClass("conf/ldap.json");

intents = discord.Intents.default();
intents.members = True;

client = commands.Bot(command_prefix=settingsDiscord.commandPrefix, intents=intents);

#Load Cogs
client.add_cog(botManagement.botManagementClass(client));
client.add_cog(courtesan.courtesanClass(client, settingsMySql));
client.add_cog(clubMenu.clubMenuClass(client, settingsMySql));
client.add_cog(extraStuff.extraStuffClass(client));
client.add_cog(lodestone.lodestoneClass(client));
client.add_cog(normalizeMessages.normalizeMessagesClass(client));
client.add_cog(permissions.PermissionsClass(client, settingsMySql));
client.add_cog(privateCategories.privateCategoriesClass(client, settingsMySql));
client.add_cog(reactRoleAssignment.reactRoleAssignmentClass(client, settingsMySql));
client.add_cog(textLogging.textLoggingClass(client, settingsMySql));
client.add_cog(userBios.userBiosClass(client, settingsMySql));
client.add_cog(voiceLogging.voiceLoggingClass(client, settingsMySql));

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!');

client.run(settingsDiscord.token);
