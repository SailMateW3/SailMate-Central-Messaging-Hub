import paho.mqtt.client as mqtt
import ssl
import asyncio
import logging
import time
import conf
import json
from random import randint
from datetime import datetime
from pymongo import MongoClient
from streamrClient import StreamrClient


# number of subscribers

SUB_NUM = conf.SUB_NUM

def unsubClient(client, topic):
    client.unsubscribe(topic)

def on_unsubscribe(client, userdata, mid):
    print("Unsubscribed from")
    

def connectClient(client):
    client.tls_set("./broker/config/ca_certs/ca.crt",
                tls_version=ssl.PROTOCOL_TLSv1_2,)
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_unsubscribe = on_unsubscribe
    client.connect(conf.MQTT, 8883, 60)
    client.loop_start()


def on_connect(client, userdata, flags, rc):
    cname = client._client_id.decode("utf-8")
    id = cname.split("Client")
    id = int(id[1])
    print("Connecting" + cname)
    print("Connected with result code " + str(rc))
    i = id % len(conf.TOPICS)
    print("Subscribing to " + conf.TOPICS[i])
    topic = pickTopic(i)
    client.subscribe(topic, 2)

def pickTopic(i):
    return conf.TOPICS[i]

def parseTimestamps(msg):
    decoded = msg.payload.decode("utf-8")
    return json.loads(decoded)
    

def on_message(client, userdata, msg):
    #logging.info(str(client._client_id) + ": " + msg.topic + " " + str(msg.payload) + " qos: " + str(msg.qos))
    clnt = str(client._client_id)
    topic = msg.topic
    timenow = datetime.now()
    ts = datetime.strptime(jsonOfMsg["timestamp"], "%Y-%m-%d %H:%M:%S.%f")
    print(clnt + ": " + topic + " " + str(jsonOfMsg) + " qos: " + str(msg.qos))
    # Publish to Streamr client
    # TODO: Make it work ::DD
    streamrClient.publish(conf.WALLETID)



async def main():
    clients = []
    for i in range(SUB_NUM):
        clientID = "Client"+str(i)
        client = createClient(clientID)
        connectClient(client)
        clients.append(client)
    # take user input
    while True:
        try:
            userInput = input("Enter a topic to unsubscribe to: ")
            clientId = int(input("Enter a client ID to unsubscribe from: "))
            unsubClient(clients[clientId], userInput)
            break
        except KeyboardInterrupt:
            break

        

def __main__():
    #logging.basicConfig(filename = "analysis.log", level = logging.INFO, format = "%(asctime)s:%(message)s")
    loop = asyncio.get_event_loop()
    try:
        asyncio.ensure_future(main())
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        print("Closing Loop")
        loop.close()

__main__()