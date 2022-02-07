from flask.wrappers import Request
from mongoengine.fields import StringField
import requests
#from . import elevationPoint
from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from flask_mongoengine import MongoEngine
import json
import os
import docker
from flask_cors import CORS , cross_origin

app = Flask(__name__)
CORS(app)

myServer = "middleware01"
# if __name__ == '__main__':
#     app.debug=True
#     app.run(host='0.0.0.0')

app.config['MONGODB_SETTINGS'] = {
    'db': 'pubsub',
    'host': 'mongo',
    'port': 27017
}
db = MongoEngine()
db.init_app(app)

notificationQueue = []



class Pubs(db.Document):
    name = db.StringField()
    url = db.StringField()

    def to_json(self):
        return {"name": self.name,
                "url": self.url}


publisherList = [
    {Pubs(name="elevationPoint",
               url="https://api.stormglass.io/v2/elevation/point")},
    {Pubs(name="bio",
               url="https://api.stormglass.io/v2/bio/point")},
    {Pubs(name="seaLevel",
               url="https://api.stormglass.io/v2/tide/sea-level/point")},
    {Pubs(name="astronomy",
               url="https://api.stormglass.io/v2/astronomy/point")}                      
]

class Subs(db.Document):
    name = db.StringField()
    username = db.StringField()
    email = db.StringField()
    pwd = db.StringField()

    def to_json(self):
        return {"name": self.name,
                "username": self.username,
                "email": self.email,
                "pwd": self.pwd}


class PubSub(db.Document):
    pub_name = db.StringField()  # Pubs.name
    sub_username = db.StringField()  # Subs.username

    def to_json(self):
        return {"pub_name": self.pub_name,
                "sub_username": self.sub_username}


class Events(db.Document):
    pub_name = Pubs.name
    sub_username = Subs.username
    message = db.StringField()

    def to_json(self):
        return {"pub_name": self.pub_name,
                "sub_username": self.sub_username,
                "message": self.message}

class BrokerNetwork(db.Document):
    pub_name = db.StringField()
    broker_name = db.StringField()
    brokerAddress = db.StringField()

    def to_json(self):
        return {"pub_name": self.pub_name,
                "broker_name" : self.broker_name,
                "brokerAddress":self.brokerAddress
        }

@app.route("/api/hello")
def hello_world():
    return "Hey from the server"

@app.route("/api/hostname")
def getHostname():
    return str(os.environ["HOSTNAME"])

@app.route("/api/ImageName")
def getImageName():
    #return str(subprocess.check_output(['bash','-c', 'echo $NAME']) )
    client = docker.from_env()
    return str(client )


def connectDB():
    mongodb_client = PyMongo(app, uri="mongodb://localhost:27017/pubsub")
    db = mongodb_client.db
    print("connection successful")
    return db


@app.route("/api/insertPubs")
def pushDefaultPubs():
    pub=Pubs(name="elevationPoint",
               url="https://api.stormglass.io/v2/elevation/point")
    pub.save()
    pub.update(name="elevationPoint")
    pub1 = Pubs(name="bio",
               url="https://api.stormglass.io/v2/bio/point")
    pub1.save()
    pub1.update(name="bio")
    pub2 = Pubs(name="seaLevel",
               url="https://api.stormglass.io/v2/tide/sea-level/point")
    pub2.save()
    pub2.update(name="seaLevel")           
    pub3 = Pubs(name="astronomy",
               url="https://api.stormglass.io/v2/astronomy/point")
    pub3.save()
    pub3.update(name="astronomy")           
    return "Publishers Added Successfully"

    
@app.route("/api/insertNetwork")
def pushDefaultBrokers():
    broker01 = BrokerNetwork(broker_name="middleware",
                            pub_name="elevationPoint")
    broker01.save()
    broker02 = BrokerNetwork(broker_name="middleware",
                            pub_name="astronomy")
    broker02.save()
    broker03 = BrokerNetwork(broker_name="middleware01",
                             pub_name = "bio")
    broker03.save()
    broker04 = BrokerNetwork(broker_name = "middleware02",
                            pub_name = "seaLevel")
    broker04.save()
    return "Brokers added Successfully"
                        


@app.route("/api/createPubs", methods=['PUT'])
def insertPubs():
    records = json.loads(request.data)
    print(records)
    pub = Pubs(name=records['name'],
               url=records['url'])
    pub.save()
    return jsonify(pub.to_json())


@app.route("/api/getPubs", methods=['GET'])
def getPubs():
    pubs = Pubs.objects.all()
    if not pubs:
        return jsonify({'error': 'data not found'})
    else:
        return jsonify(pubs.to_json())


@app.route("/api/createSubs", methods=['PUT'])
def insertSubs():
    records = json.loads(request.data)
    print("records", records)
    sub = Subs(name=records['subDetails']['name'],
               username=records['subDetails']['username'],
               email=records['subDetails']['email'],
               pwd=records['subDetails']['pwd'])
    print("Subs", sub.to_json())
    sub.save(force_insert=True)
    sub.update(username=records['subDetails']['username'])
    return jsonify(sub.to_json())


@app.route("/api/getSubs", methods=['GET'])
def getSubs():
    subs = Subs.objects.all()
    if not subs:
        return jsonify({'error': 'data not found'})
    else:
        return jsonify(subs.to_json())


