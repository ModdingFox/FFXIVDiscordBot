from discord.ext import commands
from random import seed
from random import randint
import time

class extraStuffClass(commands.Cog, name='Random Junk'):
    def __init__(self, discordClient):
        self.discordClient = discordClient;
        
    @commands.command(brief="Solt Machine", description="Solt Machine")
    async def slotMachine(self, ctx, betAmmount):
        items = [":poop:", ":cherries:", ":cupcake:", ":pizza:", ":cookie:", ":fox:"];
        
        if int(betAmmount) <= 35:
            payoutMultiplier = 1;
        elif int(betAmmount) <= 65:
           payoutMultiplier = 2;
        elif int(betAmmount) <= 95:
           payoutMultiplier = 3;
        elif int(betAmmount) <= 125:
           payoutMultiplier = 4;
        
        payoutData = [];
        payoutData.append({ 0: {} });
        payoutData.append({ 1: { 1: { "SLOT1": [1] }, 2.5: { "SLOT1": [1], "SLOT2": [1] }, 3.5: { "SLOT1": [1], "SLOT2": [1], "SLOT3": [1] } } });
        payoutData.append({ 2: { 5: { "SLOT1": [2], "SLOT2": [2], "SLOT3": [2, 5] } } });
        payoutData.append({ 3: { 7: { "SLOT1": [3], "SLOT2": [3], "SLOT3": [3, 5] } } });
        payoutData.append({ 4: { 10: { "SLOT1": [4], "SLOT2": [4], "SLOT3": [4, 5] } } });
        payoutData.append({ 5: { 125: { "SLOT1": [5], "SLOT2": [5], "SLOT3": [5] } } });
        
        prizeString = "";
        
        for payoutItem in payoutData:
            for payoutItemKey in payoutItem.keys():
                for payoutItemRewardKey in payoutItem[payoutItemKey].keys():
                    payoutMatchString = "";
                    if "SLOT1" in payoutItem[payoutItemKey][payoutItemRewardKey]:
                        payoutMatchString += items[payoutItem[payoutItemKey][payoutItemRewardKey]["SLOT1"][0]];
                        if "SLOT2" in payoutItem[payoutItemKey][payoutItemRewardKey]:
                            payoutMatchString += items[payoutItem[payoutItemKey][payoutItemRewardKey]["SLOT2"][0]];
                            if "SLOT3" in payoutItem[payoutItemKey][payoutItemRewardKey]:
                                payoutMatchString += items[payoutItem[payoutItemKey][payoutItemRewardKey]["SLOT3"][0]];
                    payoutMatchString += " " + str(int(payoutItemRewardKey * payoutMultiplier)) + " cookies";
                    prizeString += payoutMatchString + "\n";
        
        seed(time.time());
        slot1 = randint(0, len(items) - 1);
        slot2 = randint(0, len(items) - 1);
        slot3 = randint(0, len(items) - 1);
        
        payoutAmmount = 0;
        
        for payoutItem in payoutData:
            for payoutItemKey in payoutItem.keys():
                for payoutItemRewardKey in payoutItem[payoutItemKey].keys():
                    if ("SLOT1" in payoutItem[payoutItemKey][payoutItemRewardKey] and slot1 in payoutItem[payoutItemKey][payoutItemRewardKey]["SLOT1"]
                        and "SLOT2" in payoutItem[payoutItemKey][payoutItemRewardKey] and slot2 in payoutItem[payoutItemKey][payoutItemRewardKey]["SLOT2"]
                        and "SLOT3" in payoutItem[payoutItemKey][payoutItemRewardKey] and slot3 in payoutItem[payoutItemKey][payoutItemRewardKey]["SLOT3"]
                    ):
                        payoutAmmount = int(payoutItemRewardKey * payoutMultiplier);
                    elif ("SLOT1" in payoutItem[payoutItemKey][payoutItemRewardKey] and slot1 in payoutItem[payoutItemKey][payoutItemRewardKey]["SLOT1"]
                        and "SLOT2" in payoutItem[payoutItemKey][payoutItemRewardKey] and slot2 in payoutItem[payoutItemKey][payoutItemRewardKey]["SLOT2"]
                        and "SLOT3" not in payoutItem[payoutItemKey][payoutItemRewardKey]
                    ):
                        payoutAmmount = int(payoutItemRewardKey * payoutMultiplier);
                    elif ("SLOT1" in payoutItem[payoutItemKey][payoutItemRewardKey] and slot1 in payoutItem[payoutItemKey][payoutItemRewardKey]["SLOT1"]
                        and "SLOT2" not in payoutItem[payoutItemKey][payoutItemRewardKey]
                        and "SLOT3" not in payoutItem[payoutItemKey][payoutItemRewardKey]
                    ):
                        payoutAmmount = int(payoutItemRewardKey * payoutMultiplier);
                
                if payoutAmmount is not 0:
                    break;
            
            if payoutAmmount is not 0:
                break;
        
        await ctx.send("{0}\n\n{1} {2} {3}\nYou won {4} cookies".format(prizeString, items[slot1], items[slot2], items[slot3], payoutAmmount));
