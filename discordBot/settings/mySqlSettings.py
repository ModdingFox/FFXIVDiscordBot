import json

class mySqlSettingsClass:
    def __init__(self, jsonPath):
        with open(jsonPath) as jsonFile:
            jsonData = json.load(jsonFile);
            self.host = jsonData["host"];
            self.user = jsonData["user"];
            self.password = jsonData["password"];
