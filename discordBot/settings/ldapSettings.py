import json

class ldapSettingsClass:
    def __init__(self, jsonPath):
        with open(jsonPath) as jsonFile:
            jsonData = json.load(jsonFile);
            self.host = jsonData["host"];
            self.dn = jsonData["dn"];
            self.user = jsonData["user"] + "," + self.dn;
            self.password = jsonData["password"];
            self.managementGroup = jsonData["managementGroup"] + "," + self.dn;
            self.memberGroup = jsonData["memberGroup"] + "," + self.dn;
            self.banGroup = jsonData["banGroup"] + "," + self.dn;
