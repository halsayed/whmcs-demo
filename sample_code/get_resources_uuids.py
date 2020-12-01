import os
import base64
import requests

# disable ssl warnings
import urllib3
urllib3.disable_warnings()

# API configuration and parameters ...
pc_address = '127.0.0.1'
username = 'admin'
password = os.environ.get('PASSWORD')  # change the password to a suitable value
authorization = base64.b64encode(f'{username}:{password}'.encode()).decode()
url = f'https://{pc_address}:9440/api/nutanix/v3'
kwargs = {
    'verify': False,
    'headers': {'Authorization': f'Basic {authorization}'}
}


# ==========================================================================================
# List the available clusters (PEs) connected to this Prism Central
# ==========================================================================================
payload = {'kind': 'cluster'}
resp = requests.post(f'{url}/clusters/list', json=payload, **kwargs)
if resp.status_code == 200:
    count = 1
    print('\n==========================\nAvailable Clusters\n==========================')
    for cluster in resp.json()['entities']:
        # Note: PC itself is a cluster, but it cannot be used as a resource to provision VMs,
        # check for 'AOS' type cluster to run VMs
        if 'AOS' in cluster['status']['resources']['config'].get('service_list', []):
            print(f'({count}) Name: {cluster["status"]["name"]},\t UUID: {cluster["metadata"]["uuid"]}')
            count += 1
else:
    print(f'ERROR - API call failed, status code: {resp.status_code}, message: {resp.content}')


# ==========================================================================================
# List the available Networks
# ==========================================================================================
payload = {'kind': 'subnet', 'length': 999}
resp = requests.post(f'{url}/subnets/list', json=payload, **kwargs)
if resp.status_code == 200:
    count = 1
    print('\n==========================\nAvailable Subnets\n==========================')
    for subnet in resp.json()['entities']:
        print(f'({count}) Name: {subnet["status"]["name"]},\t UUID: {subnet["metadata"]["uuid"]}')
        count += 1
else:
    print(f'ERROR - API call failed, status code: {resp.status_code}, message: {resp.content}')


# ==========================================================================================
# List the available Images
# ==========================================================================================
payload = {'kind': 'image', 'length': 999}
resp = requests.post(f'{url}/images/list', json=payload, **kwargs)
if resp.status_code == 200:
    count = 1
    print('\n==========================\nAvailable Images\n==========================')
    for image in resp.json()['entities']:
        print(f'({count}) Name: {image["spec"]["name"]},\t UUID: {image["metadata"]["uuid"]}')
        count += 1
else:
    print(f'ERROR - API call failed, status code: {resp.status_code}, message: {resp.content}')
