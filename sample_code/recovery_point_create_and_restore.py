import os
import base64
import requests
from time import sleep

# disable ssl warnings
import urllib3
urllib3.disable_warnings()

# API configuration and parameters ...
pc_address = '10.38.7.9'
username = 'admin'
# password = os.environ.get('PASSWORD')  # change the password to a suitable value
password = 'nx2Tech911!'
authorization = base64.b64encode(f'{username}:{password}'.encode()).decode()
url = f'https://{pc_address}:9440/api/nutanix/v3'
kwargs = {
    'verify': False,
    'headers': {'Authorization': f'Basic {authorization}'}
}

# Define source VM name
# ------------------------------------------
vm_name = 'test-1'
snapshot_name = 'snap-1'

# ========================================================
# ==== Get VM UUID
# ========================================================
payload = {
    'kind': 'vm',
    'filter': f'vm_name=={vm_name}'
}
resp = requests.post(f'{url}/vms/list', json=payload, **kwargs)
if resp.status_code == 200:
    print(f'\nGetting uuid of vm: {vm_name}')
    if resp.json()['metadata']['length']:
        vm_uuid = resp.json()['entities'][0]['metadata']['uuid']
        print(f'VM found, uuid: {vm_uuid}')
    else:
        print('VM not found, stopping ...')
        exit(0)
else:
    print(f'ERROR - API call failed, status code: {resp.status_code}, message: {resp.content}')


# =========================================================
# ==== Create recovery point
# =========================================================
payload = {
    'name': snapshot_name,
    'recovery_point_type': 'CRASH_CONSISTENT'       # anotehr option could be APP_CONSISTENT
}
resp = requests.post(f'{url}/vms/{vm_uuid}/snapshot', json=payload, **kwargs)
if resp.status_code == 202:
    task_uuid = resp.json()['task_uuid']
    print(f'Snapshot created, task uuid: {task_uuid}')
else:
    print(f'ERROR - API call failed, status code: {resp.status_code}, message: {resp.content}')



# =========================================================
# ==== get snapshot uuid
# =========================================================
print('waiting for snapshot...')
sleep(3)
resp = requests.get(f'{url}/tasks/{task_uuid}', **kwargs)
if resp.status_code == 200:
    recovery_point_uuid = resp.json()['entity_reference_list'][0]['uuid']
    print(f'Recovery point uuid: {recovery_point_uuid}')
else:
    print(f'ERROR - API call failed, status code: {resp.status_code}, message: {resp.content}')


# =========================================================
# ==== restore VM from recovery point
# =========================================================
print(f'restoring VM {vm_name}...')
payload = {
    'vm_override_spec': {
        'name': f'restored-{vm_name}'
    }
}
resp = requests.post(f'{url}/vm_recovery_points/{recovery_point_uuid}/restore', json=payload, **kwargs)
if resp.status_code == 202:
    print(f'recovery point restored to new vm: restored-{vm_name}')
else:
    print(f'ERROR - API call failed, status code: {resp.status_code}, message: {resp.content}')
