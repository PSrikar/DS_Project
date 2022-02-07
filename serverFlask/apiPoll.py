from flask import Flask,jsonify
import requests
import arrow
import calendar
import time
import json
from datetime import datetime, timedelta,timezone
app = Flask(__name__)

# if __name__ == '__main__':
#     app.run(host="0.0.0.0", port=20000, debug=True)

auth ='077cbc8c-2b74-11ec-baa5-0242ac130002-077cbd40-2b74-11ec-baa5-0242ac130002'

#a25e0536-3456-11ec-83d3-0242ac130002-a25e05ae-3456-11ec-83d3-0242ac130002

endtime = (datetime.now(timezone.utc) + timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M:%S')
starttime =datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S')
middlewares = [
    'http://middleware:5000/api/notify',
    'http://middleware01:5001/api/notify',
    'http://middleware02:5002/api/notify'
]

def elevation():
    response = requests.get(
    'https://api.stormglass.io/v2/elevation/point',
    params={
        'lat': 58.7984,
        'lng': 17.8081,
    },
    headers={
        'Authorization': auth
    }
    )

    # Do something with response data.
    json_data = response.json()

    print(json_data)

    return json_data

def bio():
        # Get first hour of today
    start = arrow.now().floor('day')

    # Get last hour of today
    end = arrow.now().ceil('day')

    response = requests.get(
    'https://api.stormglass.io/v2/bio/point',
    params={
        'lat': 58.7984,
        'lng': 17.8081,
        'params': ','.join(['iron', 'nitrate']),
        'start': starttime, #'2021-10-23T04:00:00+00:00',  # Convert to UTC timestamp
        'end': endtime #'2021-10-23T23:00:00+00:00'  # Convert to UTC timestamp
    },
    headers={
        'Authorization': auth
    }
    )
    print("Start",calendar.timegm(start.utctimetuple()))
    print("End",calendar.timegm(end.utctimetuple()))   
    # Do something with response data.
    json_data = response.json()
    print(json_data)
    return json_data 

def seaLevel():
    start = arrow.now().floor('day')
    end = arrow.now().shift(days=1).floor('day')

    response = requests.get(
    'https://api.stormglass.io/v2/tide/sea-level/point',
    params={
        'lat': 43.38,
        'lng': -3.01,
        'start': starttime, #'2021-10-23T04:00:00+00:00',  # Convert to UTC timestamp
        'end': endtime #'2021-10-23T23:00:00+00:00'  # Convert to UTC timestamp
    },
    headers={
        'Authorization': auth
    }
    )

    # Do something with response data.
    json_data = response.json()        
    print(json_data)
    return json_data


def astronomy():
    # Get first hour of today
    start = arrow.now().floor('day')
    end = arrow.now().shift(days=1).floor('day')



    response = requests.get(
    'https://api.stormglass.io/v2/astronomy/point',
    params={
        'lat': 58.7984,
        'lng': 17.8081,
        'start': starttime,#'2021-11-03T04:00:00+00:00',  # Convert to UTC timestamp
        'end': endtime #'2021-11-03T23:00:00+00:00'  # Convert to UTC timestamp
    },
    headers={
        'Authorization': auth
    }
    )

    # Do something with response data.
    json_data = response.json()    
    print(json_data)
    return json_data

def notifyMiddleware():

    elevationPoint = elevation()
    elevationPoint['api'] = "elevationPoint"
    bioData = bio()
    bioData['api'] = "bio"
    seaLevelData = seaLevel()
    seaLevelData['api'] = "seaLevel"
    astronomyData = astronomy()
    astronomyData['api'] = "astronomy"
    res0 = requests.post('http://middleware:5000/api/notify',json.dumps(elevationPoint))
    res1 = requests.post('http://middleware:5000/api/notify',json.dumps(bioData))
    res2 = requests.post('http://middleware:5000/api/notify',json.dumps(seaLevelData))
    res3=requests.post('http://middleware:5000/api/notify',json.dumps(astronomyData))

    for middleware in middlewares:
        requests.post(middleware,json.dumps(elevationPoint))
        requests.post(middleware,json.dumps(bioData))
        requests.post(middleware,json.dumps(seaLevelData))
        requests.post(middleware,json.dumps(astronomyData))








starttime = time.time()
while True:
    print("tick",(30 -(time.time() % 30.0)))
    notifyMiddleware()
    time.sleep(45 -(time.time() % 45.0))

