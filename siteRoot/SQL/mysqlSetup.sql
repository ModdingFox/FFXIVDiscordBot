DROP DATABASE IF EXISTS userAccountData;
DROP DATABASE IF EXISTS discord;
DROP DATABASE IF EXISTS ffxivPlayers;
DROP DATABASE IF EXISTS ffxivReference;
DROP DATABASE IF EXISTS ffxivStatic;

CREATE DATABASE userAccountData COLLATE utf8mb4_unicode_ci;
CREATE DATABASE discord COLLATE utf8mb4_unicode_ci;
CREATE DATABASE ffxivPlayers COLLATE utf8mb4_unicode_ci;
CREATE DATABASE ffxivReference COLLATE utf8mb4_unicode_ci;
CREATE DATABASE ffxivStatic COLLATE utf8mb4_unicode_ci;

CREATE TABLE userAccountData.discordLink
(
    id                  INT     NOT NULL AUTO_INCREMENT,
    userCN              TEXT    NOT NULL,
    discordId           TEXT    NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE discord.cookies
(
    id                              INT       NOT NULL AUTO_INCREMENT,
    discordLinkId                   INT       NOT NULL,
    totalCookies                    INT       NOT NULL DEFAULT 0,
    giveMeCookiesLastTimestamp      TIMESTAMP     NULL,
    stealCookiesFromLastTimestamp   TIMESTAMP     NULL,
    discordVCJoinLastTimestamp      TIMESTAMP     NULL,
    discordVCLastTimestamp          TIMESTAMP     NULL,
    discordTextMessageCount         INT       NOT NULL DEFAULT 0,
    discordTextMessageLastTimestamp TIMESTAMP     NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (discordLinkId) REFERENCES userAccountData.discordLink(id) ON DELETE CASCADE
);

CREATE TRIGGER discord_cookies_dates BEFORE INSERT ON discord.cookies
FOR EACH ROW SET
    NEW.giveMeCookiesLastTimestamp      = IFNULL(NEW.giveMeCookiesLastTimestamp      , TIMESTAMPADD(DAY, -1, NOW())),
    NEW.stealCookiesFromLastTimestamp   = IFNULL(NEW.stealCookiesFromLastTimestamp   , TIMESTAMPADD(DAY, -1, NOW())),
    NEW.discordVCJoinLastTimestamp      = IFNULL(NEW.discordVCJoinLastTimestamp      , TIMESTAMPADD(DAY, -1, NOW())),
    NEW.discordVCLastTimestamp          = IFNULL(NEW.discordVCLastTimestamp          , TIMESTAMPADD(DAY, -1, NOW())),
    NEW.discordTextMessageLastTimestamp = IFNULL(NEW.discordTextMessageLastTimestamp , TIMESTAMPADD(DAY, -1, NOW()));

CREATE TABLE textChatLog
(
    id               INT       NOT NULL AUTO_INCREMENT,
    messageTimestamp TIMESTAMP     NULL,
    authorId         TEXT      NOT NULL,
    channelId        TEXT      NOT NULL,
    messageContent   TEXT      NOT NULL,
    attachmentUrls   TEXT          NULL,
    PRIMARY KEY (id)
);

CREATE TRIGGER discord_textChatLog_timestamps BEFORE INSERT ON discord.textChatLog
FOR EACH ROW SET
    NEW.messageTimestamp = IFNULL(NEW.messageTimestamp , NOW());

CREATE TABLE discord.voiceChatLog
(
    id                    INT       NOT NULL AUTO_INCREMENT,
    discordUserId         TEXT      NOT NULL,
    userName              TEXT      NOT NULL,
    channelId             TEXT          NULL,
    channelName           TEXT      NOT NULL,
    joinChannelTimeStamp  TIMESTAMP     NULL,
    leaveChannelTimestamp TIMESTAMP     NULL,
    PRIMARY KEY (id)
);

CREATE TRIGGER discord_voiceChatLog_dates BEFORE INSERT ON discord.voiceChatLog
FOR EACH ROW SET
    NEW.joinChannelTimeStamp      = IFNULL(NEW.joinChannelTimeStamp      , NOW());

CREATE TABLE ffxivReference.classes
(
    id   INT  NOT NULL AUTO_INCREMENT,
    name TEXT NOT NULL,
    PRIMARY KEY (id)
);

INSERT INTO ffxivReference.classes (name) VALUES ("Astrologian");
INSERT INTO ffxivReference.classes (name) VALUES ("Bard");
INSERT INTO ffxivReference.classes (name) VALUES ("Black Mage");
INSERT INTO ffxivReference.classes (name) VALUES ("Dancer");
INSERT INTO ffxivReference.classes (name) VALUES ("Dark Knight");
INSERT INTO ffxivReference.classes (name) VALUES ("Dragoon");
INSERT INTO ffxivReference.classes (name) VALUES ("Gunbreaker");
INSERT INTO ffxivReference.classes (name) VALUES ("Machinist");
INSERT INTO ffxivReference.classes (name) VALUES ("Monk");
INSERT INTO ffxivReference.classes (name) VALUES ("Ninja");
INSERT INTO ffxivReference.classes (name) VALUES ("Paladin");
INSERT INTO ffxivReference.classes (name) VALUES ("Red Mage");
INSERT INTO ffxivReference.classes (name) VALUES ("Samurai");
INSERT INTO ffxivReference.classes (name) VALUES ("Scholar");
INSERT INTO ffxivReference.classes (name) VALUES ("Summoner");
INSERT INTO ffxivReference.classes (name) VALUES ("Warrior");
INSERT INTO ffxivReference.classes (name) VALUES ("White Mage");

CREATE TABLE ffxivPlayers.playerCharacters
(
    id                  INT     NOT NULL AUTO_INCREMENT,
    userCN              TEXT    NOT NULL,
    characterFirstName  TEXT    NOT NULL,
    characterLastName   TEXT    NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE ffxivPlayers.characterClasses
(
    id                INT NOT NULL AUTO_INCREMENT,
    playerCharacterId INT NOT NULL,
    classId           INT NOT NULL,
    currentLevel      INT NOT NULL DEFAULT -1,
    averageILevel     INT NOT NULL DEFAULT -1,
    hasMeldsCheckbox  BOOLEAN NOT NULL DEFAULT false,
    PRIMARY KEY (id),
    FOREIGN KEY (playerCharacterId) REFERENCES ffxivPlayers.playerCharacters(id) ON DELETE CASCADE,
    FOREIGN KEY (classId) REFERENCES ffxivReference.classes(id) ON DELETE CASCADE
);

CREATE TABLE ffxivStatic.playerRegistrationStatic
(   
    id                  INT     NOT NULL AUTO_INCREMENT,
    userCN              TEXT    NOT NULL,
    hasSavageExperience BOOLEAN NOT NULL DEFAULT false,
    hasRaidExperience   BOOLEAN NOT NULL DEFAULT false,
    sunday              BOOLEAN NOT NULL DEFAULT false,
    monday              BOOLEAN NOT NULL DEFAULT false,
    tuesday             BOOLEAN NOT NULL DEFAULT false,
    wednesday           BOOLEAN NOT NULL DEFAULT false,
    thursday            BOOLEAN NOT NULL DEFAULT false,
    friday              BOOLEAN NOT NULL DEFAULT false,
    saturday            BOOLEAN NOT NULL DEFAULT false,
    PRIMARY KEY (id)
);
