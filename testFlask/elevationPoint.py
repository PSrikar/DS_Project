import requests

def elevation():
    response = requests.get(
    'https://api.stormglass.io/v2/elevation/point',
    params={
        'lat': 58.7984,
        'lng': 17.8081,
    },
    headers={
        'Authorization': 'c6baec26-1f3b-11ec-9b0e-0242ac130002-c6baec94-1f3b-11ec-9b0e-0242ac130002'
    }
    )

    # Do something with response data.
    json_data = response.json()

    print(json_data)

    return json_data