@app.route("/api/getSub", methods=['GET'])
def getSub():
    username = request.args.get('username')
    sub = Subs.objects(username=username).first()
    sub['pwd'] = '***********'
    if not sub:
        return jsonify({'error': 'data not found'})
    else:
        return jsonify(sub.to_json())


@app.route("/api/subscribe", methods=['PUT'])
def subscribe():
    records = json.loads(request.data)
    print(records)
    subscription = PubSub(pub_name=records['pubsub']['pub_name'],
                          sub_username=records['pubsub']['sub_username'][1:])
    subscription.save()
    return jsonify(subscription.to_json())


@app.route("/api/unsubscribe", methods=['DELETE'])
def unsubcribe():
    record = json.loads(request.data)
    print(record)
    pubsub = PubSub.objects(
        pub_name=record['pub_name'], sub_username=record['sub_username'][1:]).first()
    if not pubsub:
        return "Record not Subscribed"
    else:
        pubsub.delete()
    return "Unsubscribe successful"


@app.route("/api/saveNotification", methods=['PUT'])
def saveMessage():
    records = json.loads(request.data)
    event = Events(pub_name=records['pub_name'],
                   sub_username=records['sub_username'],
                   message=records['message'])
    print(event)
    event.save()
    return jsonify(event.to_json())


@app.route("/api/login", methods=['POST'])
def login():
    records = json.loads(request.data)
    print(records)
    print("Password", records['subDetails']['password'])
    subscriber = Subs.objects(
        username=records['subDetails']['username'], pwd=records['subDetails']['password']).first()
    if not subscriber:
        return "Failed"
    else:
        return "OK"


@app.route("/api/notify", methods=['POST'])
def getNotify():
    records = json.loads(request.data)
    print(records)
    notificationQueue.append(records)
    print("notificationQueue")
    #print(notificationQueue)
    return "notification successful"


@app.route("/api/notify1", methods=['GET'])
@cross_origin(origin='*')
def pushNotifications01():
    username = request.args.get('username')
    print("username", username)
    pubsub = PubSub.objects(sub_username=username[1:]).all()
    print("pubsubs", pubsub)
    subscribedTopics = []
    matchedTopics = []
    i = 0
    for s in pubsub:
        subscribedTopics.append(s.pub_name)
    for n in notificationQueue:
        if n['api'] in subscribedTopics:
            matchedTopics.append(n)
            notificationQueue.pop(i)
        i = i+1
    print("Topics Subscribed", subscribedTopics)
    print("notificationQueue size",len(notificationQueue))
    #print(notificationQueue)
    print("Matched topics", matchedTopics)
    # notificationQueue.clear()
    return jsonify(matchedTopics)


@app.route("/api/advertise", methods=['PUT'])
def advertise():
    records = json.loads(request.data)
    print(records)
    pub = Pubs(name=records['name'],
               url=records['url'])
    pub.save()
    return jsonify(pub.to_json())

@app.route("/api/deadvertise",methods=['DELETE'])
def deadvertise():
    record = json.loads(request.data)
    print(record)
    pub = Pubs.objects(
        name=record['name']).first()
    if not pub:
        return "Record not advertised"
    else:
        pub.delete()
    return "Advertise successful"

@app.route("/api/brokerInfo",methods=['Get'])
def getBrokerInfo():
    brokers = BrokerNetwork.objects.all()
    if not brokers:
        return jsonify({"error":"Broker data not found"})
    else:
        return jsonify(brokers.to_json())

@app.route("/api/notify", methods=['GET'])
@cross_origin(origin='*')
def pushNotifications():
    username = request.args.get('username')
    print("username", username)
    pubsub = PubSub.objects(sub_username=username[1:]).all()
    brokerFilter = BrokerNetwork.objects(broker_name=myServer).all()
    brokers = []
    for broker in brokerFilter:
        brokers.append(broker["pub_name"])
    print("pubsubs", pubsub)
    print("brokerNet",brokers)
    subscribedTopics = []
    matchedTopics = []
    i = 0
    for s in pubsub:
        subscribedTopics.append(s.pub_name)
    for n in notificationQueue:
        if n['api'] in subscribedTopics and n['api'] in brokers:
            matchedTopics.append(n)
            notificationQueue.pop(i)
        i = i+1
    print("Topics Subscribed", subscribedTopics)
    print("notificationQueue")
    #print(notificationQueue)
    print("Matched topics", matchedTopics)
    return jsonify(matchedTopics)

@app.route("/api/addBroker",methods=['POST'])
def addBroker():
    records = json.loads(request.data)
    print(records)
    for bro in records:
        broker = BrokerNetwork(broker_name=bro['broker_name'],pub_name=bro['pub_name'],brokerAddress=bro['brokerAddress'])
        broker.save()
    if not broker:
        return "Failed to Add Broker"
    else:
        return "OK"

@app.route("/api/addMe",methods=['GET'])
def addME():
    myRecord = [{
    "broker_name":myServer,
    "pub_name":"bio",
    "brokerAddress": "http://localhost:5001/"
    }
    ]
    res0 = requests.post('http://middleware02:5002/api/addBroker',json.dumps(myRecord))
    if not res0:
        return "Failed"
    else:
        return "I got added to the network"