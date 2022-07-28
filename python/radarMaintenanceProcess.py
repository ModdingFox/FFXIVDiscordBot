#!/bin/python3
from kazoo.client import KazooClient;
from influxdb import InfluxDBClient;
from time import time;

zookeeper = KazooClient(hosts='127.0.0.1:2181');
influxDB = InfluxDBClient(host='127.0.0.1', port=8086);

influxDB.create_database('radar');
influxDB.switch_database('radar');

def playerStatTemplate(playerName, eventType, currentTime, ctime, mtime):
    return {
        "measurement": "player",
        "tags": { "name": playerName, "eventType": eventType },
        "fields": {
            "count": 1,
            "ctime": ctime,
            "mtime": mtime,
            "duration": mtime - ctime
        }
    };

zookeeper.start();
currentTime = int(time() * 1000);
children = zookeeper.get_children("/radar/players");
influxPoints = [];

influxPoints.append({
    "measurement": "count",
    "fields": { "playerCount": len(children) }
});

for childName in children:
    childPath = "/radar/players/{0}".format(childName)
    child = zookeeper.get(childPath);
    timeDiff = currentTime - child[1].mtime;
    if timeDiff > (10 * 1000):
        influxPoints.append(
            playerStatTemplate(
                childName,
                "OutOfRange",
                currentTime,
                child[1].ctime,
                child[1].mtime
        ));
        zookeeper.delete(childPath, recursive=True);
    else:
        influxPoints.append(
            playerStatTemplate(
                childName,
                "InRange",
                currentTime,
                child[1].ctime,
                child[1].mtime
        ));
zookeeper.stop();
influxDB.write_points(influxPoints);
