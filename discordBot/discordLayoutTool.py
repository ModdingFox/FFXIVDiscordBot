import discordUtils

import discord
from discord.ext import commands
from io import BytesIO

import json;
from json import JSONDecodeError 

class discordLayoutToolClass(commands.Cog, name='Discord Layout Tool'):
    def __init__(self, discordClient):
        self.discordClient = discordClient;

    def assetToHashMap(self, asset):
        assetAttributes = {};
        if asset is not None:
            assetAttributes['key'] = asset.key;
            assetAttributes['url'] = asset.url;
        return assetAttributes;

    def colourToHashMap(self, colour):
        colourAttributes = {};
        if colour is not None:
            colourAttributes['b'] = colour.b;
            colourAttributes['g'] = colour.g;
            colourAttributes['r'] = colour.r;
            colourAttributes['value'] = colour.value;
        return colourAttributes;

    def permissionsToHashMap(self, permissions):
        permissioneAttributes = {};
        if permissions is not None:
            permissioneAttributes['add_reactions'] = permissions.add_reactions;
            permissioneAttributes['administrator'] = permissions.administrator;
            permissioneAttributes['attach_files'] = permissions.attach_files;
            permissioneAttributes['ban_members'] = permissions.ban_members;
            permissioneAttributes['change_nickname'] = permissions.change_nickname;
            permissioneAttributes['connect'] = permissions.connect;
            permissioneAttributes['create_instant_invite'] = permissions.create_instant_invite;
            permissioneAttributes['create_private_threads'] = permissions.create_private_threads;
            permissioneAttributes['create_public_threads'] = permissions.create_public_threads;
            permissioneAttributes['deafen_members'] = permissions.deafen_members;
            permissioneAttributes['embed_links'] = permissions.embed_links;
            permissioneAttributes['external_emojis'] = permissions.external_emojis;
            permissioneAttributes['external_stickers'] = permissions.external_stickers;
            permissioneAttributes['kick_members'] = permissions.kick_members;
            permissioneAttributes['manage_channels'] = permissions.manage_channels;
            permissioneAttributes['manage_emojis'] = permissions.manage_emojis;
            permissioneAttributes['manage_emojis_and_stickers'] = permissions.manage_emojis_and_stickers;
            permissioneAttributes['manage_events'] = permissions.manage_events;
            permissioneAttributes['manage_guild'] = permissions.manage_guild;
            permissioneAttributes['manage_messages'] = permissions.manage_messages;
            permissioneAttributes['manage_nicknames'] = permissions.manage_nicknames;
            permissioneAttributes['manage_permissions'] = permissions.manage_permissions;
            permissioneAttributes['manage_roles'] = permissions.manage_roles;
            permissioneAttributes['manage_threads'] = permissions.manage_threads;
            permissioneAttributes['manage_webhooks'] = permissions.manage_webhooks;
            permissioneAttributes['mention_everyone'] = permissions.mention_everyone;
            permissioneAttributes['moderate_members'] = permissions.moderate_members;
            permissioneAttributes['move_members'] = permissions.move_members;
            permissioneAttributes['mute_members'] = permissions.mute_members;
            permissioneAttributes['priority_speaker'] = permissions.priority_speaker;
            permissioneAttributes['read_message_history'] = permissions.read_message_history;
            permissioneAttributes['read_messages'] = permissions.read_messages;
            permissioneAttributes['request_to_speak'] = permissions.request_to_speak;
            permissioneAttributes['send_messages'] = permissions.send_messages;
            permissioneAttributes['send_messages_in_threads'] = permissions.send_messages_in_threads;
            permissioneAttributes['send_tts_messages'] = permissions.send_tts_messages;
            permissioneAttributes['speak'] = permissions.speak;
            permissioneAttributes['stream'] = permissions.stream;
            permissioneAttributes['use_application_commands'] = permissions.use_application_commands;
            permissioneAttributes['use_embedded_activities'] = permissions.use_embedded_activities;
            permissioneAttributes['use_external_emojis'] = permissions.use_external_emojis;
            permissioneAttributes['use_external_stickers'] = permissions.use_external_stickers;
            permissioneAttributes['use_voice_activation'] = permissions.use_voice_activation;
            permissioneAttributes['value'] = permissions.value;
            permissioneAttributes['view_audit_log'] = permissions.view_audit_log;
            permissioneAttributes['view_channel'] = permissions.view_channel;
            permissioneAttributes['view_guild_insights'] = permissions.view_guild_insights;
        return permissioneAttributes;

    def permissionOverwriteToHashMap(self, permissionOverwrite):
        permissionOverwriteAttributes = {};
        if permissionOverwrite is not None:
            allow = permissionOverwrite.pair()[0];
            deny  = permissionOverwrite.pair()[1];
            permissionOverwriteAttributes['allow'] = self.permissionsToHashMap(allow);
            permissionOverwriteAttributes['deny'] = self.permissionsToHashMap(deny);
        return permissionOverwriteAttributes;

    def overwritesToHashMap(self, overwrites):
        overwritesData = {};
        if overwrites is not None:
            for overwrite in overwrites.keys():
                overwritesData[overwrite.name] = self.permissionOverwriteToHashMap(overwrites[overwrite]);
        return overwritesData;

    def roleToHashMap(self, role):
        roleAttributes = {};
        roleAttributes['color'] = self.colourToHashMap(role.color);
        roleAttributes['colour'] = self.colourToHashMap(role.colour);
        ##roleAttributes['created_at'] = role.created_at; <- Env specific dont need for this
        #roleAttributes['display_icon'] = role.display_icon; <- Dont really know if we care about this enough and im lazy
        ##roleAttributes['guild'] = role.guild; <- Env specific dont need for this
        roleAttributes['hoist'] = role.hoist;
        roleAttributes['icon'] = self.assetToHashMap(role.icon);
        #roleAttributes['id'] = role.id;
        roleAttributes['managed'] = role.managed;
        ##roleAttributes['members'] = role.members; <- Env specific dont need for this
        #roleAttributes['mention'] = role.mention;
        roleAttributes['mentionable'] = role.mentionable;
        roleAttributes['name'] = role.name;
        roleAttributes['permissions'] = self.permissionsToHashMap(role.permissions);
        roleAttributes['position'] = role.position;
        ##roleAttributes['tags'] = role.tags; <- Dont really know if we care about this enough and im lazy
        roleAttributes['unicode_emoji'] = role.unicode_emoji;
        return roleAttributes;

    def rolesToHashMap(self, roles):
        roleData = {};
        for role in roles:
            roleData[role.name] = self.roleToHashMap(role);
        return roleData;

    def stageChannelToHashMap(self, stageChannel):
        stageChannelAttributes = {};
        if stageChannel is not None:
            stageChannelAttributes['bitrate'] = stageChannel.bitrate;
            #stageChannelAttributes['category'] = stageChannel.category;
            #stageChannelAttributes['category_id'] = stageChannel.category_id;
            #stageChannelAttributes['changed_roles'] = stageChannel.changed_roles;
            #stageChannelAttributes['created_at'] = stageChannel.created_at;
            #stageChannelAttributes['guild'] = stageChannel.guild;
            #stageChannelAttributes['id'] = stageChannel.id;
            #stageChannelAttributes['instance'] = stageChannel.instance;
            #stageChannelAttributes['jump_url'] = stageChannel.jump_url;
            #stageChannelAttributes['listeners'] = stageChannel.listeners;
            #stageChannelAttributes['members'] = stageChannel.members;
            #stageChannelAttributes['mention'] = stageChannel.mention;
            #stageChannelAttributes['moderators'] = stageChannel.moderators;
            stageChannelAttributes['name'] = stageChannel.name;
            stageChannelAttributes['nsfw'] = stageChannel.nsfw;
            stageChannelAttributes['overwrites'] = self.overwritesToHashMap(stageChannel.overwrites);
            stageChannelAttributes['permissions_synced'] = stageChannel.permissions_synced;
            stageChannelAttributes['position'] = stageChannel.position;
            #stageChannelAttributes['requesting_to_speak'] = stageChannel.requesting_to_speak;
            stageChannelAttributes['rtc_region'] = stageChannel.rtc_region;
            #stageChannelAttributes['scheduled_events'] = stageChannel.scheduled_events;
            #stageChannelAttributes['speakers'] = stageChannel.speakers;
            stageChannelAttributes['topic'] = stageChannel.topic;
            stageChannelAttributes['type'] = stageChannel.type;
            stageChannelAttributes['user_limit'] = stageChannel.user_limit;
            #stageChannelAttributes['video_quality_mode'] = stageChannel.video_quality_mode;
            #stageChannelAttributes['voice_states'] = stageChannel.voice_states;
        return stageChannelAttributes;

    def stageChannelsToHashMap(self, stageChannels):
        stageChannelsData = {};
        for stageChannel in stageChannels:
            stageChannelsData[stageChannel.name] = self.stageChannelToHashMap(stageChannel);
        return stageChannelsData;

    def textChannelToHashMap(self, textChannel):
        textChannelAttributes = {};
        if textChannel is not None:
            #textChannelAttributes['category'] = textChannel.category;
            #textChannelAttributes['category_id'] = textChannel.category_id;
            #textChannelAttributes['changed_roles'] = textChannel.changed_roles;
            #textChannelAttributes['created_at'] = textChannel.created_at;
            textChannelAttributes['default_auto_archive_duration'] = textChannel.default_auto_archive_duration;
            #textChannelAttributes['guild'] = textChannel.guild;
            #textChannelAttributes['id'] = textChannel.id;
            #textChannelAttributes['jump_url'] = textChannel.jump_url;
            #textChannelAttributes['last_message'] = textChannel.last_message;
            #textChannelAttributes['last_message_id'] = textChannel.last_message_id;
            #textChannelAttributes['members'] = textChannel.members;
            #textChannelAttributes['mention'] = textChannel.mention;
            textChannelAttributes['name'] = textChannel.name;
            textChannelAttributes['nsfw'] = textChannel.nsfw;
            textChannelAttributes['overwrites'] = self.overwritesToHashMap(textChannel.overwrites);
            textChannelAttributes['permissions_synced'] = textChannel.permissions_synced;
            textChannelAttributes['position'] = textChannel.position;
            textChannelAttributes['slowmode_delay'] = textChannel.slowmode_delay;
            #textChannelAttributes['threads'] = textChannel.threads;
            textChannelAttributes['topic'] = textChannel.topic;
            textChannelAttributes['type'] = textChannel.type;
        return textChannelAttributes;

    def textChannelsToHashMap(self, textChannels):
        textChannelsData = {};
        for textChannel in textChannels:
            textChannelsData[textChannel.name] = self.textChannelToHashMap(textChannel);
        return textChannelsData;

    def voiceChannelToHashMap(self, voiceChannel):
        voiceChannelAttributes = {};
        if voiceChannel is not None:
            voiceChannelAttributes['bitrate'] = voiceChannel.bitrate;
            #voiceChannelAttributes['category'] = voiceChannel.category;
            #voiceChannelAttributes['category_id'] = voiceChannel.category_id;
            #voiceChannelAttributes['changed_roles'] = voiceChannel.changed_roles;
            #voiceChannelAttributes['created_at'] = voiceChannel.created_at;
            #voiceChannelAttributes['guild'] = voiceChannel.guild;
            #voiceChannelAttributes['id'] = voiceChannel.id;
            #voiceChannelAttributes['jump_url'] = voiceChannel.jump_url;
            #voiceChannelAttributes['last_message'] = voiceChannel.last_message;
            #voiceChannelAttributes['last_message_id'] = voiceChannel.last_message_id;
            #voiceChannelAttributes['members'] = voiceChannel.members;
            #voiceChannelAttributes['mention'] = voiceChannel.mention;
            voiceChannelAttributes['name'] = voiceChannel.name;
            voiceChannelAttributes['nsfw'] = voiceChannel.nsfw;
            voiceChannelAttributes['overwrites'] = self.overwritesToHashMap(voiceChannel.overwrites);
            voiceChannelAttributes['permissions_synced'] = voiceChannel.permissions_synced;
            voiceChannelAttributes['position'] = voiceChannel.position;
            voiceChannelAttributes['rtc_region'] = voiceChannel.rtc_region;
            #voiceChannelAttributes['scheduled_events'] = voiceChannel.scheduled_events;
            voiceChannelAttributes['type'] = voiceChannel.type;
            voiceChannelAttributes['user_limit'] = voiceChannel.user_limit;
            #voiceChannelAttributes['video_quality_mode'] = voiceChannel.video_quality_mode;
            #voiceChannelAttributes['voice_states'] = voiceChannel.voice_states;
        return voiceChannelAttributes;

    def voiceChannelsToHashMap(self, voiceChannels):
        voiceChannelsData = {};
        for voiceChannel in voiceChannels:
            voiceChannelsData[voiceChannel.name] = self.voiceChannelToHashMap(voiceChannel);
        return voiceChannelsData;

    def categoryToHashMap(self, category):
        categoryAttributes = {};
        if category is not None:
            #categoryAttributes['category'] = category.category;
            #categoryAttributes['changed_roles'] = category.changed_roles;
            #categoryAttributes['channels'] = category.channels;
            #categoryAttributes['created_at'] = category.created_at;
            #categoryAttributes['guild'] = category.guild;
            #categoryAttributes['id'] = category.id;
            #ategoryAttributes['jump_url'] = category.jump_url;
            #ategoryAttributes['mention'] = category.mention;
            categoryAttributes['name'] = category.name;
            categoryAttributes['nsfw'] = category.nsfw;
            categoryAttributes['overwrites'] = self.overwritesToHashMap(category.overwrites);
            categoryAttributes['permissions_synced'] = category.permissions_synced;
            categoryAttributes['position'] = category.position;
            categoryAttributes['stage_channels'] = self.stageChannelsToHashMap(category.stage_channels);
            categoryAttributes['text_channels'] = self.textChannelsToHashMap(category.text_channels);
            categoryAttributes['type'] = category.type;
            categoryAttributes['voice_channels'] = self.voiceChannelsToHashMap(category.voice_channels);
        return categoryAttributes;

    def categoriesToHashMap(self, categories):
        categoriesData = {};
        for category in categories:
            categoriesData[category.name] = self.categoryToHashMap(category);
        return categoriesData;

    async def hashMapToRoles(self, ctx, roleData):
        topRole = ctx.guild.get_member(ctx.me.id).top_role;
        currentRoles = discordUtils.getRolesByName(ctx.guild);
        currentRoleKeys = currentRoles.keys();
        desiredRoleKeys = roleData.keys();
        createRoles = list(set(desiredRoleKeys).difference(currentRoleKeys));
        deleteRoles = list(set(currentRoleKeys).difference(desiredRoleKeys));
        for deleteRole in deleteRoles:
            if deleteRole != topRole.name:
                for currentRoleId in currentRoles[deleteRole]:
                    currentRole = ctx.guild.get_role(currentRoleId);
                    await currentRole.delete();
        for createRole in createRoles:
            if createRole != topRole.name:
                await ctx.guild.create_role(
                    name = roleData[createRole]['name'],
                    permissions = discord.Permissions(permissions = roleData[createRole]['permissions']['value']),
                    colour  = discord.Colour(roleData[createRole]['colour']['value']),
                    hoist = roleData[createRole]['hoist'],
                    mentionable = roleData[createRole]['mentionable'],
                    reason = "Created by loadServerLayout triggered by {0} - {1}".format(ctx.message.author.name, ctx.message.author.id)
                );
        for currentRoleName in roleData.keys():
            if currentRoleName != topRole.name:
                currentRoleIds = discordUtils.getRoleByName(ctx.guild, currentRoleName);
                if currentRoleIds is None:
                    await ctx.send("Could not find role {0}".format(currentRoleName));
                elif len(currentRoleIds) != 1:
                    await ctx.send("Found duplicate for role {0}".format(currentRoleName));
                else:
                    currentRole = ctx.guild.get_role(currentRoleIds[0]);
                    if roleData[currentRoleName]['position'] == 0:
                        await currentRole.edit(
                            name = roleData[currentRoleName]['name'],
                            permissions = discord.Permissions(permissions = roleData[currentRoleName]['permissions']['value']),
                            colour  = discord.Colour(roleData[currentRoleName]['colour']['value']),
                            hoist = roleData[currentRoleName]['hoist'],
                            mentionable = roleData[currentRoleName]['mentionable'],
                            reason = "Updated by loadServerLayout triggered by {0} - {1}".format(ctx.message.author.name, ctx.message.author.id)
                        );
                    else:
                        await currentRole.edit(
                            name = roleData[currentRoleName]['name'],
                            permissions = discord.Permissions(permissions = roleData[currentRoleName]['permissions']['value']),
                            colour  = discord.Colour(roleData[currentRoleName]['colour']['value']),
                            hoist = roleData[currentRoleName]['hoist'],
                            mentionable = roleData[currentRoleName]['mentionable'],
                            position = roleData[currentRoleName]['position'],
                            reason = "Updated by loadServerLayout triggered by {0} - {1}".format(ctx.message.author.name, ctx.message.author.id)
                        );

    async def deleteChannels(self, channels):
        for channel in channels:
            await channel.delete();

    async def hashMapToOverwrites(self, ctx, overwritesData):
        overwrites = {};
        for currentOverwriteKey in overwritesData.keys():
            currentRoleIds = discordUtils.getRoleByName(ctx.guild, currentOverwriteKey);
            if currentRoleIds is None:
                await ctx.send("Could not find role {0}".format(currentOverwriteKey));
            elif len(currentRoleIds) != 1:
                await ctx.send("Found duplicate for role {0}".format(currentOverwriteKey));
            else:
                currentRole = ctx.guild.get_role(currentRoleIds[0]);
                allow = discord.Permissions(permissions = overwritesData[currentOverwriteKey]['allow']['value']);
                deny = discord.Permissions(permissions = overwritesData[currentOverwriteKey]['deny']['value']);
                overwrites[currentRole] = discord.PermissionOverwrite.from_pair(allow, deny);
        return overwrites;

    async def hashMapsToChannels(self, ctx, category, stageChannels, textChannels, voiceChannels):
        currentChannels = category.channels;
        currentChannelsKeys = list(map(lambda element: element.name, currentChannels));
        desiredChannelsKeys = list(stageChannels.keys()) + list(textChannels.keys()) + list(voiceChannels.keys());
        createChannels = list(set(desiredChannelsKeys).difference(currentChannelsKeys));
        deleteChannels = list(set(currentChannelsKeys).difference(desiredChannelsKeys));
        for deleteChannel in deleteChannels:
            for currentChannel in currentChannels:
                if currentChannel.name == deleteChannel:
                    await currentChannel.delete();
        for createChannel in createChannels:
            if createChannel in stageChannels.keys():
                await category.create_stage_channel(
                    name = stageChannels[createChannel]['name'],
                    topic = stageChannels[createChannel]['topic'],
                    overwrites = await self.hashMapToOverwrites(ctx, stageChannels[createChannel]['overwrites']),
                    reason = "Created by loadServerLayout triggered by {0} - {1}"
                );
            elif createChannel in textChannels.keys():
                await category.create_text_channel(
                    name = textChannels[createChannel]['name'],
                    overwrites = await self.hashMapToOverwrites(ctx, textChannels[createChannel]['overwrites']),
                    topic = textChannels[createChannel]['topic'],
                    slowmode_delay = textChannels[createChannel]['slowmode_delay'],
                    nsfw = textChannels[createChannel]['nsfw'],
                    default_auto_archive_duration = textChannels[createChannel]['default_auto_archive_duration'],
                    reason = "Created by loadServerLayout triggered by {0} - {1}"
                );
            elif createChannel in voiceChannels.keys():
                await category.create_voice_channel(
                    name = voiceChannels[createChannel]['name'],
                    overwrites = await self.hashMapToOverwrites(ctx, voiceChannels[createChannel]['overwrites']),
                    bitrate = voiceChannels[createChannel]['bitrate'],
                    user_limit = voiceChannels[createChannel]['user_limit'],
                    rtc_region = voiceChannels[createChannel]['rtc_region'],
                    reason = "Created by loadServerLayout triggered by {0} - {1}"
                );
            else:
                await ctx.send("Channel {0} is not of type stageChannel, textChannel, or voiceChannel".format(createChannel));
        for currentStageChannel in category.stage_channels:
            await currentStageChannel.edit(
                 name = stageChannels[currentStageChannel.name]['name'],
                 position = stageChannels[currentStageChannel.name]['position'],
                 overwrites = await self.hashMapToOverwrites(ctx, stageChannels[currentStageChannel.name]['overwrites']),
                 reason = "Updated by loadServerLayout triggered by {0} - {1}"
            );
        for currentTextChannel in category.text_channels:
            await currentTextChannel.edit(
                 name = textChannels[currentTextChannel.name]['name'],
                 topic = textChannels[currentTextChannel.name]['topic'],
                 position = textChannels[currentTextChannel.name]['position'],
                 nsfw = textChannels[currentTextChannel.name]['nsfw'],
                 slowmode_delay = textChannels[currentTextChannel.name]['slowmode_delay'],
                 overwrites = await self.hashMapToOverwrites(ctx, textChannels[currentTextChannel.name]['overwrites']),
                 default_auto_archive_duration = textChannels[currentTextChannel.name]['default_auto_archive_duration'],
                 reason = "Updated by loadServerLayout triggered by {0} - {1}"
            );
        for currentVoiceChannel in category.voice_channels:
            await currentVoiceChannel.edit(
                 name = voiceChannels[currentVoiceChannel.name]['name'],
                 bitrate = voiceChannels[currentVoiceChannel.name]['bitrate'],
                 nsfw = voiceChannels[currentVoiceChannel.name]['nsfw'],
                 user_limit = voiceChannels[currentVoiceChannel.name]['user_limit'],
                 position = voiceChannels[currentVoiceChannel.name]['position'],
                 overwrites = await self.hashMapToOverwrites(ctx, voiceChannels[currentVoiceChannel.name]['overwrites']),
                 rtc_region = voiceChannels[currentVoiceChannel.name]['rtc_region'],
                 reason = "Updated by loadServerLayout triggered by {0} - {1}"
            );

    async def hashMapToCategories(self, ctx, categoriesData):
        currentCategories = ctx.guild.categories;
        currentCategoriesKeys = list(map(lambda element: element.name, currentCategories));
        desiredCategoriesKeys = categoriesData.keys();
        createCategories = list(set(desiredCategoriesKeys).difference(currentCategoriesKeys));
        deleteCategories = list(set(currentCategoriesKeys).difference(desiredCategoriesKeys));
        for deleteCategory in deleteCategories:
            for currentCategory in currentCategories:
                if currentCategory.name == deleteCategory:
                    await self.deleteChannels(currentCategory.channels);
                    await currentCategory.delete();
        for createCategory in createCategories:
            await ctx.guild.create_category(
                name = categoriesData[createCategory]['name'],
                reason = "Created by loadServerLayout triggered by {0} - {1}"
            );
        currentCategories = ctx.guild.categories;
        for currentCategory in currentCategories:
            await currentCategory.edit(
                name = categoriesData[currentCategory.name]['name'],
                overwrites = await self.hashMapToOverwrites(ctx, categoriesData[currentCategory.name]['overwrites']),
                position = categoriesData[currentCategory.name]['position'],
                reason = "Updated by loadServerLayout triggered by {0} - {1}"
            );
            await self.hashMapsToChannels(
                ctx,
                currentCategory,
                categoriesData[currentCategory.name]['stage_channels'],
                categoriesData[currentCategory.name]['text_channels'],
                categoriesData[currentCategory.name]['voice_channels']
            );

    @commands.command(brief="Save Server Layout", description="Save server layout to json")
    async def saveServerLayoutToJSON(self, ctx):
        serverData = {};
        categoriesData = self.categoriesToHashMap(ctx.guild.categories);
        roleData = self.rolesToHashMap(ctx.guild.roles);
        serverData['categoriesData'] = categoriesData;
        serverData['roleData'] = roleData;
        serverLayoutJSON = json.dumps(serverData, indent=4);
        serverLayoutBytes = bytes(serverLayoutJSON, "utf-8");
        await ctx.send("Server Layout JSON", file=discord.File(BytesIO(serverLayoutBytes), "serverLayout.json"));

    @commands.command(brief="Load Server Layout", description="Load server layout from json")
    async def loadServerLayoutFromJSON(self, ctx):
        if len(ctx.message.attachments) == 1:
            serverDataAttachment = await ctx.message.attachments[0].read();
            try:
                serverData = json.loads(serverDataAttachment);
                if "roleData" in serverData.keys():
                     await self.hashMapToRoles(ctx, serverData["roleData"]);
                else:
                    await ctx.send("No roleData. Skipping.");
                if "categoriesData" in serverData.keys():
                    await self.hashMapToCategories(ctx, serverData["categoriesData"]);
                else:
                    await ctx.send("No categoriesData. Skipping.");
                await ctx.send("Server layout update complete");
            except JSONDecodeError as e:
                await ctx.send("Data recieved is not json");
        else:
            await ctx.send("Must attach a single configuration payload file");

