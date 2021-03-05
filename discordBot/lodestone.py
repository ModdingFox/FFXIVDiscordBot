import discord
from discord.ext import commands
import re
import requests
from bs4 import BeautifulSoup

class lodestoneClass(commands.Cog, name='Lodestone'):
    def getLodestonePlayerListing(self, world, firstName, lastName):
        queryString = "?q=" + firstName + "+" + lastName;
        
        if world is not None and world != "All":
            queryString += "&worldname=" + world;
        elif world == "All":
            pass;
        
        requestResult = requests.get(self.lodeStoneCharacterSearchUrl + queryString, verify = False);
        soup = BeautifulSoup(requestResult.text, 'html.parser');
        
        characters = [];
        searchResults = soup.body.findAll("div", {"class": "entry"});
        
        for entry in searchResults:
            character = entry.find("a", {"class": "entry__link"});
            freecompany = entry.find("a", {"class": "entry__freecompany__link"});
            
            characterData = {};
            
            if character is not None:
                characterInfo = character.find("div", {"class": "entry__box entry__box--world"});
                characterData['characterLink'] = self.lodeStoneBaseUrl + character['href'];
                characterData['characterName'] = characterInfo.find("p", {"class": "entry__name"}).getText().replace(u'\xa0', u' ');
                dataCenterAndWorld = re.search("^([a-zA-Z]+) \(([a-zA-Z]+)\)$", characterInfo.find("p", {"class": "entry__world"}).getText().replace(u'\xa0', u' '));
                characterData['characterWorld'] = dataCenterAndWorld.group(1);
                characterData['characterDataCenter'] = dataCenterAndWorld.group(2);
            
            if freecompany is not None:
                characterData['characterGuildLink'] = self.lodeStoneBaseUrl + freecompany['href'];
                characterData['characterGuild'] = freecompany.find("span").getText().replace(u'\xa0', u' ');
            
            if len(characterData) > 0 and characterData['characterName'] == firstName + " " + lastName:
                characters.append(characterData);
            
        return characters;
    
    def generateCharacterBriefText(self, characterDataIn):
        result = "";
        
        if characterDataIn['characterName'] is not None:
            result += "    Name: " + characterDataIn['characterName'] + "\n";
        if characterDataIn['characterDataCenter'] is not None:
            result += "    Datacenter: " + characterDataIn['characterDataCenter'] + "\n";
        if characterDataIn['characterWorld'] is not None:
            result += "    World: " + characterDataIn['characterWorld'] + "\n";
        if characterDataIn['characterLink'] is not None:
            result += "    Character Profile: <" + characterDataIn['characterLink'] + ">\n";
        if characterDataIn['characterGuild'] is not None:
            result += "    Freecompany: " + characterDataIn['characterGuild'] + "\n";
        if characterDataIn['characterGuildLink'] is not None:
            result += "    Freecompany Link: <" + characterDataIn['characterGuildLink'] + ">" + "\n";
        
        return result;
    
    def getLodestonePlayerInfo(self, world, firstName, lastName):
        lodestonePlayerListing = self.getLodestonePlayerListing(world, firstName, lastName);
        lodestonePlayerLink = None;
        
        if len(lodestonePlayerListing) > 0:
            lodestonePlayerLink = lodestonePlayerListing[0]['characterLink'];
            
            if lodestonePlayerLink is None:
                return "Could not retrieve link for the requested player", None;
        else:
            return "No players matching request found", None;
        
        requestResult = requests.get(lodestonePlayerLink, verify = False);
        soup = BeautifulSoup(requestResult.text, 'html.parser');
        
        searchResults = soup.body.findAll("div", {"id": "character"});
        result = "";
        resultImage = "";
        
        if searchResults is not None and len(searchResults) > 0:
            characterData = searchResults[0];
            characterProfile = characterData.find("div", {"class": "character__profile"});
            
            if characterProfile is not None and len(characterProfile) > 0:
                characterProfileData = characterData.find("div", {"class": "character__profile__data__detail"});
                characterProfileDetail = characterData.find("div", {"class": "character__profile__detail"});
                
                if characterProfileData is not None and len(characterProfileData) > 0 and characterProfileDetail is not None and len(characterProfileDetail) > 0:
                    characterProfileDataCharacterBlockBoxes = characterProfileData.findAll("div", {"class": "character-block__box"});
                    characterProfileDetailCharacterDetailImage = characterProfileDetail.find("div", {"class": "character__detail__image"});
                    characterProfileDetailCharacterLevelList = characterProfileDetail.findAll("div", {"class": "character__level__list"});
                    
                    if characterProfileDataCharacterBlockBoxes is not None and len(characterProfileDataCharacterBlockBoxes) > 0 and characterProfileDetailCharacterDetailImage is not None and len(characterProfileDetailCharacterDetailImage) > 0 and characterProfileDetailCharacterLevelList is not None and len(characterProfileDetailCharacterLevelList) > 0:
                        characterProfileDetailCharacterDetailImageJsImagePopup = characterProfileDetailCharacterDetailImage.find("a", {"class": "js__image_popup"});
                        
                        if characterProfileDetailCharacterDetailImageJsImagePopup is not None and len(characterProfileDetailCharacterDetailImageJsImagePopup) > 0:
                            resultImage = characterProfileDetailCharacterDetailImageJsImagePopup['href'];
                        else:
                            return "Could not get characterProfileDetailCharacterDetailImageJsImagePopup", None;
                        
                        result += self.generateCharacterBriefText(lodestonePlayerListing[0]);
                        
                        for characterProfileDataCharacterBlockBox in characterProfileDataCharacterBlockBoxes:
                            characterProfileDataCharacterBlockBoxElements = characterProfileDataCharacterBlockBox.findAll("p");
                            
                            if characterProfileDataCharacterBlockBoxElements is not None and len(characterProfileDataCharacterBlockBoxElements) > 0:
                                isEven = False;
                                currentLine = "";
                                for characterProfileDataCharacterBlockBoxElement in characterProfileDataCharacterBlockBoxElements:
                                    if not isEven:
                                        currentLine += "    " + characterProfileDataCharacterBlockBoxElement.getText() + ": ";
                                        isEven = True;
                                    else:
                                        currentLine += characterProfileDataCharacterBlockBoxElement.getText(separator=" / ") + "\n";
                                        isEven = False;
                                if not isEven:
                                    result += currentLine;
                            else:
                                return "Could not get characterProfileDataCharacterBlockBoxElements", None;
                        
                        for characterProfileDetailCharacterLevels in characterProfileDetailCharacterLevelList:
                            characterProfileDetailCharacterLevelListItems = characterProfileDetailCharacterLevels.findAll("li");
    
                            if characterProfileDetailCharacterLevelListItems is not None and len(characterProfileDetailCharacterLevelListItems) > 0:
                                for characterProfileDetailCharacterLevelListItem in characterProfileDetailCharacterLevelListItems:
                                    characterProfileDetailCharacterLevelItem = characterProfileDetailCharacterLevelListItem.find("img");
    
                                    if characterProfileDetailCharacterLevelItem is not None:
                                        result += "    " + characterProfileDetailCharacterLevelItem['data-tooltip'] + ": " + characterProfileDetailCharacterLevelListItem.getText() + "\n";
                                    else:
                                        return "Could not find characterProfileDetailCharacterLevelItem", None;
                            else:
                                return "Could not find characterProfileDetailCharacterLevelListItems", None;
                    else:
                        return "Could not retrieve characterProfileDataCharacterBlocks, characterProfileDetailCharacterDetailImage, or characterProfileDetailCharacterLevelList", None;
                else:
                    return "Could not get characterProfileData and characterProfileDetail", None;
        else:
            return "Could not find character data", None;
        
        return result, resultImage;
    
    def __init__(self, discordClient):
        self.discordClient = discordClient;
        self.lodeStoneBaseUrl = "https://na.finalfantasyxiv.com";
        self.lodeStoneCharacterSearchUrl = self.lodeStoneBaseUrl + "/lodestone/character/";
        
    @commands.command(brief="Provides a brief on the target player", description="Provides a brief on the target player")
    async def lodestoneCharacterBrief(self, ctx, world, firstName, lastName):
        characters = self.getLodestonePlayerListing(world, firstName, lastName);
        if len(characters) > 0:
            for character in characters:
                await ctx.send(self.generateCharacterBriefText(character));
        else:
            await ctx.send("No results found");
    
    @commands.command(brief="Provides some more detailed information on the target player", description="Provides some more detailed information on the target player")
    async def lodestonePlayerInfo(self, ctx, world, firstName, lastName):
        resultMessage, resultImage = self.getLodestonePlayerInfo(world, firstName, lastName);
        if resultImage is not None:
            embedImage = discord.Embed();
            embedImage.set_image(url=resultImage);
            await ctx.send("", embed=embedImage);
            await ctx.send(resultMessage);
        else:
             await ctx.send(resultMessage);
