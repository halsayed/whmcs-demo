import requests


def new(params):
    url = 'http://10.38.11.42:5000/api'
    resp = requests.post(url, json=params)
    if resp.status_code == 200:
        return resp.json()
    else:
        return {'error': 'api call failed'}
