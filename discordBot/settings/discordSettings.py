import json

class discordSettingsClass:
    def __init__(self, jsonPath):
        with open(jsonPath) as jsonFile:
            jsonData = json.load(jsonFile);
            self.token = jsonData["token"];
            self.commandPrefix = jsonData["commandPrefix"];
