import discord

def getRolesByName(guild):
    rolesByName = {};
    for role in guild.roles:
        if role.name not in rolesByName.keys():
            rolesByName[role.name] = [];
        rolesByName[role.name].append(role.id);
    return rolesByName;

def getRoleByName(guild, roleName):
    rolesByName = getRolesByName(guild);
    if roleName in rolesByName.keys():
        return rolesByName[roleName];
    else:
        return None;

def getUserIdsByRoleName(guild, roleName):
    roleIds =  getRoleByName(guild, roleName);
    userIds = [];
    for member in guild.members:
        for role in member.roles:
            if role.id in roleIds:
                userIds.append(member.id);
                break;
    return userIds;

def getUserIdsByRoleId(guild, roleId):
    userIds = [];
    for member in guild.members:
        for role in member.roles:
            if str(role.id) == str(roleId):
                userIds.append(member.id);
                break;
    return userIds;

def getMessageAttachments(message):
    attachmentUrls = [];
    for attachment in message.attachments:
        attachmentUrls.append(attachment.url);
    return attachmentUrls;

def getChannelIdsByName(guild, channelName):
    channelIds = [];
    for channel in guild.channels:
        if channel.name == channelName:
            channelIds.append(channel.id);
    return channelIds;

async def fetchChannelById(guild, channelId):
    targetChannels = await guild.fetch_channels();
    targetChannel = None;
    for currentChannel in targetChannels:
        if str(currentChannel.id) == str(channelId):
            targetChannel = currentChannel;
            break;
    return targetChannel;

def getUserRoleIds(ctx):
    roleIds = [];
    for role in ctx.message.author.roles:
        roleIds.append(role.id);
    return roleIds;
