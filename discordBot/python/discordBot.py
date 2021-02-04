#!/bin/python3

#yum install python3-pip.noarch python3-devel.x86_64
#pip-3 install discord
#pip-3 install python-dotenv
#pip-3 install PyMySQL
#pip-3 install requests
#pip-3 install python-ldap

import discord
import pymysql.cursors
import re
import requests
import json
import ldap
from random import seed
from random import randint
import time
import datetime
from bs4 import BeautifulSoup

mysqlHost = 'localhost'
mySqlUser = 'root'
mySqlPassword = ''

ldapHost = 'ldap://127.0.0.1'
ldapDN = 'dc=foxtek,dc=us'
ldapUser = 'cn=ldapadm,' + ldapDN
ldapPassword = ''
ldapSiteManagementGroup = "cn=SiteManagement,ou=Group," + ldapDN
ldapMemberGroup = "cn=Members,ou=Group,"+ ldapDN
ldapBanGroup = "cn=Banned,ou=Group," + ldapDN

def validateDiscordUser(discordId):
    global mysqlHost
    global mySqlUser
    global mySqlPassword
    global ldapHost
    global ldapDN
    global ldapUser
    global ldapPassword
    global ldapMemberGroup
    global ldapBanGroup
    result = { "Authorized": False, 'userDN': "", "userUid": "", "userGroups": [] }

    connection = pymysql.connect(host = mysqlHost, user = mySqlUser, password = mySqlPassword, cursorclass=pymysql.cursors.DictCursor)
    ldapconn = ldap.initialize(ldapHost)
    
    userCN = None
    
    try:
        with connection.cursor() as cursor:
            sql = "SELECT userCN FROM userAccountData.discordLink WHERE discordId = %s"
            cursor.execute(sql, discordId)
            sqlResult = cursor.fetchone()
            if sqlResult is not None:
                userCN = sqlResult['userCN']
    finally:
        connection.close()
    
    if userCN == None:
        return result
    
    try:
        ldapconn = ldap.initialize(ldapHost)
        ldapconn.protocol_version = ldap.VERSION3
        ldapconn.simple_bind_s(ldapUser, ldapPassword)
        
        ldapResult = ldapconn.search_s("ou=People," + ldapDN, ldap.SCOPE_SUBTREE, "(cn=" + userCN + ")", ['uid'])
        
        result['userDN'] = ldapResult[0][0]
        result['userUid'] = ldapResult[0][1]['uid'][0].decode('utf-8')

        ldapResult = ldapconn.search_s("ou=Group," + ldapDN, ldap.SCOPE_SUBTREE, "(member=" + result['userDN'] + ")", ['DN'])
        
        for userGroup in ldapResult:
            result['userGroups'].append(userGroup[0])
        
        if (ldapMemberGroup in result['userGroups']) and (ldapBanGroup not in result['userGroups']):
            result['Authorized'] = True
    except Exception as e:
        print(e)
    finally:
        ldapconn.unbind_s()
    
    return result

def logMessage(authorId, channelId, messageId, messageContent, attachmentUrls):
    global mysqlHost
    global mySqlUser
    global mySqlPassword
    result = False
    
    connection = pymysql.connect(host = mysqlHost, user = mySqlUser, password = mySqlPassword, cursorclass=pymysql.cursors.DictCursor)
    
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO discord.textChatLog (authorId, channelId, messageId, messageContent, attachmentUrls) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (authorId, channelId, messageId, messageContent, ", ".join(attachmentUrls)))
            connection.commit()
            result = True
    
    finally:
            connection.close()
    
    return result

def insertVoiceChatLog(discordUserId, userName, channelId, channelName):
    global mysqlHost
    global mySqlUser
    global mySqlPassword
    result = False
    
    connection = pymysql.connect(host = mysqlHost, user = mySqlUser, password = mySqlPassword, cursorclass=pymysql.cursors.DictCursor)
    
    try:
        with connection.cursor() as cursor:
            if channelId is not None:
                sql = "INSERT INTO discord.voiceChatLog (discordUserId, userName, channelId, channelName) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (discordUserId, userName, channelId, channelName))
            else:
                sql = "INSERT INTO discord.voiceChatLog (discordUserId, userName, channelName) VALUES (%s, %s, %s)"
                cursor.execute(sql, (discordUserId, userName, channelName))
            
            connection.commit()
            result = True
    
    finally:
            connection.close()
    
    return result

def updateVoiceChatLog(discordId):
    global mysqlHost
    global mySqlUser
    global mySqlPassword
    result = False
    
    connection = pymysql.connect(host = mysqlHost, user = mySqlUser, password = mySqlPassword, cursorclass=pymysql.cursors.DictCursor)
    
    try:
        with connection.cursor() as cursor:
            sql = "UPDATE discord.voiceChatLog SET leaveChannelTimestamp = now() WHERE discordUserId = %s AND leaveChannelTimestamp is NULL"
            cursor.execute(sql, (discordId))
            connection.commit()
            result = True
    
    finally:
            connection.close()
    
    return result

discordClient=discord.Client()
discordChannelId="807001358682685461"
discordToken=''
discordChannels=["club-spectrem-bot"]

baseUrl = "https://127.0.0.1/Rest/"

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    global ldapSiteManagementGroup
    
    attachmentUrls = []
    for attachment in message.attachments:
        attachmentUrls.append(attachment.url)
    logMessage(message.author.id, message.channel.id, message.id, message.content, attachmentUrls)
    
    if str(message.channel) in discordChannels:
        if str(client.user.id) != str(message.author.id):
            if message.content == "!help":
                response = "General Command Listing:\n"
                response += "    !murderTheBot - Halts the bots server process\n"
                response += "    !register (registration code) - Links user discord to FC website\n"
                await message.channel.send(response)
            elif message.content == "!murderTheBot":
               if ldapSiteManagementGroup in validateDiscordUser(message.author.id)['userGroups']:
                   await message.channel.send("Bot killed by <@!{0}>".format(message.author.id))
                   exit(0)
               else:
                   await message.channel.send("<@!{0}> is not allowed to kill the bot".format(message.author.id))
            elif message.content.startswith("!register"):
                commandMatch = re.search("^!register ([0-9a-z]{8}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{12})$", message.content)
                if commandMatch is not None:
                    payload = {"Method": "registerDiscordLinkToken", "JSON": '{ "discordLinkToken": "' + str(commandMatch.group(1)) + '", "discordId": "' + str(message.author.id) + '"}' }
                    requestResult = requests.post(baseUrl + "discordLink.php", data = payload, verify = False)
                    requestResultJson = json.loads(requestResult.text)
                    if requestResultJson['status'] == "Success":
                        await message.channel.send("User account registered")
                    elif requestResultJson['status'] == "Warning":
                        await message.channel.send(requestResultJson['warning'])
                    elif requestResultJson['status'] == "Error":
                        await message.channel.send(requestResultJson['error'])
                else:
                    await message.channel.send("Registration code does not match the expected format")

@client.event
async def on_voice_state_update(member, before, after):
    userNameAndNick = "{0}({1})".format(member.name, member.nick)
    
    updateVoiceChatLog(member.id)
    
    if after.channel is not None:
        insertVoiceChatLog(member.id, userNameAndNick, after.channel.id, after.channel.name)
    else:
        insertVoiceChatLog(member.id, userNameAndNick, None, "None")

client.run(discordToken)
