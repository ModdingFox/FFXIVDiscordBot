CREATE DATABASE ClubSpectrum;

CREATE TABLE ClubSpectrum.applications
(
    id        INT     NOT NULL AUTO_INCREMENT,
    guildId   TEXT    NOT NULL,
    question1 TEXT,
    question2 TEXT,
    question3 TEXT,
    question4 TEXT,
    question5 TEXT,
    question6 TEXT,
    question7 TEXT,
    question8 TEXT,
    question9 TEXT,
    question10 TEXT,
    question11 TEXT,
    PRIMARY KEY (id)
);

CREATE TABLE ClubSpectrum.radar
(
    name           TEXT    NOT NULL,
    world          TEXT    NOT NULL,
    inRangeTime    TIMESTAMP NULL,
    outOfRangeTime TIMESTAMP NULL
);
