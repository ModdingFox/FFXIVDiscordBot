#!/bin/python3

from settings import discordSettings, mySqlSettings, ldapSettings

import loggingModule

import botManagement
import clubMenu
import extraStuff
import privateCategories
import userBios

import discord
from discord.ext import commands
from discord.ext import tasks

settingsDiscord = discordSettings.discordSettingsClass("conf/discord.json");
settingsMySql = mySqlSettings.mySqlSettingsClass("conf/mySql.json");
settingsLdap = ldapSettings.ldapSettingsClass("conf/ldap.json");

intents = discord.Intents.default();
intents.members = True;

client = commands.Bot(command_prefix=settingsDiscord.commandPrefix, intents=intents);

#Load Logging Modules
moduleTextLogging = loggingModule.textLoggingClass(client, settingsMySql);
moduleVoiceLogging = loggingModule.voiceLoggingClass(client, settingsMySql);

#Load Cogs
client.add_cog(botManagement.botManagementClass(client));
client.add_cog(clubMenu.clubMenuClass(client, settingsMySql));
client.add_cog(extraStuff.extraStuffClass(client));
client.add_cog(privateCategories.privateCategoriesClass(client, settingsMySql));
client.add_cog(userBios.userBiosClass(client, settingsMySql));

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!');

client.run(settingsDiscord.token)
