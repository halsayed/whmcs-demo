import requests
import sys

url = 'http://10.38.11.42:5000/api'
payload = {
    'var1': sys.argv[1],
    'var2': 'another here'
}

resp = requests.post(url, json=payload)
if resp.status_code == 200:
    print('success')
else:
    print('failure')
