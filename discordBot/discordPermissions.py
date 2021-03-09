import discord

def checkPermissions(ctx):
    if ctx.guild.owner_id == ctx.author.id:
        return True;
    else:
        return False;
