from discord.ext import commands
import pymysql.cursors

class clubMenuClass(commands.Cog, name='Club Menu'):
    def removeMenuItem(self, guildId, menuItem, menuType):
        result = False
        
        connection = pymysql.connect(host = self.settingsMySql.host, user = self.settingsMySql.user, password = self.settingsMySql.password, cursorclass=pymysql.cursors.DictCursor);
    	
        try:
            with connection.cursor() as cursor:
                sql = "DELETE FROM discord.menuItems WHERE guildId = %s AND menuItem = %s AND menuType = %s";
                cursor.execute(sql, (guildId, menuItem, menuType));
                connection.commit();
                result = True;
        finally:
                connection.close();
        
        return result;
    
    def addMenuItem(self, guildId, menuItem, itemCost, menuType):
        result = False;
        
        self.removeMenuItem(guildId, menuItem, menuType);
        
        connection = pymysql.connect(host = self.settingsMySql.host, user = self.settingsMySql.user, password = self.settingsMySql.password, cursorclass=pymysql.cursors.DictCursor);
    	
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO discord.menuItems (guildId, menuItem, itemCost, menuType) VALUES (%s, %s, %s, %s)";
                cursor.execute(sql, (guildId, menuItem, itemCost, menuType));
                connection.commit();
                result = True;
        finally:
                connection.close();
        
        return result;
    
    def getMenuItems(self, guildId, menuType):
        result = [];
        
        connection = pymysql.connect(host = self.settingsMySql.host, user = self.settingsMySql.user, password = self.settingsMySql.password, cursorclass=pymysql.cursors.DictCursor);
    	
        try:
            with connection.cursor() as cursor:
                sql = "SELECT menuItem, itemCost FROM discord.menuItems WHERE guildId = %s AND menuType = %s";
                cursor.execute(sql, (guildId, menuType));
                results = cursor.fetchall();
                for queryResult in results:
                    result.append(queryResult);
        finally:
                connection.close();
        
        return result;
    
    def initTables(self):
        result = False;
        
        connection = pymysql.connect(host = self.settingsMySql.host, user = self.settingsMySql.user, password = self.settingsMySql.password, cursorclass=pymysql.cursors.DictCursor);
        
        try:
            with connection.cursor() as cursor:
                cursor.execute("CREATE DATABASE IF NOT EXISTS discord COLLATE utf8mb4_unicode_ci");
                cursor.execute("CREATE TABLE IF NOT EXISTS discord.menuItems( guildId  TEXT NOT NULL, menuItem TEXT NOT NULL, itemCost INT  NOT NULL, menuType TEXT NOT NULL )");
                result = True;
        finally:
                connection.close();
        
        return result;
    
    def __init__(self, discordClient, settingsMySql):
        self.discordClient = discordClient;
        self.settingsMySql = settingsMySql;
        self.initTables();
        
    @commands.command(brief="Creates a new drink menu item or changes an existing ones price", description="Creates a new drink menu item or changes an existing ones price")
    async def addDrinkItem(self, ctx, itemName, cost):
        if self.addMenuItem(ctx.guild.id, str(itemName), int(cost), "drinkMenu"):
            await ctx.send("Added Drink\nItem: {0}\nCost: {1}".format(itemName, cost));
        else:
            await ctx.send("Failed To Add Drink\nItem: {0}\nCost: {1}".format(itemName, cost));
    
    @commands.command(brief="Creates a new food menu item or changes an existing ones price", description="Creates a new food menu item or changes an existing ones price")
    async def addFoodItem(self, ctx, itemName, cost):
        if self.addMenuItem(ctx.guild.id, str(itemName), int(cost), "foodMenu"):
            await ctx.send("Added Food\nItem: {0}\nCost: {1}".format(itemName, cost));
        else:
            await ctx.send("Failed To Add Food\nItem: {0}\nCost: {1}".format(itemName, cost));
    
    @commands.command(brief="Removes a drink menu item", description="Removes a drink menu item")
    async def removeDrinkItem(self, ctx, itemName):
        if self.removeMenuItem(ctx.guild.id, str(itemName), "drinkMenu"):
            await ctx.send("Removed Drink: {0}".format(itemName));
        else:
            await ctx.send("Failed To Remove Drink: {0}".format(itemName));
    
    @commands.command(brief="Removes a food menu item", description="Removes a food menu item")
    async def removeFoodItem(self, ctx, itemName):
        if self.removeMenuItem(ctx.guild.id, str(itemName), "foodMenu"):
            await ctx.send("Removed Food: {0}".format(itemName));
        else:
            await ctx.send("Failed To Remove Food: {0}".format(itemName));
    
    @commands.command(brief="Gets the current drink menu", description="Gets the current drink menu")
    async def drinkMenu(self, ctx):
        message = "--Drink Menu--\n";
        for item in self.getMenuItems(ctx.guild.id, "drinkMenu"):
            message += "{0} - {1} Gil\n".format(item["menuItem"], item["itemCost"]);
        await ctx.send(message);
    
    @commands.command(brief="Gets the current food menu", description="Gets the current food menu")
    async def foodMenu(self, ctx):
        message = "--Food Menu--\n";
        for item in self.getMenuItems(ctx.guild.id, "foodMenu"):
            message += "{0} - {1} Gil\n".format(item["menuItem"], item["itemCost"]);
        await ctx.send(message);
